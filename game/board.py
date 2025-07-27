
from models.room import Room

class Board:
    def __init__(self):
        self.rooms = {}
        self.build_board()

    def build_board(self):
        # Define rooms
        room_names = [
            "Kitchen", "Ballroom", "Conservatory", "Dining Room",
            "Billiard Room", "Library", "Lounge", "Hall", "Study"
        ]

        # Initialize Room objects
        for name in room_names:
            self.rooms[name] = Room(name)

        # Connect adjacent rooms (simplified logic)
        self.rooms["Kitchen"].connect_room("Ballroom")
        self.rooms["Ballroom"].connect_room("Conservatory")
        self.rooms["Dining Room"].connect_room("Kitchen")
        self.rooms["Dining Room"].connect_room("Billiard Room")
        self.rooms["Library"].connect_room("Conservatory")
        self.rooms["Library"].connect_room("Billiard Room")
        self.rooms["Lounge"].connect_room("Dining Room")
        self.rooms["Hall"].connect_room("Lounge")
        self.rooms["Hall"].connect_room("Study")

        # Secret passages
        self.rooms["Study"].set_secret_passage("Kitchen")
        self.rooms["Kitchen"].set_secret_passage("Study")
        self.rooms["Conservatory"].set_secret_passage("Lounge")
        self.rooms["Lounge"].set_secret_passage("Conservatory")

    def get_room(self, room_name):
        return self.rooms.get(room_name)

    def get_secret_passage(self, room_name):
        room = self.get_room(room_name)
        return room.secret_passage if room else None

    def display_rooms(self):
        for room in self.rooms.values():
            print(room)
