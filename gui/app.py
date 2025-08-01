import tkinter as tk
from tkinter import messagebox, ttk
from gui.board_view import BoardView
from game.engine import GameEngine
from game.cards import CHARACTER_CARDS, WEAPON_CARDS, ROOM_CARDS
from game.ai_player import AIPlayer

class CluedoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cluedo Game")
        self.root.geometry("900x900")

        self.game = None
        self.current_player = None
        self.valid_moves = []
        self.steps_left = 0

        self.start_screen()

    # -------------------------
    # Start Menu
    # -------------------------
    def start_screen(self):
        for w in self.root.winfo_children():
            w.destroy()

        tk.Label(self.root, text="Enter 3–6 Player Names", font=("Helvetica", 16)).pack(pady=10)
        self.name_entries = []
        for _ in range(6):
            e = tk.Entry(self.root, font=("Helvetica", 14))
            e.pack(pady=3)
            self.name_entries.append(e)

        tk.Button(self.root, text="Start Game", font=("Helvetica", 14), command=self.start_game).pack(pady=20)

    def start_game(self):
        player_names = [e.get().strip() for e in self.name_entries if e.get().strip()]
        if not (3 <= len(player_names) <= 6):
            messagebox.showerror("Error", "Please enter between 3 and 6 names.")
            return

        # Assign characters automatically
        player_info = []
        for i, name in enumerate(player_names):
            player_info.append((name, CHARACTER_CARDS[i]))

        self.game = GameEngine(player_info)
        self.current_player = self.game.get_current_player()

        self.setup_board()

    # -------------------------
    # Board UI
    # -------------------------
    def setup_board(self):
        for w in self.root.winfo_children():
            w.destroy()

        self.info_label = tk.Label(self.root, text=self.get_player_text(), font=("Helvetica", 14))
        self.info_label.pack(pady=5)

        self.roll_label = tk.Label(self.root, text="Roll the dice", font=("Helvetica", 12))
        self.roll_label.pack()

        self.roll_button = tk.Button(self.root, text="🎲 Roll Dice", font=("Helvetica", 14), command=self.roll_dice)
        self.roll_button.pack(pady=5)

        self.board_view = BoardView(self.root, self.game, click_callback=self.handle_board_click)
        self.board_view.pack(pady=10)

    def get_player_text(self):
        return f"Current: {self.current_player.name} ({self.current_player.character})"

    # -------------------------
    # Player Turn
    # -------------------------
    def roll_dice(self):
        if isinstance(self.current_player, AIPlayer):
            return

        self.steps_left = self.game.roll_dice()
        self.roll_label.config(text=f"You rolled a {self.steps_left}")

        self.valid_moves = self.game.get_valid_moves(self.current_player, self.steps_left)
        self.board_view.set_valid_moves(self.valid_moves)

    def handle_board_click(self, x, y):
        if isinstance(self.current_player, AIPlayer):
            return

        if (x, y) in self.valid_moves:
            room = self.game.move_player(self.current_player, (x, y))
            self.board_view.draw_players()

            if room:
                self.prompt_suggestion(room)
            else:
                self.end_turn()

    # -------------------------
    # Suggestion & Accusation
    # -------------------------
    def prompt_suggestion(self, room):
        win = tk.Toplevel(self.root)
        win.title("Make a Suggestion")

        tk.Label(win, text=f"You are in {room}", font=("Helvetica", 14)).pack(pady=5)

        tk.Label(win, text="Character:").pack()
        char_var = tk.StringVar()
        char_menu = ttk.Combobox(win, textvariable=char_var, values=CHARACTER_CARDS)
        char_menu.pack()

        tk.Label(win, text="Weapon:").pack()
        weapon_var = tk.StringVar()
        weapon_menu = ttk.Combobox(win, textvariable=weapon_var, values=WEAPON_CARDS)
        weapon_menu.pack()

        def submit():
            suggestion = self.game.make_suggestion(self.current_player, char_var.get(), weapon_var.get(), room)
            refuter, card = self.game.refute_suggestion(self.current_player, **suggestion)
            if refuter:
                messagebox.showinfo("Refuted", f"{refuter} showed you {card}")
            else:
                messagebox.showinfo("No Refutation", "No one could refute your suggestion.")
            win.destroy()
            self.prompt_accusation(room)

        tk.Button(win, text="Submit", command=submit).pack(pady=5)

    def prompt_accusation(self, room):
        if not messagebox.askyesno("Accusation", "Do you want to make a final accusation?"):
            self.end_turn()
            return

        win = tk.Toplevel(self.root)
        win.title("Final Accusation")

        tk.Label(win, text="Character:").pack()
        char_var = tk.StringVar()
        char_menu = ttk.Combobox(win, textvariable=char_var, values=CHARACTER_CARDS)
        char_menu.pack()

        tk.Label(win, text="Weapon:").pack()
        weapon_var = tk.StringVar()
        weapon_menu = ttk.Combobox(win, textvariable=weapon_var, values=WEAPON_CARDS)
        weapon_menu.pack()

        tk.Label(win, text="Room:").pack()
        room_var = tk.StringVar(value=room)
        room_menu = ttk.Combobox(win, textvariable=room_var, values=ROOM_CARDS)
        room_menu.pack()

        def submit_accusation():
            correct = self.game.make_accusation(self.current_player, char_var.get(), weapon_var.get(), room_var.get())
            if correct:
                messagebox.showinfo("Winner", f"{self.current_player.name} wins!")
                self.root.quit()
            else:
                messagebox.showwarning("Wrong!", f"{self.current_player.name} is eliminated.")
                self.board_view.draw_players()
                self.end_turn()
            win.destroy()

        tk.Button(win, text="Submit Accusation", command=submit_accusation).pack(pady=5)

    # -------------------------
    # AI Turn
    # -------------------------
    def run_ai_turn(self):
        if not isinstance(self.current_player, AIPlayer):
            return

        steps = self.game.roll_dice()
        move_choice = self.game.ai_choose_move(self.current_player, steps)
        room = self.game.move_player(self.current_player, move_choice)
        self.board_view.draw_players()

        if room:
            suggestion = self.current_player.make_suggestion(room)
            refuter, card = self.game.refute_suggestion(self.current_player, **suggestion)
            if card:
                self.current_player.update_knowledge(card)
            if self.current_player.should_accuse():
                if self.game.make_accusation(self.current_player, **self.current_player.should_accuse()):
                    messagebox.showinfo("Winner", f"{self.current_player.name} wins!")
                    self.root.quit()

        self.end_turn()

    # -------------------------
    # Turn Management
    # -------------------------
    def end_turn(self):
        next_p = self.game.next_turn()
        if not next_p:
            messagebox.showinfo("Game Over", "No winner. All players eliminated.")
            self.root.quit()
            return

        self.current_player = next_p
        self.info_label.config(text=self.get_player_text())
        self.roll_label.config(text="Roll the dice")
        self.valid_moves.clear()
        self.board_view.set_valid_moves([])

        if isinstance(self.current_player, AIPlayer):
            self.root.after(1000, self.run_ai_turn)

def run_gui():
    root = tk.Tk()
    app = CluedoApp(root)
    root.mainloop()
