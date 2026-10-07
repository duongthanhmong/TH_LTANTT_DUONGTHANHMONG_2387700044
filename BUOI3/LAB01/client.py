"""Interactive SecureChat client; type exit to finish, as in lab-03."""
import argparse
import os
import socket
import ssl
import threading
from pathlib import Path

import tls_runtime  # Keep CA/hostname validation while undoing startup injection.
from chat_protocol import MAX_TEXT, recv_frame, send_frame, validate_name
from message_encryption import MessageEncryption

HOST = "127.0.0.1"
PORT = 8443
BASE_DIR = Path(__file__).resolve().parent
CA_CERT = BASE_DIR / "certs/ca/ca.crt"
CLIENT_CERT = BASE_DIR / "certs/client/client.crt"
CLIENT_KEY = BASE_DIR / "certs/client/client.key"


def create_context(cafile=CA_CERT, certfile=CLIENT_CERT, keyfile=CLIENT_KEY):
    tls_runtime.restore_stdlib_ssl()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_verify_locations(cafile=cafile)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    return context


class SecureChatClient:
    def __init__(self, username, host=HOST, port=PORT, server_name="localhost",
                 context=None):
        validate_name(username)
        self.username = username
        self.encryption = MessageEncryption(os.urandom(32))
        self.send_lock = threading.Lock()
        self.sock = None
        context = context or create_context()
        raw_socket = socket.create_connection((host, port), timeout=10)
        try:
            self.sock = context.wrap_socket(raw_socket, server_hostname=server_name)
            hello = f"{username}:{self.encryption.key.hex()}".encode("utf-8")
            send_frame(self.sock, hello)
            self.welcome = self.receive()
            if self.welcome is None or not self.welcome.startswith("[SYSTEM] Connected as "):
                raise ConnectionError(self.welcome or "Server closed during registration")
            self.sock.settimeout(None)
        except BaseException:
            self.close()
            raw_socket.close()
            raise

    def send(self, message):
        if len(message.encode("utf-8")) > MAX_TEXT:
            raise ValueError("Message exceeds 16000 UTF-8 bytes")
        with self.send_lock:
            send_frame(self.sock, self.encryption.encrypt(message))

    def receive(self):
        packet = recv_frame(self.sock)
        return None if packet is None else self.encryption.decrypt(packet)

    def close(self):
        if self.sock is not None:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            self.sock.close()


def receive_messages(client, stopped):
    try:
        while not stopped.is_set():
            message = client.receive()
            if message is None:
                print("[!] Server disconnected. Press Enter to exit.", flush=True)
                break
            print(message, flush=True)
            if message == "[SYSTEM] Bye":
                break
    except (OSError, EOFError, ValueError) as exc:
        if not stopped.is_set():
            print(f"[!] Connection ended: {exc}. Press Enter to exit.", flush=True)
    finally:
        stopped.set()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--username", help="Skip the Username prompt")
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument("--server-name", default="localhost")
    parser.add_argument("--echo", action="store_true", help="Run the previous echo smoke test")
    args = parser.parse_args()
    username = args.username or ("echo_" + os.urandom(3).hex() if args.echo
                                 else input("Username: ").strip())
    context = create_context()
    print("[DEBUG] SSLContext class:", type(context), flush=True)
    client = SecureChatClient(username, args.host, args.port, args.server_name, context)
    stopped = threading.Event()
    receiver = None
    try:
        print("[+] Connected to server", flush=True)
        print(f"[+] TLS version: {client.sock.version()}", flush=True)
        print(f"[+] Cipher: {client.sock.cipher()}", flush=True)
        print("[+] Server certificate verified (CA + hostname)", flush=True)
        print(client.welcome, flush=True)
        if args.echo:
            client.send("/echo Xin chao tu SecureChat Client")
            response = client.receive()
            if response != "Server received: Xin chao tu SecureChat Client":
                raise ConnectionError(f"Unexpected echo: {response!r}")
            print("[<] Server: " + response, flush=True)
            return
        print("Type messages (type 'exit' to quit). /help lists commands.", flush=True)
        receiver = threading.Thread(target=receive_messages,
                                    args=(client, stopped), daemon=True)
        receiver.start()
        while not stopped.is_set():
            try:
                message = input()
            except EOFError:
                message = "exit"
            if stopped.is_set():
                break
            if not message.strip():
                continue
            try:
                client.send(message)
            except ValueError as exc:
                print(f"[ERROR] {exc}", flush=True)
                continue
            if message.lower() in ("exit", "/quit"):
                stopped.wait(2)
                break
    finally:
        stopped.set()
        client.close()
        if receiver is not None:
            receiver.join(timeout=2)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n[+] Client stopped")
    except (OSError, ValueError) as exc:
        raise SystemExit(f"Connection failed: {exc}")
