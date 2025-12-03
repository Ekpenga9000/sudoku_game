"""
Game Launcher - Choose between Sudoku and Maze Solver
"""
import flet as ft
import subprocess
import sys
import os


class GameLauncher:
    """Main launcher for games."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the launcher interface."""
        self.page.title = "Game Launcher"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 40
        self.page.window_width = 500
        self.page.window_height = 400
        
        # Title
        title = ft.Text(
            "🎮 Game Collection",
            size=36,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.BLUE_700
        )
        
        subtitle = ft.Text(
            "Choose your adventure!",
            size=18,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.GREY_600,
            italic=True
        )
        
        # Game buttons
        sudoku_btn = ft.ElevatedButton(
            content=ft.Column([
                ft.Icon(ft.Icons.GRID_4X4, size=48, color=ft.Colors.WHITE),
                ft.Text("Sudoku Game", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text("Logic puzzle with hints", size=12, color=ft.Colors.WHITE70),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
            width=200,
            height=120,
            bgcolor=ft.Colors.GREEN_500,
            on_click=self.launch_sudoku,
        )
        
        maze_btn = ft.ElevatedButton(
            content=ft.Column([
                ft.Icon(ft.Icons.ACCOUNT_TREE, size=48, color=ft.Colors.WHITE),
                ft.Text("Maze Solver", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text("DFS & BFS visualization", size=12, color=ft.Colors.WHITE70),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
            width=200,
            height=120,
            bgcolor=ft.Colors.PURPLE_500,
            on_click=self.launch_maze,
        )
        
        games_row = ft.Row(
            [sudoku_btn, maze_btn],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=30
        )
        
        # Status text
        self.status_text = ft.Text(
            "Click on a game to start playing!",
            size=14,
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.GREY_500
        )
        
        # Main layout
        self.page.add(
            ft.Column(
                [
                    title,
                    subtitle,
                    ft.Container(height=30),  # Spacer
                    games_row,
                    ft.Container(height=20),  # Spacer
                    self.status_text,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10
            )
        )
    
    def launch_sudoku(self, e):
        """Launch the Sudoku game."""
        self.status_text.value = "Launching Sudoku Game..."
        self.page.update()
        
        try:
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            venv_python = os.path.join(script_dir, ".venv", "bin", "python")
            main_py = os.path.join(script_dir, "main.py")
            
            if os.path.exists(venv_python) and os.path.exists(main_py):
                subprocess.Popen([venv_python, main_py])
                self.status_text.value = "Sudoku Game launched! 🧩"
            else:
                self.status_text.value = "Error: Could not find Sudoku game files."
        except Exception as ex:
            self.status_text.value = f"Error launching Sudoku: {str(ex)}"
        
        self.page.update()
    
    def launch_maze(self, e):
        """Launch the Maze Solver."""
        self.status_text.value = "Launching Maze Solver..."
        self.page.update()
        
        try:
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            venv_python = os.path.join(script_dir, ".venv", "bin", "python")
            maze_py = os.path.join(script_dir, "maze_solver.py")
            
            if os.path.exists(venv_python) and os.path.exists(maze_py):
                subprocess.Popen([venv_python, maze_py])
                self.status_text.value = "Maze Solver launched! 🌟"
            else:
                self.status_text.value = "Error: Could not find Maze Solver files."
        except Exception as ex:
            self.status_text.value = f"Error launching Maze Solver: {str(ex)}"
        
        self.page.update()


def main(page: ft.Page):
    """Main application entry point."""
    launcher = GameLauncher(page)


if __name__ == "__main__":
    ft.app(target=main)