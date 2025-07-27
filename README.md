<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Cluedo Game - README</title>
</head>
<body>

<h1>🔍 Cluedo Game (Python + Tkinter)</h1>

<p>
  This is a turn-based digital implementation of the classic board game <strong>Cluedo (Clue)</strong>, built using Python and Tkinter. The game supports both human and AI players, turn rotation, suggestions, refutations, and final accusations.
</p>

<h2>🎯 Features</h2>
<ul>
  <li>2D grid-based board with real-time player movement</li>
  <li>Dropdown-based suggestion and accusation interface</li>
  <li>AI players with basic deduction logic</li>
  <li>Room entry logic (e.g., Kitchen)</li>
  <li>Player elimination and automatic win detection</li>
</ul>

<h2>📁 Project Structure</h2>
<pre>
Cluedo-/
├── main.py                  # Entry point to run the game
├── README.md                # This file
├── game/
│   ├── __init__.py
│   ├── engine.py            # Core game logic and turn handling
│   ├── player.py            # Human player class
│   ├── ai_player.py         # AI player class with basic logic
│   ├── deck.py              # Card generation, dealing, and solution creation
│   ├── board.py             # Static board size/config
│   ├── cards.py             # List of characters, weapons, and rooms
│   ├── rules.py             # Move validation rules
├── gui/
│   ├── app.py               # Main Tkinter GUI application
│   ├── board_view.py        # Grid board rendering and player drawing
</pre>

<h2>🧠 Game Rules Summary</h2>
<ul>
  <li>Players move by rolling a die (1-6)</li>
  <li>If a player enters a room, they may suggest a murder combination (character, weapon, room)</li>
  <li>Other players attempt to refute by showing a matching card</li>
  <li>Players may attempt a final accusation at any time</li>
  <li>Incorrect final accusation eliminates the player</li>
  <li>The last standing player or a correct accusation wins the game</li>
</ul>

<h2>🚀 How to Run</h2>

<ol>
  <li>Make sure you have Python 3.x installed</li>
  <li>Navigate to the project folder:</li>
  <pre><code>cd Cluedo-</code></pre>
  <li>Run the game using:</li>
  <pre><code>python main.py</code></pre>
</ol>

<h2>👥 Player Setup</h2>
<ul>
  <li>On start screen, enter 3–6 player names</li>
  <li>To make a player AI-controlled, prefix the name with <code>AI_</code> (e.g., <code>AI_Bob</code>)</li>
  <li>Remaining options like direction, character, and weapon selections will appear as dropdowns</li>
</ul>

<h2>📌 Notes</h2>
<ul>
  <li>Currently, only one room (Kitchen) is implemented. You can add more rooms and room entry logic via the board and engine.</li>
  <li>AI logic is basic and meant for simulation only. Feel free to expand it with smarter decision-making.</li>
  <li>Code is modular and beginner-friendly for further enhancements or academic use.</li>
</ul>


<h2>👨‍💻 Author</h2>
<p>Developed by Liz</p>

</body>
</html>
