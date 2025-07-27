
class Weapon:
    def __init__(self, name: str):
        self.name = name
        self.location = None  # Will be updated when placed in a room

    def place_in_room(self, room_name: str):
        self.location = room_name

    def __str__(self):
        return f"{self.name} (in {self.location})" if self.location else self.name
