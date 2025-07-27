import tkinter as tk

CELL_SIZE = 50
BOARD_SIZE = 10  # 10x10 grid

PLAYER_COLORS = ["red", "blue", "green", "purple", "orange", "brown"]

class BoardView(tk.Canvas):
    def __init__(self, root, game_engine):
        canvas_size = CELL_SIZE * BOARD_SIZE
        super().__init__(root, width=canvas_size, height=canvas_size, bg="white")
        self.game = game_engine
        self.draw_grid()
        self.draw_players()

    def draw_grid(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                x0 = j * CELL_SIZE
                y0 = i * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE
                self.create_rectangle(x0, y0, x1, y1, outline="gray")

    def draw_players(self):
        self.delete("player")
        for index, player in enumerate(self.game.players):
            if player is None or not getattr(player, "active", True):
                continue  # Skip eliminated players

            x, y = player.position
            color = PLAYER_COLORS[index % len(PLAYER_COLORS)]

            # Draw token (circle)
            self.create_oval(
                y * CELL_SIZE + 10, x * CELL_SIZE + 10,
                y * CELL_SIZE + 40, x * CELL_SIZE + 40,
                fill=color, tags="player"
            )

            # Display player name under the token
            self.create_text(
                y * CELL_SIZE + 25, x * CELL_SIZE + 45,
                text=player.name[:8],  # limit to 8 characters for fit
                font=("Helvetica", 9), tags="player"
            )
