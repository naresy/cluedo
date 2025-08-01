import random
from game.player import Player
from game.cards import ROOM_CARDS, CHARACTER_CARDS, WEAPON_CARDS

class AIPlayer(Player):
    def __init__(self, name, character, cards):
        super().__init__(name, character, cards)
        self.seen_cards = set()

        # Track possible solutions for deduction
        self.possible_solutions = {
            "character": set(CHARACTER_CARDS),
            "weapon": set(WEAPON_CARDS),
            "room": set(ROOM_CARDS)
        }

    def choose_target_room(self):
        """Pick a room AI hasn't ruled out yet."""
        unseen_rooms = [r for r in ROOM_CARDS if r not in self.seen_cards]
        return random.choice(unseen_rooms) if unseen_rooms else random.choice(ROOM_CARDS)

    def make_suggestion(self, room):
        """Pick best guess based on unseen cards."""
        char = random.choice(list(self.possible_solutions["character"]))
        weapon = random.choice(list(self.possible_solutions["weapon"]))
        return {"character": char, "weapon": weapon, "room": room}

    def should_accuse(self):
        """Accuse if only one possibility remains in each category."""
        if (len(self.possible_solutions["character"]) == 1 and
            len(self.possible_solutions["weapon"]) == 1 and
            len(self.possible_solutions["room"]) == 1):
            return {
                "character": next(iter(self.possible_solutions["character"])),
                "weapon": next(iter(self.possible_solutions["weapon"])),
                "room": next(iter(self.possible_solutions["room"]))
            }
        return None

    def update_knowledge(self, card):
        """Remove seen card from possible solutions."""
        self.seen_cards.add(card)
        for key in self.possible_solutions:
            self.possible_solutions[key].discard(card)
