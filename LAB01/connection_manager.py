"""Per-client encryption and serialized writes for the textbook chat."""
import socket
import threading
from chat_protocol import send_frame
from message_encryption import MessageEncryption


class ConnectionManager:
    def __init__(self):
        self.clients = {}
        self.lock = threading.Lock()

    def add_client(self, client_sock, username, encryption_key):
        with self.lock:
            if any(info["username"].casefold() == username.casefold()
                   for info in self.clients.values()):
                raise ValueError("Username is already in use")
            info = {
                "username": username,
                "encryption_key": encryption_key,
                "encryption": MessageEncryption(encryption_key),
                "send_lock": threading.Lock(),
            }
            self.clients[client_sock] = info
            return info

    def remove_client(self, client_sock):
        with self.lock:
            self.clients.pop(client_sock, None)

    def get_client(self, client_sock):
        with self.lock:
            info = self.clients.get(client_sock)
            return dict(info) if info else None

    def usernames(self, members):
        with self.lock:
            return sorted(self.clients[s]["username"] for s in members
                          if s in self.clients)

    def send_message(self, client_sock, message):
        info = self.get_client(client_sock)
        if info is None:
            return False
        try:
            with info["send_lock"]:
                send_frame(client_sock, info["encryption"].encrypt(message))
            return True
        except (OSError, ValueError):
            # Wake the receiver so its finally block removes room membership.
            try:
                client_sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            return False

    def broadcast(self, message, sender_sock):
        with self.lock:
            recipients = list(self.clients)
        return sum(self.send_message(sock, message)
                   for sock in recipients if sock is not sender_sock)
