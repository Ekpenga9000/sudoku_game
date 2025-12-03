# Sudoku Game

A fully-featured Sudoku game built with Python and Flet.

## Features

- **Multiple Difficulty Levels**: Easy, Medium, and Hard
- **Interactive GUI**: Clean and intuitive user interface
- **Real-time Validation**: Immediate feedback on moves
- **Mistake Tracking**: Limited mistakes to add challenge
- **Hint System**: Get help when stuck
- **Auto-solve**: View the complete solution
- **Visual Feedback**: Color-coded cells for correct/incorrect moves

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:
   ```bash
   pip install flet
   ```

## How to Run

```bash
python main.py
```

## How to Play

1. Click "New Game" to start a new puzzle
2. Select your preferred difficulty level
3. Click on empty cells and enter numbers (1-9)
4. Correct moves will be highlighted in green
5. Incorrect moves will be highlighted in red
6. You have a limited number of mistakes before game over
7. Use "Hint" to get help with a random cell
8. Use "Check Solution" to verify your complete puzzle
9. Use "Solve" to see the complete solution

## Game Rules

- Fill the 9×9 grid with digits 1-9
- Each row must contain all digits from 1-9
- Each column must contain all digits from 1-9
- Each 3×3 sub-grid must contain all digits from 1-9

## File Structure

- `main.py` - Main application with Flet UI
- `sudoku_solver.py` - Sudoku generation and solving logic
- `README.md` - This file

## Dependencies

- `flet` - Modern Python GUI framework
- `random` - For puzzle generation (built-in)

Enjoy playing Sudoku!