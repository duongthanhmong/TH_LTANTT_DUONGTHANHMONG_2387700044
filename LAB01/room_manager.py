"""One active room per client; snapshot recipients before network I/O."""
import threading


class RoomManager:
    def __init__(self):
        self.rooms = {"general": set()}
        self.lock = threading.Lock()

    def create_room(self, room_name):
        with self.lock:
            self.rooms.setdefault(room_name, set())

    def join_room(self, room_name, client_sock):
        with self.lock:
            for members in self.rooms.values():
                members.discard(client_sock)
            self.rooms.setdefault(room_name, set()).add(client_sock)
            self._remove_empty_rooms()

    def leave_room(self, room_name, client_sock):
        with self.lock:
            self.rooms.get(room_name, set()).discard(client_sock)
            self._remove_empty_rooms()

    def remove_client(self, client_sock):
        with self.lock:
            for members in self.rooms.values():
                members.discard(client_sock)
            self._remove_empty_rooms()

    def _remove_empty_rooms(self):
        for name in list(self.rooms):
            if name != "general" and not self.rooms[name]:
                del self.rooms[name]

    def members(self, room_name):
        with self.lock:
            return set(self.rooms.get(room_name, ()))

    def list_rooms(self):
        with self.lock:
            return {name: len(members) for name, members in sorted(self.rooms.items())}

    def broadcast_room(self, room_name, message, sender_sock, send_message):
        recipients = self.members(room_name)
        return sum(send_message(sock, message)
                   for sock in recipients if sock is not sender_sock)
