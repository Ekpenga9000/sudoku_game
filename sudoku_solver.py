"""
Sudoku solver and generator module.
"""
import random
from typing import List, Tuple, Optional


class SudokuSolver:
    """Class to handle Sudoku solving and generation logic."""
    
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
    
    def is_valid(self, board: List[List[int]], row: int, col: int, num: int) -> bool:
        """Check if placing num at (row, col) is valid."""
        # Check row
        for x in range(9):
            if board[row][x] == num:
                return False
        
        # Check column
        for x in range(9):
            if board[x][col] == num:
                return False
        
        # Check 3x3 box
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
        
        return True
    
    def solve_sudoku(self, board: List[List[int]]) -> bool:
        """Solve Sudoku using backtracking."""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, i, j, num):
                            board[i][j] = num
                            if self.solve_sudoku(board):
                                return True
                            board[i][j] = 0
                    return False
        return True
    
    def generate_complete_board(self) -> List[List[int]]:
        """Generate a complete valid Sudoku board."""
        board = [[0 for _ in range(9)] for _ in range(9)]
        
        # Fill the diagonal 3x3 boxes first
        for box in range(0, 9, 3):
            self._fill_box(board, box, box)
        
        # Solve the rest
        self.solve_sudoku(board)
        return board
    
    def _fill_box(self, board: List[List[int]], row: int, col: int):
        """Fill a 3x3 box with random valid numbers."""
        nums = list(range(1, 10))
        random.shuffle(nums)
        
        for i in range(3):
            for j in range(3):
                board[row + i][col + j] = nums[i * 3 + j]
    
    def generate_puzzle(self, difficulty: str = "medium") -> Tuple[List[List[int]], List[List[int]]]:
        """Generate a Sudoku puzzle with given difficulty."""
        # Generate complete board
        complete_board = self.generate_complete_board()
        puzzle_board = [row[:] for row in complete_board]  # Deep copy
        
        # Remove numbers based on difficulty
        difficulty_map = {
            "easy": 40,
            "medium": 50,
            "hard": 60
        }
        
        cells_to_remove = difficulty_map.get(difficulty, 50)
        
        # Randomly remove cells
        removed = 0
        while removed < cells_to_remove:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if puzzle_board[row][col] != 0:
                puzzle_board[row][col] = 0
                removed += 1
        
        return puzzle_board, complete_board
    
    def check_solution(self, board: List[List[int]]) -> bool:
        """Check if the current board state is a valid complete solution."""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return False
                # Temporarily remove the number to check validity
                temp = board[i][j]
                board[i][j] = 0
                if not self.is_valid(board, i, j, temp):
                    board[i][j] = temp
                    return False
                board[i][j] = temp
        return True