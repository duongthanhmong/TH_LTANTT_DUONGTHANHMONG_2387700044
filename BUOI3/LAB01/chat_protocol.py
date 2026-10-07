"""Length-prefixed messages: TCP/TLS recv() is not a message boundary."""
import re
import struct

MAX_FRAME = 65536
MAX_TEXT = 16000


def validate_name(name):
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9_.-]{1,32}", name):
        raise ValueError("Use 1-32 letters, digits, dots, underscores or hyphens")
    return name


def recv_exact(sock, size, allow_eof=False):
    data = bytearray()
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            if allow_eof and not data:
                return None
            raise EOFError("Connection closed in the middle of a frame")
        data.extend(chunk)
    return bytes(data)


def send_frame(sock, payload):
    if not 0 < len(payload) <= MAX_FRAME:
        raise ValueError("Invalid frame size")
    sock.sendall(struct.pack("!I", len(payload)) + payload)


def recv_frame(sock):
    header = recv_exact(sock, 4, allow_eof=True)
    if header is None:
        return None
    size = struct.unpack("!I", header)[0]
    if not 0 < size <= MAX_FRAME:
        raise ValueError("Invalid frame size")
    return recv_exact(sock, size)
