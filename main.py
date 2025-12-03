"""
Main Sudoku game application using Flet.
"""
import flet as ft
from typing import List, Optional
from sudoku_solver import SudokuSolver


class SudokuGame:
    """Main Sudoku game class with Flet UI."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.solver = SudokuSolver()
        self.puzzle_board: List[List[int]] = []
        self.solution_board: List[List[int]] = []
        self.initial_board: List[List[int]] = []  # To track which cells are editable
        self.board_controls: List[List[ft.TextField]] = []
        self.difficulty = "medium"
        self.mistakes = 0
        self.max_mistakes = 3
        
        # UI Components
        self.title = ft.Text(
            "Sudoku Game",
            size=32,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )
        
        self.difficulty_dropdown = ft.Dropdown(
            width=150,
            options=[
                ft.dropdown.Option("easy", "Easy"),
                ft.dropdown.Option("medium", "Medium"),
                ft.dropdown.Option("hard", "Hard"),
            ],
            value="medium",
            on_change=self.difficulty_changed
        )
        
        self.mistakes_text = ft.Text(
            f"Mistakes: {self.mistakes}/{self.max_mistakes}",
            size=16,
            color=ft.Colors.RED_400
        )
        
        self.new_game_btn = ft.ElevatedButton(
            "New Game",
            on_click=self.new_game,
            bgcolor=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE
        )
        
        self.check_solution_btn = ft.ElevatedButton(
            "Check Solution",
            on_click=self.check_solution,
            bgcolor=ft.Colors.GREEN_400,
            color=ft.Colors.WHITE
        )
        
        self.hint_btn = ft.ElevatedButton(
            "Hint",
            on_click=self.give_hint,
            bgcolor=ft.Colors.ORANGE_400,
            color=ft.Colors.WHITE
        )
        
        self.solve_btn = ft.ElevatedButton(
            "Solve",
            on_click=self.solve_puzzle,
            bgcolor=ft.Colors.PURPLE_400,
            color=ft.Colors.WHITE
        )
        
        self.status_text = ft.Text(
            "Welcome! Click 'New Game' to start.",
            size=14,
            text_align=ft.TextAlign.CENTER
        )
        
        self.setup_board()
        self.setup_page()
    
    def setup_page(self):
        """Set up the page layout and styling."""
        self.page.title = "Sudoku Game"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.window_width = 600
        self.page.window_height = 800
        
        # Header with title and controls
        header = ft.Row(
            [
                self.title,
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        # Control panel
        controls = ft.Row(
            [
                ft.Text("Difficulty:", size=16),
                self.difficulty_dropdown,
                self.mistakes_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
        
        # Buttons
        buttons = ft.Row(
            [
                self.new_game_btn,
                self.check_solution_btn,
                self.hint_btn,
                self.solve_btn,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10
        )
        
        # Main layout
        self.page.add(
            ft.Column(
                [
                    header,
                    controls,
                    self.create_board_ui(),
                    buttons,
                    self.status_text,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )
    
    def setup_board(self):
        """Initialize the board controls."""
        self.board_controls = []
        for i in range(9):
            row = []
            for j in range(9):
                text_field = ft.TextField(
                    width=50,
                    height=50,
                    text_align=ft.TextAlign.CENTER,
                    text_size=18,
                    border_radius=5,
                    on_change=lambda e, r=i, c=j: self.on_cell_change(e, r, c),
                    input_filter=ft.NumbersOnlyInputFilter(),
                    max_length=1,
                )
                row.append(text_field)
            self.board_controls.append(row)
    
    def create_board_ui(self) -> ft.Container:
        """Create the Sudoku board UI."""
        board_rows = []
        
        for i in range(9):
            board_cols = []
            for j in range(9):
                # Add thicker borders for 3x3 box separation
                border = ft.border.all(1, ft.Colors.GREY_400)
                if i % 3 == 0 and i != 0:
                    border.top = ft.BorderSide(2, ft.Colors.BLACK)
                if j % 3 == 0 and j != 0:
                    border.left = ft.BorderSide(2, ft.Colors.BLACK)
                if i == 8:
                    border.bottom = ft.BorderSide(2, ft.Colors.BLACK)
                if j == 8:
                    border.right = ft.BorderSide(2, ft.Colors.BLACK)
                if i == 0:
                    border.top = ft.BorderSide(2, ft.Colors.BLACK)
                if j == 0:
                    border.left = ft.BorderSide(2, ft.Colors.BLACK)
                
                cell_container = ft.Container(
                    content=self.board_controls[i][j],
                    border=border,
                    padding=0,
                    margin=0,
                )
                board_cols.append(cell_container)
            
            board_rows.append(
                ft.Row(
                    board_cols,
                    spacing=0,
                    alignment=ft.MainAxisAlignment.CENTER
                )
            )
        
        return ft.Container(
            content=ft.Column(
                board_rows,
                spacing=0,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            padding=10,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=15,
                color=ft.Colors.GREY_300,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.OUTER,
            )
        )
    
    def difficulty_changed(self, e):
        """Handle difficulty change."""
        self.difficulty = e.control.value
        self.status_text.value = f"Difficulty changed to {self.difficulty}. Click 'New Game' to apply."
        self.page.update()
    
    def new_game(self, e):
        """Start a new game."""
        self.mistakes = 0
        self.mistakes_text.value = f"Mistakes: {self.mistakes}/{self.max_mistakes}"
        
        # Generate new puzzle
        self.puzzle_board, self.solution_board = self.solver.generate_puzzle(self.difficulty)
        self.initial_board = [row[:] for row in self.puzzle_board]  # Deep copy
        
        # Update UI
        self.update_board_display()
        self.status_text.value = f"New {self.difficulty} game started! Good luck!"
        self.page.update()
    
    def update_board_display(self):
        """Update the board display with current values."""
        for i in range(9):
            for j in range(9):
                cell = self.board_controls[i][j]
                value = self.puzzle_board[i][j]
                
                if value == 0:
                    cell.value = ""
                    cell.read_only = False
                    cell.bgcolor = ft.Colors.WHITE
                    cell.color = ft.Colors.BLACK
                else:
                    cell.value = str(value)
                    cell.read_only = True
                    cell.bgcolor = ft.Colors.GREY_100
                    cell.color = ft.Colors.BLUE_800
    
    def on_cell_change(self, e, row: int, col: int):
        """Handle cell value change."""
        if self.initial_board[row][col] != 0:  # Can't edit initial numbers
            return
        
        value = e.control.value
        if value == "":
            self.puzzle_board[row][col] = 0
            e.control.bgcolor = ft.Colors.WHITE
        else:
            try:
                num = int(value)
                if 1 <= num <= 9:
                    self.puzzle_board[row][col] = num
                    
                    # Check if the move is correct
                    if self.solution_board[row][col] == num:
                        e.control.bgcolor = ft.Colors.GREEN_100
                    else:
                        e.control.bgcolor = ft.Colors.RED_100
                        self.mistakes += 1
                        self.mistakes_text.value = f"Mistakes: {self.mistakes}/{self.max_mistakes}"
                        
                        if self.mistakes >= self.max_mistakes:
                            self.status_text.value = "Game Over! Too many mistakes."
                            self.disable_board()
                else:
                    e.control.value = ""
                    self.puzzle_board[row][col] = 0
            except ValueError:
                e.control.value = ""
                self.puzzle_board[row][col] = 0
        
        self.page.update()
    
    def check_solution(self, e):
        """Check if the current solution is correct."""
        if self.solver.check_solution(self.puzzle_board):
            self.status_text.value = "Congratulations! You solved the puzzle!"
            self.status_text.color = ft.Colors.GREEN
            self.disable_board()
        else:
            # Check if puzzle is complete but incorrect
            is_complete = all(self.puzzle_board[i][j] != 0 for i in range(9) for j in range(9))
            if is_complete:
                self.status_text.value = "Puzzle is complete but has errors. Keep trying!"
                self.status_text.color = ft.Colors.RED
            else:
                self.status_text.value = "Puzzle is not complete yet. Keep going!"
                self.status_text.color = ft.Colors.ORANGE
        
        self.page.update()
    
    def give_hint(self, e):
        """Provide a hint by filling one empty cell."""
        empty_cells = [(i, j) for i in range(9) for j in range(9) 
                      if self.puzzle_board[i][j] == 0 and self.initial_board[i][j] == 0]
        
        if not empty_cells:
            self.status_text.value = "No empty cells to hint!"
            self.page.update()
            return
        
        # Pick a random empty cell
        import random
        row, col = random.choice(empty_cells)
        correct_value = self.solution_board[row][col]
        
        self.puzzle_board[row][col] = correct_value
        self.board_controls[row][col].value = str(correct_value)
        self.board_controls[row][col].bgcolor = ft.Colors.YELLOW_100
        self.board_controls[row][col].read_only = True
        
        self.status_text.value = f"Hint: Added {correct_value} at row {row+1}, column {col+1}"
        self.page.update()
    
    def solve_puzzle(self, e):
        """Show the complete solution."""
        self.puzzle_board = [row[:] for row in self.solution_board]
        self.update_board_display()
        self.disable_board()
        self.status_text.value = "Puzzle solved automatically!"
        self.page.update()
    
    def disable_board(self):
        """Disable all board interactions."""
        for i in range(9):
            for j in range(9):
                self.board_controls[i][j].read_only = True


def main(page: ft.Page):
    """Main application entry point."""
    game = SudokuGame(page)


if __name__ == "__main__":
    ft.app(target=main)