import tkinter as tk
from tkinter import ttk
import time
from gui.app import CluedoApp  # Your actual game GUI


# ---------------------------
# Splash Screen
# ---------------------------
class CluedoSplash:
    def __init__(self, root, on_finish):
        self.root = root
        self.on_finish = on_finish
        self.root.title("Cluedo - Loading...")
        self.root.geometry("800x600")
        self.root.configure(bg="#111")

        # Title
        self.title_label = tk.Label(
            root, text="🔍 CLUEDO",
            font=("Helvetica", 60, "bold"), fg="gold", bg="#111"
        )
        self.title_label.pack(pady=60)

        # Tagline
        self.tagline = tk.Label(
            root, text="Who? With What? Where?",
            font=("Helvetica", 22, "italic"), fg="white", bg="#111"
        )
        self.tagline.pack(pady=10)

        # Loading message
        self.loading_msg = tk.Label(
            root, text="Loading...", font=("Helvetica", 16),
            fg="lightgray", bg="#111"
        )
        self.loading_msg.pack(pady=40)

        # Progress Bar styling
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor="#333",
            background="#4CAF50",
            thickness=20
        )

        # Progress Bar
        self.progress = ttk.Progressbar(
            root, style="Custom.Horizontal.TProgressbar",
            orient="horizontal", length=500, mode="determinate"
        )
        self.progress.pack(pady=20)

        # Start animation
        self.animate_loading()

    def animate_loading(self):
        """Fake loading animation with detective-style messages"""
        messages = [
            "🔍 Gathering suspects...",
            "🪢 Collecting murder weapons...",
            "🏠 Inspecting rooms...",
            "📜 Shuffling evidence...",
            "🕵️ Starting investigation..."
        ]

        for i in range(101):
            self.progress['value'] = i
            if i % 20 == 0 and i // 20 < len(messages):
                self.loading_msg.config(text=messages[i // 20])
            self.root.update_idletasks()
            time.sleep(0.03)  # Controls speed of loading

        self.on_finish()


# ---------------------------
# Main Menu
# ---------------------------
class CluedoMainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Cluedo - Main Menu")
        self.root.geometry("800x600")
        self.root.configure(bg="#222")

        # Title
        self.title_label = tk.Label(
            root, text="🔍 CLUEDO",
            font=("Helvetica", 48, "bold"), fg="white", bg="#222"
        )
        self.title_label.pack(pady=40)

        # Subtitle
        self.subtitle = tk.Label(
            root, text="Who? With What? Where?",
            font=("Helvetica", 20), fg="lightgray", bg="#222"
        )
        self.subtitle.pack()

        # Play Button
        play_btn = tk.Button(
            root, text="▶ Play Game",
            font=("Helvetica", 20, "bold"),
            bg="#4CAF50", fg="white",
            command=self.start_game
        )
        play_btn.pack(pady=30)

        # How to Play Button
        how_btn = tk.Button(
            root, text="📖 How to Play",
            font=("Helvetica", 18),
            bg="#2196F3", fg="white",
            command=self.show_how_to_play
        )
        how_btn.pack(pady=10)

        # Exit Button
        exit_btn = tk.Button(
            root, text="❌ Exit",
            font=("Helvetica", 18),
            bg="#f44336", fg="white",
            command=root.quit
        )
        exit_btn.pack(pady=10)

    def start_game(self):
        """Clear the menu and launch the actual game"""
        for widget in self.root.winfo_children():
            widget.destroy()
        CluedoApp(self.root)  # Load your existing Cluedo game

    def show_how_to_play(self):
        """Popup with quick instructions"""
        instructions = (
            "🎯 Objective: Be the first to solve WHO, WHAT, WHERE.\n\n"
            "1. Roll dice to move.\n"
            "2. Enter rooms to make suggestions.\n"
            "3. Use clues to deduce the murderer.\n"
            "4. Make a final accusation to win!"
        )
        top = tk.Toplevel(self.root)
        top.title("How to Play")
        tk.Label(top, text=instructions, justify="left", padx=20, pady=20).pack()


# ---------------------------
# Menu Runner
# ---------------------------
def run_menu():
    root = tk.Tk()

    def show_menu():
        for widget in root.winfo_children():
            widget.destroy()
        CluedoMainMenu(root)

    # First show splash, then menu
    CluedoSplash(root, on_finish=show_menu)
    root.mainloop()
