import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from gui.board_view import BoardView
from game.engine import GameEngine
from game.ai_player import AIPlayer
from game.cards import CHARACTER_CARDS, WEAPON_CARDS, ROOM_CARDS

class CluedoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cluedo Game")
        self.root.geometry("600x700")
        self.start_screen()

    def start_screen(self):
        self.clear_window()

        tk.Label(self.root, text="Enter 3–6 Player Names", font=("Helvetica", 14)).pack(pady=10)
        self.name_entries = []
        for _ in range(6):
            entry = tk.Entry(self.root, font=("Helvetica", 12))
            entry.pack(pady=2)
            self.name_entries.append(entry)

        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)

    def start_game(self):
        player_names = [e.get().strip() for e in self.name_entries if e.get().strip()]
        if not (3 <= len(player_names) <= 6):
            messagebox.showerror("Invalid", "Please enter 3 to 6 player names.")
            return

        player_info = []
        for i, name in enumerate(player_names):
            character = CHARACTER_CARDS[i % len(CHARACTER_CARDS)]
            player_info.append((name, character))

        self.game = GameEngine(player_info)
        self.current_player = self.game.players[0]

        self.clear_window()

        self.label = tk.Label(self.root, text=self.get_player_text(), font=("Helvetica", 14))
        self.label.pack(pady=10)

        self.dice_result = tk.StringVar(value="Roll the dice")
        self.dice_label = tk.Label(self.root, textvariable=self.dice_result, font=("Helvetica", 12))
        self.dice_label.pack()

        self.roll_button = tk.Button(self.root, text="🎲 Roll Dice", command=self.roll_dice)
        self.roll_button.pack(pady=5)

        self.board_view = BoardView(self.root, self.game)
        self.board_view.pack(pady=20)

        if isinstance(self.current_player, AIPlayer):
            self.root.after(1000, self.run_ai_turn)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def get_player_text(self):
        return f"Current: {self.current_player.name} ({self.current_player.character})"

    def roll_dice(self):
        if isinstance(self.current_player, AIPlayer):
            return

        roll = self.game.roll_dice()
        self.dice_result.set(f"🎲 You rolled a {roll}")
        self.move_prompt(roll)

    def move_prompt(self, steps):
        move_window = tk.Toplevel(self.root)
        move_window.title("Choose Direction")

        tk.Label(move_window, text=f"Move {steps} steps in which direction:").pack(pady=5)
        direction_var = tk.StringVar()
        direction_dropdown = ttk.Combobox(move_window, textvariable=direction_var)
        direction_dropdown['values'] = ["UP", "DOWN", "LEFT", "RIGHT"]
        direction_dropdown.pack(pady=5)

        def confirm():
            direction = direction_var.get()
            if self.game.move_current_player(direction, steps):
                self.board_view.draw_players()
                self.check_room_entry()
            else:
                messagebox.showerror("Invalid", "Move out of bounds or invalid.")
            move_window.destroy()
            self.end_turn()

        tk.Button(move_window, text="Confirm", command=confirm).pack(pady=5)

    def check_room_entry(self):
        pos = self.current_player.position
        if pos == (0, 0):
            room = "Kitchen"

            suggestion_window = tk.Toplevel(self.root)
            suggestion_window.title("Make a Suggestion")

            tk.Label(suggestion_window, text="Select Character:").pack()
            char_var = tk.StringVar()
            char_menu = ttk.Combobox(suggestion_window, textvariable=char_var)
            char_menu['values'] = CHARACTER_CARDS
            char_menu.pack()

            tk.Label(suggestion_window, text="Select Weapon:").pack()
            weapon_var = tk.StringVar()
            weapon_menu = ttk.Combobox(suggestion_window, textvariable=weapon_var)
            weapon_menu['values'] = WEAPON_CARDS
            weapon_menu.pack()

            def make_suggestion():
                character = char_var.get()
                weapon = weapon_var.get()
                if character and weapon:
                    messagebox.showinfo("Suggestion", f"{self.current_player.name} suggests {character} with the {weapon} in {room}")
                    refuter_name, shown_card = self.game.refute_suggestion(self.current_player, character, weapon, room)
                    if refuter_name:
                        messagebox.showinfo("Refuted", f"{refuter_name} showed {shown_card}")
                    else:
                        messagebox.showinfo("No Refutation", "No one could refute.")
                suggestion_window.destroy()
                self.ask_accusation(room)

            tk.Button(suggestion_window, text="Submit Suggestion", command=make_suggestion).pack(pady=5)

    def ask_accusation(self, room):
        if messagebox.askyesno("Final Accusation", "Would you like to make a final accusation?"):
            acc_window = tk.Toplevel(self.root)
            acc_window.title("Final Accusation")

            tk.Label(acc_window, text="Select Character:").pack()
            ac_char = tk.StringVar()
            ac_char_menu = ttk.Combobox(acc_window, textvariable=ac_char)
            ac_char_menu['values'] = CHARACTER_CARDS
            ac_char_menu.pack()

            tk.Label(acc_window, text="Select Weapon:").pack()
            ac_weapon = tk.StringVar()
            ac_weapon_menu = ttk.Combobox(acc_window, textvariable=ac_weapon)
            ac_weapon_menu['values'] = WEAPON_CARDS
            ac_weapon_menu.pack()

            tk.Label(acc_window, text="Select Room:").pack()
            ac_room = tk.StringVar(value=room)
            ac_room_menu = ttk.Combobox(acc_window, textvariable=ac_room)
            ac_room_menu['values'] = ROOM_CARDS
            ac_room_menu.pack()

            def submit_accusation():
                if self.game.make_accusation(self.current_player, ac_char.get(), ac_weapon.get(), ac_room.get()):
                    messagebox.showinfo("🎉 WINNER!", f"{self.current_player.name} won the game!")
                    self.root.quit()
                else:
                    messagebox.showwarning("Wrong!", f"{self.current_player.name} guessed wrong and is eliminated.")
                    self.game.eliminate_current_player()
                    self.board_view.draw_players()
                acc_window.destroy()

            tk.Button(acc_window, text="Submit Accusation", command=submit_accusation).pack(pady=5)

    def run_ai_turn(self):
        if not isinstance(self.current_player, AIPlayer):
            return

        roll = self.game.roll_dice()
        direction = self.current_player.decide_move_direction()
        self.game.move_current_player(direction, roll)
        self.board_view.draw_players()

        if self.current_player.position == (0, 0):
            suggestion = self.current_player.make_suggestion("Kitchen")
            messagebox.showinfo("AI Suggestion", f"{self.current_player.name} suggests {suggestion['character']} with the {suggestion['weapon']} in Kitchen")
            refuter, card = self.game.refute_suggestion(self.current_player, suggestion["character"], suggestion["weapon"], "Kitchen")
            if card:
                self.current_player.update_knowledge(card)

            final_guess = self.current_player.should_accuse()
            if final_guess:
                if self.game.make_accusation(self.current_player, final_guess["character"], final_guess["weapon"], final_guess["room"]):
                    messagebox.showinfo("🎉 WINNER!", f"{self.current_player.name} made the correct accusation and won!")
                    self.root.quit()
                else:
                    messagebox.showwarning("Wrong!", f"{self.current_player.name} guessed wrong and is eliminated.")
                    self.game.eliminate_current_player()
                    self.board_view.draw_players()

        self.end_turn()

    def end_turn(self):
        active_players = [p for p in self.game.players if p and getattr(p, "active", True)]

        if len(active_players) == 1:
            winner = active_players[0]
            messagebox.showinfo("🎉 Game Over", f"{winner.name} is the last standing and wins the game!")
            self.root.quit()
            return

        next_player = self.game.next_turn()
        while next_player and not getattr(next_player, "active", True):
            next_player = self.game.next_turn()

        if not next_player:
            messagebox.showinfo("Game Over", "All players eliminated. No winner.")
            self.root.quit()
            return

        self.current_player = next_player
        self.label.config(text=self.get_player_text())
        self.board_view.draw_players()

        if isinstance(self.current_player, AIPlayer):
            self.root.after(1000, self.run_ai_turn)

def run_gui():
    root = tk.Tk()
    app = CluedoApp(root)
    root.mainloop()
