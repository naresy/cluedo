
import random
from game.cards import CHARACTER_CARDS, WEAPON_CARDS, ROOM_CARDS

def create_solution():
    murderer = random.choice(CHARACTER_CARDS)
    weapon = random.choice(WEAPON_CARDS)
    room = random.choice(ROOM_CARDS)
    return {"murderer": murderer, "weapon": weapon, "room": room}

def create_deck(solution):
    deck = [
        card for card in CHARACTER_CARDS if card != solution["murderer"]
    ] + [
        card for card in WEAPON_CARDS if card != solution["weapon"]
    ] + [
        card for card in ROOM_CARDS if card != solution["room"]
    ]
    random.shuffle(deck)
    return deck

def deal_cards(deck, num_players):
    hands = [[] for _ in range(num_players)]
    for i, card in enumerate(deck):
        hands[i % num_players].append(card)
    return hands
