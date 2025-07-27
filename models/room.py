
class Room:
    def __init__(self, name: str):
        self.name = name
        self.connected_rooms = []  # List of adjacent room names
        self.secret_passage = None  

    def connect_room(self, room_name: str):
        if room_name not in self.connected_rooms:
            self.connected_rooms.append(room_name)

    def set_secret_passage(self, destination_room: str):
        self.secret_passage = destination_room

    def __str__(self):
        conn = ", ".join(self.connected_rooms)
        secret = f", Secret passage to {self.secret_passage}" if self.secret_passage else ""
        return f"Room: {self.name}, Connected to: {conn}{secret}"
