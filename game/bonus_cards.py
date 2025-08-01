import random

BONUS_CARDS = [
    {"name": "Extra Move", "type": "play_now", "effect": "Roll again and move."},
    {"name": "Free Suggestion", "type": "play_now", "effect": "Make a suggestion immediately."},
    {"name": "Secret Passage", "type": "play_now", "effect": "Move to any room instantly."},
    {"name": "Block Suggestion", "type": "keep", "effect": "Cancel another player's suggestion once."},
    {"name": "See Card", "type": "keep", "effect": "Force any player to show you one card."},
]

def draw_bonus_card():
    """Return a random bonus card."""
    return random.choice(BONUS_CARDS)
