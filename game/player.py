
class Player:
    def __init__(self, name: str, character: str, cards: list):
        self.name = name
        self.character = character
        self.cards = cards
        self.position = None  # (x, y) coordinates on the board

    def set_position(self, position: tuple):
        self.position = position

    def move(self, direction: str, steps: int):
        if not self.position:
            raise ValueError("Position not set.")
        x, y = self.position
        if direction == "UP":
            self.position = (x - steps, y)
        elif direction == "DOWN":
            self.position = (x + steps, y)
        elif direction == "LEFT":
            self.position = (x, y - steps)
        elif direction == "RIGHT":
            self.position = (x, y + steps)
        else:
            raise ValueError("Invalid direction")

    def make_suggestion(self, character: str, weapon: str, room: str):
        return {
            "character": character,
            "weapon": weapon,
            "room": room
        }

    def __str__(self):
        return f"{self.name} playing as {self.character}, Cards: {self.cards}"
