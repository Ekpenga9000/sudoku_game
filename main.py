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
        self.hints_used = 0
        self.max_hints = 18  # Default for medium
        self.game_active = False  # Track if game is currently active
        
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
        
        self.hints_text = ft.Text(
            f"Hints: {self.hints_used}/{self.max_hints}",
            size=16,
            color=ft.Colors.BLUE_400
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
            f"Hint ({self.max_hints})",
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
            "🎮 Ready to play? Click 'New Game' to start your Sudoku adventure!",
            size=14,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.BLUE_600
        )
        
        # Instruction text for new game
        self.instruction_text = ft.Text(
            "👆 Select your difficulty level above, then click 'New Game' to begin!",
            size=13,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.GREY_600,
            italic=True,
            visible=True
        )
        
        # Difficulty lock indicator
        self.difficulty_lock_text = ft.Text(
            "🔒 Difficulty locked during game",
            size=11,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.GREY_500,
            italic=True,
            visible=False
        )
        
        self.setup_board()
        self.setup_page()
        self.show_welcome_dialog()
    
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
                self.hints_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        )
        
        # Control panel with lock indicator
        controls_with_lock = ft.Column(
            [
                controls,
                self.difficulty_lock_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5
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
                    controls_with_lock,
                    self.instruction_text,
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
    
    def show_welcome_dialog(self):
        """Show welcome dialog when the application starts."""
        def close_dialog(e):
            welcome_dialog.open = False
            self.page.update()
        
        def start_new_game(e):
            welcome_dialog.open = False
            self.page.update()
            self.new_game(e)
        
        welcome_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Welcome to Sudoku!", size=24, weight=ft.FontWeight.BOLD),
            content=ft.Column([
                ft.Text("🧩 Ready to challenge your mind?", size=16, text_align=ft.TextAlign.CENTER),
                ft.Text(""),
                ft.Text("• Choose your difficulty level", size=14),
                ft.Text("• Fill the 9×9 grid with numbers 1-9", size=14),
                ft.Text("• Each row, column, and 3×3 box must contain all digits", size=14),
                ft.Text("• You have 3 mistakes before game over", size=14),
                ft.Text("• Hints available: Easy (30), Medium (18), Hard (10)", size=14),
                ft.Text(""),
                ft.Text("Good luck and have fun! 🎯", size=16, text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD),
            ], 
            width=400,
            height=250,
            alignment=ft.MainAxisAlignment.CENTER
            ),
            actions=[
                ft.TextButton("Maybe Later", on_click=close_dialog),
                ft.ElevatedButton(
                    "Start New Game!", 
                    on_click=start_new_game,
                    bgcolor=ft.Colors.GREEN_400,
                    color=ft.Colors.WHITE,
                    icon=ft.Icons.PLAY_ARROW
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        self.page.dialog = welcome_dialog
        welcome_dialog.open = True
        self.page.update()
    
    def get_max_hints_for_difficulty(self, difficulty: str) -> int:
        """Get maximum hints allowed for the given difficulty."""
        hint_limits = {
            "easy": 30,
            "medium": 18,
            "hard": 10
        }
        return hint_limits.get(difficulty, 18)
    
    def difficulty_changed(self, e):
        """Handle difficulty change."""
        # This should only be called when game is not active (dropdown is enabled)
        self.difficulty = e.control.value
        self.max_hints = self.get_max_hints_for_difficulty(self.difficulty)
        self.hints_text.value = f"Hints: {self.hints_used}/{self.max_hints}"
        self.hint_btn.text = f"Hint ({self.max_hints - self.hints_used})"
        # Make instruction text more prominent when difficulty changes
        self.instruction_text.visible = True
        self.instruction_text.value = f"✨ {self.difficulty.capitalize()} difficulty selected! Click 'New Game' to start playing!"
        self.instruction_text.color = ft.Colors.BLUE_700
        self.status_text.value = f"Difficulty changed to {self.difficulty}. Ready to challenge yourself?"
        self.status_text.color = ft.Colors.BLACK
        self.page.update()
    
    def new_game(self, e):
        """Start a new game."""
        self.mistakes = 0
        self.hints_used = 0
        self.max_hints = self.get_max_hints_for_difficulty(self.difficulty)
        self.mistakes_text.value = f"Mistakes: {self.mistakes}/{self.max_mistakes}"
        self.hints_text.value = f"Hints: {self.hints_used}/{self.max_hints}"
        
        # Generate new puzzle
        self.puzzle_board, self.solution_board = self.solver.generate_puzzle(self.difficulty)
        self.initial_board = [row[:] for row in self.puzzle_board]  # Deep copy
        
        # Update UI
        self.update_board_display()
        self.instruction_text.visible = False  # Hide instruction text once game starts
        
        # Set game as active
        self.game_active = True
        self.difficulty_dropdown.disabled = True  # Physically disable the dropdown
        self.difficulty_dropdown.bgcolor = ft.Colors.GREY_200  # Visual indicator that it's locked
        self.difficulty_dropdown.color = ft.Colors.GREY_500  # Dim text color when locked
        self.difficulty_lock_text.visible = True  # Show lock indicator
        
        # Reset hint button
        self.hint_btn.disabled = False
        self.hint_btn.text = f"Hint ({self.max_hints})"
        self.hint_btn.bgcolor = ft.Colors.ORANGE_400
        
        self.status_text.value = f"New {self.difficulty} game started! Good luck!"
        self.status_text.color = ft.Colors.BLACK
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
        # Check if hints are exhausted
        if self.hints_used >= self.max_hints:
            self.status_text.value = f"No more hints available! You've used all {self.max_hints} hints for {self.difficulty} difficulty."
            self.status_text.color = ft.Colors.RED
            self.page.update()
            return
        
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
        
        # Update hint counter
        self.hints_used += 1
        self.hints_text.value = f"Hints: {self.hints_used}/{self.max_hints}"
        
        remaining_hints = self.max_hints - self.hints_used
        self.status_text.value = f"Hint: Added {correct_value} at row {row+1}, column {col+1}. {remaining_hints} hints left."
        self.status_text.color = ft.Colors.BLUE_600
        
        # Update hint button if no hints left
        if self.hints_used >= self.max_hints:
            self.hint_btn.disabled = True
            self.hint_btn.text = "No Hints Left"
            self.hint_btn.bgcolor = ft.Colors.GREY_400
        else:
            self.hint_btn.text = f"Hint ({remaining_hints})"
        
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
        
        # Mark game as inactive so difficulty can be changed again
        self.game_active = False
        self.difficulty_dropdown.disabled = False  # Re-enable the dropdown
        self.difficulty_dropdown.bgcolor = ft.Colors.WHITE  # Reset visual indicator
        self.difficulty_dropdown.color = ft.Colors.BLACK  # Reset text color
        self.difficulty_lock_text.visible = False  # Hide lock indicator
        
        # Show instruction text again to encourage starting a new game
        self.instruction_text.visible = True
        self.instruction_text.value = "🎯 Ready for another challenge? Select difficulty and click 'New Game'!"
        self.instruction_text.color = ft.Colors.PURPLE_600


def main(page: ft.Page):
    """Main application entry point."""
    game = SudokuGame(page)


if __name__ == "__main__":
    ft.app(target=main)