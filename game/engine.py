import random
from game.board import Board
from game.cards import CHARACTER_CARDS, ROOM_CARDS, WEAPON_CARDS
from game.player import Player
from game.ai_player import AIPlayer

class GameEngine:
    def __init__(self, player_info):
        """
        player_info: list of tuples (name, character)
        """
        self.board = Board()
        self.solution = self.create_solution()
        self.deck = self.create_deck(self.solution)
        self.players = []
        self.current_turn = 0
        self.setup_players(player_info)
        self.active_moves = []  # for click-to-move
        self.visited_rooms = {p[0]: set() for p in player_info}

    # ------------------------
    # Game Setup
    # ------------------------
    def create_solution(self):
        return {
            "murderer": random.choice(CHARACTER_CARDS),
            "weapon": random.choice(WEAPON_CARDS),
            "room": random.choice(ROOM_CARDS)
        }

    def create_deck(self, solution):
        deck = [c for c in CHARACTER_CARDS if c != solution["murderer"]]
        deck += [w for w in WEAPON_CARDS if w != solution["weapon"]]
        deck += [r for r in ROOM_CARDS if r != solution["room"]]
        random.shuffle(deck)
        return deck

    def deal_cards(self, deck, num_players):
        hands = [[] for _ in range(num_players)]
        for idx, card in enumerate(deck):
            hands[idx % num_players].append(card)
        return hands

    def setup_players(self, player_info):
        hands = self.deal_cards(self.deck, len(player_info))
        for i, (name, character) in enumerate(player_info):
            is_ai = name.startswith("AI_")
            player_class = AIPlayer if is_ai else Player
            player = player_class(name, character, hands[i])
            player.set_position((i * 2, 0))  # spread start positions
            self.players.append(player)

    # ------------------------
    # Turn Logic
    # ------------------------
    def roll_dice(self):
        return random.randint(1, 6)

    def get_current_player(self):
        return self.players[self.current_turn]

    def next_turn(self):
        """Rotate to next active player."""
        for _ in range(len(self.players)):
            self.current_turn = (self.current_turn + 1) % len(self.players)
            p = self.players[self.current_turn]
            if p and p.active:
                return p
        return None

    # ------------------------
    # Movement Logic
    # ------------------------
    def get_valid_moves(self, player, steps):
        return self.board.get_walkable_tiles(player.position, steps)

    def move_player(self, player, position):
        player.set_position(position)
        room = self.board.get_room_name(position)
        if room:
            self.visited_rooms[player.name].add(room)
        return room

    # ------------------------
    # AI Movement
    # ------------------------
    def ai_choose_move(self, player, steps):
        """AI moves toward nearest unvisited room."""
        unseen_rooms = [r for r in ROOM_CARDS if r not in self.visited_rooms[player.name]]
        if not unseen_rooms:
            unseen_rooms = ROOM_CARDS[:]  # all visited, random pick

        # Pick a target room
        target_room = random.choice(unseen_rooms)
        coords = self.board.rooms[target_room]["coords"]
        tx, ty = (coords[0] + coords[2]) // 2, (coords[1] + coords[3]) // 2

        # Move closer
        px, py = player.position
        best_moves = self.get_valid_moves(player, steps)
        best_moves.sort(key=lambda m: abs(m[0] - tx) + abs(m[1] - ty))
        return best_moves[0] if best_moves else player.position

    # ------------------------
    # Suggestion & Refutation
    # ------------------------
    def make_suggestion(self, player, character, weapon, room):
        return {"character": character, "weapon": weapon, "room": room}

    def refute_suggestion(self, suggesting_player, character, weapon, room):
        total_players = len(self.players)
        current_index = self.players.index(suggesting_player)

        for i in range(1, total_players):
            idx = (current_index + i) % total_players
            refuter = self.players[idx]
            if not refuter or not refuter.active:
                continue

            matches = []
            if character in refuter.cards: matches.append(character)
            if weapon in refuter.cards: matches.append(weapon)
            if room in refuter.cards: matches.append(room)

            if matches:
                shown_card = random.choice(matches)
                if isinstance(suggesting_player, AIPlayer):
                    suggesting_player.update_knowledge(shown_card)
                return refuter.name, shown_card

        return None, None

    # ------------------------
    # Accusation
    # ------------------------
    def make_accusation(self, player, character, weapon, room):
        correct = (
            character == self.solution["murderer"] and
            weapon == self.solution["weapon"] and
            room == self.solution["room"]
        )
        if not correct:
            player.active = False
        return correct
