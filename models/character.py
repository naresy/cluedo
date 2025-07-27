

class Character:
    def __init__(self, name: str, starting_position: tuple):
        self.name = name
        self.position = starting_position  # (x, y) coordinates on the board

    def move_to(self, new_position: tuple):
        self.position = new_position

    def __str__(self):
        return f"{self.name} at {self.position}"
