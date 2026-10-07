"""SecureChat: mTLS, textbook AES-CBC messages, and multiple chat rooms."""
import argparse
import socket
import ssl
import threading
from pathlib import Path

import tls_runtime  # Restore stdlib SSL before creating contexts.
from chat_protocol import MAX_TEXT, recv_frame, send_frame, validate_name
from connection_manager import ConnectionManager
from message_encryption import MessageEncryption
from room_manager import RoomManager

HOST = "127.0.0.1"
PORT = 8443
BASE_DIR = Path(__file__).resolve().parent
CA_CERT = BASE_DIR / "certs/ca/ca.crt"
SERVER_CERT = BASE_DIR / "certs/server/server.crt"
SERVER_KEY = BASE_DIR / "certs/server/server.key"

connection_manager = ConnectionManager()
room_manager = RoomManager()
HELP = ("/join ROOM | /rooms | /users | /help | /quit (or exit). "
        "Plain text is sent to the other clients in your room.")


def create_context():
    tls_runtime.restore_stdlib_ssl()
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(SERVER_CERT, SERVER_KEY)
    context.load_verify_locations(cafile=CA_CERT)
    context.verify_mode = ssl.CERT_REQUIRED
    return context


def handle_client(conn, addr):
    registered = False
    username = None
    encryption = None
    current_room = "general"
    try:
        certificate = conn.getpeercert()
        if not certificate:
            raise ssl.SSLError("Client certificate required")
        subject = dict(part for rdn in certificate["subject"] for part in rdn)
        print(f"[+] Client certificate received: CN={subject.get('commonName')}", flush=True)
        print(f"[+] TLS version: {conn.version()} | Client: {addr}", flush=True)

        # The random AES key is exchanged only inside the verified mTLS channel.
        data = recv_frame(conn)
        if data is None:
            return
        username, key_hex = data.decode("utf-8").split(":", 1)
        validate_name(username)
        key = bytes.fromhex(key_hex)
        if len(key) != 32:
            raise ValueError("Expected a 256-bit AES key")
        encryption = MessageEncryption(key)
        info = connection_manager.add_client(conn, username, key)
        registered = True
        # Send the welcome before another thread can send room messages.
        with info["send_lock"]:
            room_manager.join_room(current_room, conn)
            send_frame(conn, encryption.encrypt(
                f"[SYSTEM] Connected as {username}; room=general. {HELP}"))
        conn.settimeout(None)
        print(f"[+] {username} joined general", flush=True)

        while True:
            packet = recv_frame(conn)
            if packet is None:
                break
            message = encryption.decrypt(packet)
            if len(message.encode("utf-8")) > MAX_TEXT:
                connection_manager.send_message(conn, "[ERROR] Message exceeds 16000 UTF-8 bytes")
                continue
            if not message.strip():
                continue
            command, _, argument = message.partition(" ")
            if message.lower() in ("exit", "/quit"):
                connection_manager.send_message(conn, "[SYSTEM] Bye")
                break
            if command == "/join":
                try:
                    destination = validate_name(argument.strip())
                except ValueError as exc:
                    connection_manager.send_message(conn, f"[ERROR] {exc}")
                    continue
                with info["send_lock"]:
                    room_manager.join_room(destination, conn)
                    current_room = destination
                    send_frame(conn, encryption.encrypt(f"[SYSTEM] Joined room {current_room}"))
                print(f"[+] {username} joined {current_room}", flush=True)
            elif command == "/rooms":
                rooms = ", ".join(f"{name} ({count})"
                                  for name, count in room_manager.list_rooms().items())
                connection_manager.send_message(conn, f"[SYSTEM] Rooms: {rooms}")
            elif command == "/users":
                names = connection_manager.usernames(room_manager.members(current_room))
                connection_manager.send_message(conn, f"[SYSTEM] Users in {current_room}: {', '.join(names)}")
            elif command == "/help":
                connection_manager.send_message(conn, "[SYSTEM] " + HELP)
            elif command == "/echo":
                connection_manager.send_message(conn, f"Server received: {argument}")
            elif command.startswith("/"):
                connection_manager.send_message(conn, "[ERROR] Unknown command. Use /help")
            else:
                print(f"[{current_room}] [{username}]: {message}", flush=True)
                delivered = room_manager.broadcast_room(
                    current_room, f"[{username}]: {message}", conn,
                    connection_manager.send_message)
                if delivered == 0:
                    connection_manager.send_message(
                        conn, "[SYSTEM] No other client in this room. Open a second client.")
    except (OSError, EOFError, ValueError) as exc:
        print(f"[-] Client error from {addr}: {type(exc).__name__}: {exc}", flush=True)
        if encryption is not None and not registered:
            try:
                send_frame(conn, encryption.encrypt(f"[ERROR] {exc}"))
            except OSError:
                pass
    finally:
        room_manager.remove_client(conn)
        if registered:
            connection_manager.remove_client(conn)
        try:
            conn.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        conn.close()
        print(f"[-] Client disconnected: {username or addr}", flush=True)


def accept_client(raw_socket, addr, context):
    try:
        raw_socket.settimeout(10)
        conn = context.wrap_socket(raw_socket, server_side=True)
    except (OSError, ValueError) as exc:
        print(f"[-] TLS handshake failed from {addr}: {exc}", flush=True)
        raw_socket.close()
        return
    handle_client(conn, addr)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default=HOST)
    parser.add_argument("--port", type=int, default=PORT)
    args = parser.parse_args()
    context = create_context()
    print("[DEBUG] SSLContext class:", type(context), flush=True)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        option = getattr(socket, "SO_EXCLUSIVEADDRUSE", socket.SO_REUSEADDR)
        listener.setsockopt(socket.SOL_SOCKET, option, 1)
        listener.bind((args.host, args.port))
        listener.listen(16)
        print("SecureChat TLS Server | mTLS CERT_REQUIRED | AES-256-CBC inside TLS", flush=True)
        print(f"[+] Listening on {args.host}:{listener.getsockname()[1]}", flush=True)
        print("[+] Waiting for clients...", flush=True)
        while True:
            raw_socket, addr = listener.accept()
            threading.Thread(target=accept_client,
                             args=(raw_socket, addr, context), daemon=True).start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[+] Server stopped")
    except OSError as exc:
        raise SystemExit(f"Cannot start server: {exc}. Stop the old server or choose --port.")
