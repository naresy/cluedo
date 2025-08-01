class Player:
    def __init__(self, name, character, cards):
        self.name = name
        self.character = character
        self.cards = cards
        self.position = (0, 0)
        self.active = True

    def set_position(self, pos):
        self.position = pos

    def move(self, direction, steps):
        pass  # Movement handled by GameEngine
