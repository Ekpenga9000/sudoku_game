# Game Collection

A collection of interactive games built with Python and Flet.

## Games Included

### 🧩 Sudoku Game
A fully-featured Sudoku game with multiple difficulty levels.

#### Features
- **Multiple Difficulty Levels**: Easy (30 hints), Medium (18 hints), and Hard (10 hints)
- **Interactive GUI**: Clean and intuitive user interface
- **Real-time Validation**: Immediate feedback on moves
- **Mistake Tracking**: Limited mistakes to add challenge
- **Hint System**: Strategic hint usage with difficulty-based limits
- **Auto-solve**: View the complete solution
- **Visual Feedback**: Color-coded cells for correct/incorrect moves
- **Difficulty Lock**: Cannot change difficulty during active games

### 🌟 Maze Solver
An interactive maze solver that visualizes pathfinding algorithms.

#### Features
- **Algorithm Visualization**: Watch DFS and BFS algorithms in action
- **Random Maze Generation**: Generate new mazes using recursive backtracking
- **Speed Control**: Adjust visualization speed (1x to 10x)
- **Color-coded Visualization**:
  - Green: Start position
  - Red: End position
  - Black: Walls
  - Yellow: Currently exploring
  - Blue: Already visited
  - Purple: Solution path
- **Algorithm Comparison**: Switch between DFS and BFS to see the differences
- **Interactive Controls**: Generate, solve, and clear mazes easily

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
   ```bash
   pip install flet
   ```

## How to Run

### Option 1: Game Launcher (Recommended)
```bash
python launcher.py
```
Choose between Sudoku and Maze Solver from the launcher interface.

### Option 2: Run Games Directly
```bash
# Run Sudoku Game
python main.py

# Run Maze Solver
python maze_solver.py
```

## How to Play

### Sudoku Game
1. Click "New Game" to start a new puzzle
2. Select your preferred difficulty level
3. Click on empty cells and enter numbers (1-9)
4. Use hints strategically (limited by difficulty)
5. Complete the puzzle following Sudoku rules

### Maze Solver
1. Click "Generate Maze" to create a new random maze
2. Select algorithm: DFS (Depth-First Search) or BFS (Breadth-First Search)
3. Adjust speed using the slider
4. Click "Solve Maze" to watch the algorithm find the path
5. Use "Clear Path" to reset and try different algorithms

## Algorithm Differences

### DFS (Depth-First Search)
- Explores as far as possible along each branch before backtracking
- Uses a stack (LIFO - Last In, First Out)
- May not find the shortest path
- Generally uses less memory

### BFS (Breadth-First Search)
- Explores all neighbors at the current depth before moving deeper
- Uses a queue (FIFO - First In, First Out)
- Guarantees the shortest path in unweighted graphs
- Generally uses more memory

## Game Rules

### Sudoku
- Fill the 9×9 grid with digits 1-9
- Each row must contain all digits from 1-9
- Each column must contain all digits from 1-9
- Each 3×3 sub-grid must contain all digits from 1-9

### Maze Solver
- Find a path from the green start position to the red end position
- Cannot move through black walls
- Can only move in four directions (up, down, left, right)

## File Structure

- `launcher.py` - Game selection launcher
- `main.py` - Sudoku game with Flet UI
- `sudoku_solver.py` - Sudoku generation and solving logic
- `maze_solver.py` - Maze generator and pathfinding visualizer
- `requirements.txt` - Project dependencies
- `README.md` - This file

## Dependencies

- `flet` - Modern Python GUI framework
- `random` - For puzzle/maze generation (built-in)
- `asyncio` - For animation timing (built-in)
- `collections.deque` - For BFS queue (built-in)

Enjoy exploring algorithms and playing games! 🎮