"""Local integration tests. Starts its own server on an OS-assigned port."""
import os
from pathlib import Path
import queue
import re
import socket
import ssl
import struct
import subprocess
import sys
import threading
import time
import unittest

import tls_runtime
from chat_protocol import MAX_FRAME, recv_frame
from client import CA_CERT, CLIENT_CERT, CLIENT_KEY, SecureChatClient, create_context

ROOT = Path(__file__).resolve().parent


class Process:
    def __init__(self, *args):
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUNBUFFERED="1")
        self.proc = subprocess.Popen([sys.executable, "-u", *args], cwd=ROOT,
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT, text=True,
                                     encoding="utf-8", env=env)
        self.lines = []
        self.events = queue.Queue()
        self.reader = threading.Thread(target=self._read, daemon=True)
        self.reader.start()

    def _read(self):
        for line in self.proc.stdout:
            self.lines.append(line)
            self.events.put(line.rstrip("\r\n"))
        self.events.put(None)

    def wait_for(self, text, timeout=8):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                line = self.events.get(timeout=max(0.01, deadline-time.monotonic()))
            except queue.Empty:
                break
            if line is None:
                break
            if text in line:
                return line
        raise AssertionError(f"Missing {text!r}; output: {''.join(self.lines)[-4000:]}")

    def send(self, text):
        self.proc.stdin.write(text + "\n")
        self.proc.stdin.flush()

    def close(self):
        if self.proc.poll() is None:
            self.proc.terminate()
        self.proc.wait(timeout=5)
        self.reader.join(timeout=2)
        self.proc.stdin.close()
        self.proc.stdout.close()


class FramingTests(unittest.TestCase):
    def test_fragmented_and_coalesced_frames(self):
        first = "Xin chào Việt Nam".encode("utf-8")
        second = b"second frame"
        wire = struct.pack("!I", len(first)) + first + struct.pack("!I", len(second)) + second

        class Stream:
            def __init__(self):
                self.data = bytearray(wire)
            def recv(self, size):
                count = min(size, 3, len(self.data))
                result = bytes(self.data[:count])
                del self.data[:count]
                return result

        stream = Stream()
        self.assertEqual(recv_frame(stream), first)
        self.assertEqual(recv_frame(stream), second)
        self.assertIsNone(recv_frame(stream))

    def test_oversized_frame_rejected_before_payload_read(self):
        class Stream:
            def recv(self, size):
                return struct.pack("!I", MAX_FRAME + 1)
        with self.assertRaisesRegex(ValueError, "frame size"):
            recv_frame(Stream())

    def test_truncated_frame_rejected(self):
        class Stream:
            data = bytearray(b"\x00\x00\x00\x05abc")
            def recv(self, size):
                data = bytes(self.data[:size])
                del self.data[:size]
                return data
        with self.assertRaises(EOFError):
            recv_frame(Stream())


class ChatTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = Process("server.py", "--port", "0")
        ready = cls.server.wait_for("Listening on ")
        cls.port = int(ready.rsplit(":", 1)[1])
        print(f"\nTest server: 127.0.0.1:{cls.port} (separate from port 8443)", flush=True)

    @classmethod
    def tearDownClass(cls):
        cls.server.close()
        (ROOT / "work").mkdir(exist_ok=True)
        (ROOT / "work" / "chat-integration-server.log").write_text(
            "".join(cls.server.lines), encoding="utf-8")

    def setUp(self):
        self.clients = []

    def tearDown(self):
        for client in self.clients:
            client.close()

    def connect(self, name, **kwargs):
        c = SecureChatClient(name, port=self.port, **kwargs)
        c.sock.settimeout(5)
        self.clients.append(c)
        return c

    def test_two_clients_chat_bidirectionally(self):
        a, b = self.connect("alice_two"), self.connect("bob_two")
        self.assertEqual(ssl.SSLContext.__module__, "ssl")
        self.assertIn(a.sock.version(), ("TLSv1.2", "TLSv1.3"))
        self.assertTrue(a.sock.getpeercert())
        a.send("Xin chao Bob")
        self.assertEqual(b.receive(), "[alice_two]: Xin chao Bob")
        b.send("Chao Alice")
        self.assertEqual(a.receive(), "[bob_two]: Chao Alice")

    def test_long_unicode_and_burst_messages(self):
        a, b = self.connect("alice_long"), self.connect("bob_long")
        message = "Tiếng Việt an toàn 🔐 " * 300
        self.assertGreater(len(message.encode("utf-8")), 4096)
        a.send(message)
        self.assertEqual(b.receive(), "[alice_long]: " + message)
        for i in range(30):
            a.send(f"burst {i}")
        self.assertEqual([b.receive() for _ in range(30)],
                         [f"[alice_long]: burst {i}" for i in range(30)])

    def test_concurrent_senders_do_not_mix_frames(self):
        a, b, c = (self.connect(n) for n in ("writer_a", "writer_b", "reader_c"))
        errors = []
        def send_many(client):
            try:
                for i in range(15):
                    client.send(f"message {i}")
            except Exception as exc:
                errors.append(exc)
        threads = [threading.Thread(target=send_many, args=(p,)) for p in (a, b)]
        for thread in threads:
            thread.start()
        messages = [c.receive() for _ in range(30)]
        for thread in threads:
            thread.join(timeout=5)
            self.assertFalse(thread.is_alive())
        self.assertEqual(errors, [])
        self.assertEqual(set(messages), {
            f"[writer_{name}]: message {i}" for name in ("a", "b") for i in range(15)
        })

    def test_room_isolation_and_switching(self):
        a, b = self.connect("alice_rooms"), self.connect("bob_rooms")
        b.send("/join study")
        self.assertEqual(b.receive(), "[SYSTEM] Joined room study")
        a.send("only general")
        # A command response is an ordered marker: no general message may precede it.
        b.send("/users")
        self.assertEqual(b.receive(), "[SYSTEM] Users in study: bob_rooms")
        a.send("/join study")
        while True:
            response = a.receive()
            if response == "[SYSTEM] Joined room study":
                break
        a.send("same room now")
        self.assertEqual(b.receive(), "[alice_rooms]: same room now")
        b.send("/rooms")
        self.assertIn("study (2)", b.receive())

    def test_duplicate_username_rejected(self):
        self.connect("duplicate")
        with self.assertRaisesRegex(ConnectionError, "already in use"):
            self.connect("DUPLICATE")

    def test_disconnect_removes_membership(self):
        a, b = self.connect("alice_exit"), self.connect("bob_exit")
        a.send("/join cleanup")
        self.assertEqual(a.receive(), "[SYSTEM] Joined room cleanup")
        b.send("/join cleanup")
        self.assertEqual(b.receive(), "[SYSTEM] Joined room cleanup")
        a.send("exit")
        self.assertEqual(a.receive(), "[SYSTEM] Bye")
        self.assertIsNone(a.receive())
        b.send("/users")
        self.assertEqual(b.receive(), "[SYSTEM] Users in cleanup: bob_exit")

    def test_cli_two_real_clients_and_exit(self):
        a = Process("client.py", "--port", str(self.port), "--username", "cli_alice")
        b = Process("client.py", "--port", str(self.port), "--username", "cli_bob")
        try:
            a.wait_for("Type messages")
            b.wait_for("Type messages")
            a.send("Xin chao tu Alice")
            b.wait_for("[cli_alice]: Xin chao tu Alice")
            b.send("Bob da nhan duoc")
            a.wait_for("[cli_bob]: Bob da nhan duoc")
            for p in (a, b):
                p.send("exit")
                p.wait_for("[SYSTEM] Bye")
                self.assertEqual(p.proc.wait(timeout=5), 0)
            print("CLI evidence: Alice -> Bob and Bob -> Alice; both exited normally", flush=True)
        finally:
            a.close()
            b.close()

    def test_echo_cli(self):
        result = subprocess.run(
            [sys.executable, "client.py", "--port", str(self.port), "--echo"],
            cwd=ROOT, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Server received: Xin chao tu SecureChat Client", result.stdout)

    def test_missing_client_certificate_rejected(self):
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.load_verify_locations(cafile=CA_CERT)
        with self.assertRaises(ssl.SSLError):
            with socket.create_connection(("127.0.0.1", self.port), timeout=5) as raw:
                with ctx.wrap_socket(raw, server_hostname="localhost") as tls:
                    tls.sendall(b"\x00\x00\x00\x01x")
                    tls.recv(1)

    def test_wrong_hostname_rejected(self):
        with self.assertRaises(ssl.SSLCertVerificationError):
            self.connect("bad_hostname", server_name="wrong.example")

    def test_unknown_ca_rejected(self):
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ctx.load_cert_chain(CLIENT_CERT, CLIENT_KEY)
        with self.assertRaises(ssl.SSLCertVerificationError):
            self.connect("bad_ca", context=ctx)

    def test_tls12_remains_supported(self):
        ctx = create_context()
        ctx.maximum_version = ssl.TLSVersion.TLSv1_2
        c = self.connect("tls12", context=ctx)
        self.assertEqual(c.sock.version(), "TLSv1.2")
        c.send("/echo TLS12")
        self.assertEqual(c.receive(), "Server received: TLS12")

    def test_stalled_handshake_does_not_block_other_clients(self):
        with socket.create_connection(("127.0.0.1", self.port), timeout=5):
            c = self.connect("not_blocked")
            c.send("/echo still working")
            self.assertEqual(c.receive(), "Server received: still working")


if __name__ == "__main__":
    unittest.main(verbosity=2)
