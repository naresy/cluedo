# game/board.py
CELL_SIZE = 50
BOARD_SIZE = 25  # larger so rooms have space

ROOMS = {
    "Kitchen": {"color": "#a8d5a2", "coords": (0, 0, 5, 5)},
    "Ballroom": {"color": "#d5e1a3", "coords": (6, 0, 11, 5)},
    "Conservatory": {"color": "#8fd3c3", "coords": (12, 0, 17, 5)},
    "Dining Room": {"color": "#f6b26b", "coords": (0, 6, 5, 11)},
    "Billiard Room": {"color": "#76a5af", "coords": (12, 6, 17, 11)},
    "Library": {"color": "#6fa8dc", "coords": (18, 6, 23, 11)},
    "Lounge": {"color": "#e06666", "coords": (0, 12, 5, 17)},
    "Hall": {"color": "#ffd966", "coords": (6, 12, 11, 17)},
    "Study": {"color": "#b45f06", "coords": (18, 12, 23, 17)}
}

SECRET_PASSAGES = {
    "Kitchen": "Study",
    "Study": "Kitchen",
    "Conservatory": "Lounge",
    "Lounge": "Conservatory"
}

class Board:
    def __init__(self):
        self.rooms = ROOMS
        self.secret_passages = SECRET_PASSAGES

    def get_room_name(self, position):
        """Return room name if position is inside a room rectangle."""
        px, py = position
        for room, data in self.rooms.items():
            x1, y1, x2, y2 = data["coords"]
            if x1 <= px <= x2 and y1 <= py <= y2:
                return room
        return None

    def get_secret_passage(self, room_name):
        return self.secret_passages.get(room_name, None)

    def is_walkable(self, position):
        """We allow walking anywhere for now (no walls implemented)."""
        px, py = position
        return 0 <= px < BOARD_SIZE and 0 <= py < BOARD_SIZE

    def get_walkable_tiles(self, start, steps):
        """Simple movement: Manhattan distance within steps."""
        walkable = []
        sx, sy = start
        for dx in range(-steps, steps+1):
            for dy in range(-steps, steps+1):
                if abs(dx) + abs(dy) <= steps:
                    tx, ty = sx+dx, sy+dy
                    if self.is_walkable((tx, ty)):
                        walkable.append((tx, ty))
        return walkable
