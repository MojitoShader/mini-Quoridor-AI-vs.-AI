# mini-Quoridor-AI-vs.-AI

**Mini Quoridor AI vs. AI**
This repository contains a compact implementation of the Quoridor board game, in which two autonomous agents compete by navigating their pawn to the opposite side while placing walls to impede their opponent.
Here a video of the two AI's playing: https://www.youtube.com/watch?v=kIrv7xb_VHA
---

## Objective

Each AI seeks to reach the far edge of a 5×5 grid in as few moves as possible. Both players begin with a limited number of walls (4 each). On their turn, an agent may either move its pawn one square (up/down/left/right) or place a wall—horizontal or vertical—to lengthen the opponent’s shortest path. The twist: after an initial random wall placement, the two AIs use identical logic to plan and react, ensuring a fair “mirror match.”

---

## Code Structure

* **Game.py**

  * Initializes the Pygame window and visualizes the board, pawns, walls and move log.
  * Manages the game loop, turn order and win condition.
  * Implements core rules:

    * `get_legal_moves()`: returns all valid pawn- and wall-moves for the active player.
    * `move_player()` and `place_wall()`: update pawn positions or wall placement, decrementing wall stock.
    * `extract_path()` / `reachable()`: a randomized depth-first procedure to test if a route to the goal exists.

* **P1.py & P2.py**

  * Define two AI classes (`Player1AI`, `Player2AI`) that share identical decision logic but mirror each other’s start/end rows.
  * **Path evaluation**

    * `pathLenght()`: a breadth-first search computes the minimum number of pawn-moves needed to reach the goal row, given current walls.
    * In `get_move()`, the AI runs 50 randomized trials of `extract_path()` to pick a concrete shortest move.
  * **Strategic wall placement**

    * `calculate_best_move()`: simulates each legal wall-move, measures how much it increases the opponent’s path relative to its own, and chooses the move with the highest net gain.
    * A recursive `evaluate_move()` (depth 3) anticipates the opponent’s best wall reply, embedding a simple minimax-style heuristic.

---

## How It Works

1. **Startup**

   * `Game.py` randomly places one wall, then alternates turns between P1 and P2.
2. **Agent Turn**

   * **Evaluate walls**: each AI considers all remaining walls, simulating their effect on both players’ path lengths and the opponent’s likely response.
   * **Decide**: if a wall yields a positive strategic benefit, it is placed; otherwise the AI advances its pawn along the (probable) shortest path.
3. **Termination**

   * The first pawn to reach its target row triggers a win; the game loop ends and the winner is logged.

---

## Usage

1. Install dependencies: `pip install pygame`
2. Run `python Game.py`
3. Watch the two AIs compete in real time.

Feel free to extend the look-ahead depth, tweak the wall-evaluation metric or replace the randomized path extractor with a purely deterministic BFS to experiment with different strategic behaviors.
