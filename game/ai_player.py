import random
from game.player import Player

ROOM_POSITIONS = {
    "Kitchen": (0, 0),
    "Ballroom": (0, 6),
    "Conservatory": (0, 9),
    "Dining Room": (4, 0),
    "Lounge": (9, 0),
    "Hall": (6, 4),
    "Library": (6, 9),
    "Study": (9, 6),
    "Billiard Room": (9, 9)
}

CHARACTERS = ["Miss Scarlett", "Colonel Mustard", "Mrs. White", "Reverend Green", "Mrs. Peacock", "Professor Plum"]
WEAPONS = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope", "Wrench"]

class AIPlayer(Player):
    def __init__(self, name, character, cards):
        super().__init__(name, character, cards)
        self.knowledge = set(cards)
        self.visited_rooms = set()
        self.target_room = None

    def update_knowledge(self, card):
        self.knowledge.add(card)

    def decide_move_direction(self):
        if self.target_room is None or self.target_room in self.visited_rooms:
            unvisited = [r for r in ROOM_POSITIONS if r not in self.visited_rooms]
            self.target_room = random.choice(unvisited) if unvisited else random.choice(list(ROOM_POSITIONS))

        target_pos = ROOM_POSITIONS[self.target_room]
        my_x, my_y = self.position
        tx, ty = target_pos

        if abs(tx - my_x) > abs(ty - my_y):
            return "DOWN" if tx > my_x else "UP"
        elif ty != my_y:
            return "RIGHT" if ty > my_y else "LEFT"
        else:
            return random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

    def make_suggestion(self, room):
        self.visited_rooms.add(room)
        unknown_chars = [c for c in CHARACTERS if c not in self.knowledge]
        unknown_weapons = [w for w in WEAPONS if w not in self.knowledge]
        character = random.choice(unknown_chars or CHARACTERS)
        weapon = random.choice(unknown_weapons or WEAPONS)
        return {"character": character, "weapon": weapon, "room": room}

    def should_accuse(self):
        suspects = [c for c in CHARACTERS if c not in self.knowledge]
        weapons = [w for w in WEAPONS if w not in self.knowledge]
        rooms = [r for r in ROOM_POSITIONS if r not in self.knowledge]

        if len(suspects) == 1 and len(weapons) == 1 and len(rooms) == 1:
            return {"character": suspects[0], "weapon": weapons[0], "room": rooms[0]}
        return None
