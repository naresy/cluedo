import tkinter as tk
from game.board import CELL_SIZE, BOARD_SIZE

class BoardView(tk.Canvas):
    def __init__(self, root, game_engine, click_callback=None):
        super().__init__(root, width=CELL_SIZE*BOARD_SIZE, height=CELL_SIZE*BOARD_SIZE, bg="white")
        self.game = game_engine
        self.click_callback = click_callback
        self.bind("<Button-1>", self.on_click)
        self.draw_board()

    def draw_board(self):
        self.delete("all")
        # Draw rooms
        for room, data in self.game.board.rooms.items():
            x1, y1, x2, y2 = [c * CELL_SIZE for c in data["coords"]]
            self.create_rectangle(x1, y1, x2, y2, fill=data["color"], outline="black")
            self.create_text((x1+x2)//2, (y1+y2)//2, text=room, font=("Helvetica", 10, "bold"))

        # Grid lines
        for i in range(BOARD_SIZE):
            self.create_line(i*CELL_SIZE, 0, i*CELL_SIZE, CELL_SIZE*BOARD_SIZE, fill="gray")
            self.create_line(0, i*CELL_SIZE, CELL_SIZE*BOARD_SIZE, i*CELL_SIZE, fill="gray")

        self.draw_players()

    def draw_players(self):
        self.delete("player")
        colors = ["red", "blue", "green", "purple", "orange", "brown"]
        for idx, player in enumerate(self.game.players):
            if not player or not player.active:
                continue
            x, y = player.position
            px, py = x*CELL_SIZE + CELL_SIZE//2, y*CELL_SIZE + CELL_SIZE//2
            self.create_oval(px-15, py-15, px+15, py+15, fill=colors[idx], tags="player")
            self.create_text(px, py, text=player.character[0], fill="white", font=("Helvetica", 12, "bold"), tags="player")

    def set_valid_moves(self, moves):
        """Highlight the valid squares the player can move to."""
        self.delete("highlight")
        for x, y in moves:
            x1, y1 = x*CELL_SIZE, y*CELL_SIZE
            x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
            self.create_rectangle(x1, y1, x2, y2, outline="yellow", width=2, tags="highlight")

    def on_click(self, event):
        if not self.click_callback:
            return
        grid_x, grid_y = event.x // CELL_SIZE, event.y // CELL_SIZE
        self.click_callback(grid_x, grid_y)
