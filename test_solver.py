"""
Test script for Sudoku solver functionality.
"""
from sudoku_solver import SudokuSolver


def test_sudoku_solver():
    """Test the basic functionality of the Sudoku solver."""
    solver = SudokuSolver()
    
    print("Testing Sudoku Solver...")
    
    # Test puzzle generation
    print("\n1. Generating puzzles for different difficulties:")
    for difficulty in ["easy", "medium", "hard"]:
        puzzle, solution = solver.generate_puzzle(difficulty)
        
        # Count empty cells
        empty_cells = sum(row.count(0) for row in puzzle)
        print(f"{difficulty.capitalize()}: {empty_cells} empty cells")
        
        # Verify solution
        if solver.check_solution(solution):
            print(f"{difficulty.capitalize()}: Solution is valid ✓")
        else:
            print(f"{difficulty.capitalize()}: Solution is invalid ✗")
    
    print("\n2. Testing validity checker:")
    # Create a simple test board
    test_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    
    # Test valid move
    if solver.is_valid(test_board, 0, 2, 4):
        print("Valid move test: ✓")
    else:
        print("Valid move test: ✗")
    
    # Test invalid move (duplicate in row)
    if not solver.is_valid(test_board, 0, 2, 5):  # 5 already exists in row 0
        print("Invalid move test (row): ✓")
    else:
        print("Invalid move test (row): ✗")
    
    print("\nAll tests completed!")


if __name__ == "__main__":
    test_sudoku_solver()