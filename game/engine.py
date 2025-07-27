import random
from game.deck import create_solution, create_deck, deal_cards
from game.board import Board
from game.cards import CHARACTER_CARDS
from game.player import Player
from game.ai_player import AIPlayer
from game.rules import validate_move, is_valid_direction

class GameEngine:
    def __init__(self, player_info):  # expects list of (name, character)
        self.board = Board()
        self.solution = create_solution()
        self.deck = create_deck(self.solution)
        self.players = []
        self.current_turn = 0
        self.setup_players(player_info)

    def setup_players(self, player_info):
        hands = deal_cards(self.deck, len(player_info))
        for i, (name, character) in enumerate(player_info):
            is_ai = name.startswith("AI_")
            player = AIPlayer(name, character, hands[i]) if is_ai else Player(name, character, hands[i])
            player.set_position((0, i * 2))
            player.active = True
            self.players.append(player)

    def roll_dice(self):
        return random.randint(1, 6)

    def next_turn(self):
        if self.all_players_eliminated():
            return None
        for _ in range(len(self.players)):
            self.current_turn = (self.current_turn + 1) % len(self.players)
            player = self.players[self.current_turn]
            if player and getattr(player, 'active', True):
                return player
        return None

    def move_current_player(self, direction, steps):
        player = self.players[self.current_turn]
        if not is_valid_direction(direction):
            return False
        if validate_move(player.position, direction, steps, board_size=10):
            player.move(direction, steps)
            return True
        return False

    def handle_suggestion(self, player, room_name):
        suggestion = player.make_suggestion(room_name)
        print(f"{player.name} suggests: {suggestion}")
        return suggestion

    def make_accusation(self, player, character, weapon, room):
        correct = (
            character == self.solution["murderer"] and
            weapon == self.solution["weapon"] and
            room == self.solution["room"]
        )
        return correct

    def eliminate_current_player(self):
        self.players[self.current_turn].active = False

    def all_players_eliminated(self):
        return all(p is None or not getattr(p, 'active', True) for p in self.players)

    def refute_suggestion(self, suggesting_player, character, weapon, room):
        total_players = len(self.players)
        current_index = self.players.index(suggesting_player)

        for i in range(1, total_players):
            idx = (current_index + i) % total_players
            player = self.players[idx]
            if player is None or not getattr(player, 'active', True):
                continue

            matches = []
            if character in player.cards:
                matches.append(character)
            if weapon in player.cards:
                matches.append(weapon)
            if room in player.cards:
                matches.append(room)

            if matches:
                card = random.choice(matches)
                if isinstance(suggesting_player, AIPlayer):
                    suggesting_player.update_knowledge(card)
                return player.name, card

        return None, None

    def start_game(self):
        print("🎲 Starting Cluedo...")
        print("Solution is hidden.")
        for _ in range(10):
            self.run_turn()

    def run_turn(self):
        player = self.players[self.current_turn]
        if not player or not getattr(player, 'active', True):
            return

        print(f"\n{player.name}'s turn ({player.character})")
        roll = self.roll_dice()
        print(f"Rolled: {roll}")

        if isinstance(player, AIPlayer):
            direction = player.decide_move_direction()
            moved = self.move_current_player(direction, roll)
            print(f"{player.name} moves {direction} → {moved}")
            if moved and player.position == (0, 0):
                suggestion = self.handle_suggestion(player, "Kitchen")
                refuter, shown_card = self.refute_suggestion(player, suggestion["character"], suggestion["weapon"], suggestion["room"])
                if refuter:
                    print(f"Refuted by {refuter}: {shown_card}")
                else:
                    print("No one could refute.")
                final = player.should_accuse()
                if final:
                    if self.make_accusation(player, final["character"], final["weapon"], final["room"]):
                        print(f"🎉 {player.name} wins!")
                        exit()
                    else:
                        print(f"{player.name} guessed wrong and is eliminated.")
                        self.eliminate_current_player()
        else:
            input("Press Enter to roll dice...")
            direction = input("Direction (UP/DOWN/LEFT/RIGHT): ").upper()
            moved = self.move_current_player(direction, roll)
            if moved:
                print(f"{player.name} moved to {player.position}")
                if player.position == (0, 0):
                    self.handle_suggestion(player, "Kitchen")

        self.next_turn()
