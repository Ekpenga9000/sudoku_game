"""
Maze solver with DFS and BFS algorithm visualization using Flet.
"""
import flet as ft
import random
import time
from typing import List, Tuple, Set
from collections import deque
import asyncio


class MazeCell:
    """Represents a single cell in the maze."""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.is_wall = False
        self.is_start = False
        self.is_end = False
        self.is_visited = False
        self.is_path = False
        self.algorithm_state = "unvisited"  # "unvisited", "visiting", "frontier", "visited", "path"


class MazeSolver:
    """Main maze solver class with Flet UI."""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.maze_size = 21  # Odd number for proper maze generation
        self.maze: List[List[MazeCell]] = []
        self.maze_controls: List[List[ft.Container]] = []
        self.start_pos = (1, 1)
        self.end_pos = (self.maze_size - 2, self.maze_size - 2)
        self.solving = False
        self.current_algorithm = "DFS"
        
        # Colors for different cell states
        self.colors = {
            "wall": ft.Colors.GREY_900,
            "empty": ft.Colors.GREY_50,
            "start": ft.Colors.GREEN_500,
            "end": ft.Colors.RED_500,
            "visiting": ft.Colors.YELLOW_600,  # Current cell being processed - brighter yellow
            "frontier": ft.Colors.CYAN_300,    # BFS frontier - cyan for better contrast
            "visited": ft.Colors.INDIGO_200,   # Visited cells - softer indigo
            "path": ft.Colors.PINK_400,        # Solution path - pink for distinction
            "border": ft.Colors.GREY_400
        }
        
        self.setup_ui()
        self.generate_maze()
        
    def setup_ui(self):
        """Set up the user interface."""
        self.page.title = "Maze Solver - DFS & BFS Visualization"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.window_width = 900
        self.page.window_height = 800
        
        # Title
        title = ft.Text(
            "🌟 Maze Solver Visualization",
            size=28,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )
        
        # Algorithm selector
        self.algorithm_dropdown = ft.Dropdown(
            width=120,
            options=[
                ft.dropdown.Option("DFS", "DFS"),
                ft.dropdown.Option("BFS", "BFS"),
            ],
            value="DFS",
            on_change=self.algorithm_changed
        )
        
        # Control buttons
        self.generate_btn = ft.ElevatedButton(
            "Generate Maze",
            on_click=self.generate_maze_click,
            bgcolor=ft.Colors.BLUE_400,
            color=ft.Colors.WHITE
        )
        
        self.solve_btn = ft.ElevatedButton(
            "Solve Maze",
            on_click=self.solve_maze_click,
            bgcolor=ft.Colors.GREEN_400,
            color=ft.Colors.WHITE
        )
        
        self.clear_btn = ft.ElevatedButton(
            "Clear Path",
            on_click=self.clear_path_click,
            bgcolor=ft.Colors.ORANGE_400,
            color=ft.Colors.WHITE
        )
        
        # Status text
        self.status_text = ft.Text(
            "Click 'Generate Maze' to start, then 'Solve Maze' to watch the algorithm!",
            size=14,
            text_align=ft.TextAlign.CENTER
        )
        
        # Speed control
        self.speed_slider = ft.Slider(
            min=1,
            max=10,
            value=5,
            divisions=9,
            label="{value}x",
            width=200
        )
        
        # Controls layout
        controls = ft.Row(
            [
                ft.Text("Algorithm:", size=16),
                self.algorithm_dropdown,
                ft.Text("Speed:", size=16),
                self.speed_slider,
                self.generate_btn,
                self.solve_btn,
                self.clear_btn,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15
        )
        
        # Legend
        legend = ft.Row(
            [
                ft.Container(width=20, height=20, bgcolor=self.colors["start"], border_radius=3),
                ft.Text("Start", size=12),
                ft.Container(width=20, height=20, bgcolor=self.colors["end"], border_radius=3),
                ft.Text("End", size=12),
                ft.Container(width=20, height=20, bgcolor=self.colors["wall"], border_radius=3),
                ft.Text("Wall", size=12),
                ft.Container(width=20, height=20, bgcolor=self.colors["visiting"], border_radius=3),
                ft.Text("Active", size=12),
                ft.Container(width=20, height=20, bgcolor=self.colors["frontier"], border_radius=3),
                ft.Text("Queue", size=12),
                ft.Container(width=20, height=20, bgcolor=self.colors["visited"], border_radius=3),
                ft.Text("Done", size=12),
                ft.Container(width=20, height=20, bgcolor=self.colors["path"], border_radius=3),
                ft.Text("Path", size=12),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5
        )
        
        # Initialize maze display
        self.create_maze_display()
        
        # Main layout
        self.page.add(
            ft.Column(
                [
                    title,
                    controls,
                    legend,
                    self.maze_container,
                    self.status_text,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            )
        )
    
    def create_maze_display(self):
        """Create the visual maze display."""
        self.maze = [[MazeCell(x, y) for x in range(self.maze_size)] for y in range(self.maze_size)]
        self.maze_controls = []
        
        rows = []
        for y in range(self.maze_size):
            row_controls = []
            row_containers = []
            for x in range(self.maze_size):
                container = ft.Container(
                    width=22,
                    height=22,
                    bgcolor=self.colors["wall"],
                    border_radius=3,  # Rounded corners for smoother look
                    border=ft.border.all(0.5, self.colors["border"]),  # Thinner border
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=1,
                        color=ft.Colors.GREY_400,
                        offset=ft.Offset(0, 0),
                    ),
                )
                row_controls.append(container)
                row_containers.append(container)
            
            self.maze_controls.append(row_controls)
            rows.append(ft.Row(row_containers, spacing=0.5))  # Smaller spacing
        
        self.maze_container = ft.Container(
            content=ft.Column(rows, spacing=0.5),  # Smaller spacing
            padding=15,
            bgcolor=ft.Colors.GREY_100,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.GREY_300,
                offset=ft.Offset(0, 2),
            ),
        )
    
    def algorithm_changed(self, e):
        """Handle algorithm selection change."""
        self.current_algorithm = e.control.value
        self.status_text.value = f"{self.current_algorithm} algorithm selected. Ready to solve!"
        self.page.update()
    
    def generate_maze(self):
        """Generate a random maze using recursive backtracking."""
        # Initialize all cells as walls
        for y in range(self.maze_size):
            for x in range(self.maze_size):
                self.maze[y][x].is_wall = True
                self.maze[y][x].is_visited = False
                self.maze[y][x].is_path = False
                self.maze[y][x].algorithm_state = "unvisited"
        
        # Create maze using recursive backtracking
        self._generate_maze_recursive(1, 1)
        
        # Set start and end positions
        self.maze[self.start_pos[1]][self.start_pos[0]].is_wall = False
        self.maze[self.start_pos[1]][self.start_pos[0]].is_start = True
        self.maze[self.end_pos[1]][self.end_pos[0]].is_wall = False
        self.maze[self.end_pos[1]][self.end_pos[0]].is_end = True
        
        # Update display
        self.update_maze_display()
    
    def _generate_maze_recursive(self, x: int, y: int):
        """Recursive maze generation algorithm."""
        self.maze[y][x].is_wall = False
        self.maze[y][x].is_visited = True
        
        # Define directions: right, down, left, up
        directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            
            # Check bounds
            if 0 <= nx < self.maze_size and 0 <= ny < self.maze_size:
                if self.maze[ny][nx].is_visited:
                    continue
                
                # Remove wall between current and next cell
                wall_x, wall_y = x + dx // 2, y + dy // 2
                self.maze[wall_y][wall_x].is_wall = False
                
                # Recursively visit next cell
                self._generate_maze_recursive(nx, ny)
    
    def update_maze_display(self):
        """Update the visual representation of the maze."""
        for y in range(self.maze_size):
            for x in range(self.maze_size):
                cell = self.maze[y][x]
                container = self.maze_controls[y][x]
                
                if cell.is_start:
                    container.bgcolor = self.colors["start"]
                elif cell.is_end:
                    container.bgcolor = self.colors["end"]
                elif cell.is_path:
                    container.bgcolor = self.colors["path"]
                elif cell.algorithm_state == "visiting":
                    container.bgcolor = self.colors["visiting"]
                elif cell.algorithm_state == "frontier":
                    container.bgcolor = self.colors["frontier"]
                elif cell.algorithm_state == "visited":
                    container.bgcolor = self.colors["visited"]
                elif cell.is_wall:
                    container.bgcolor = self.colors["wall"]
                else:
                    container.bgcolor = self.colors["empty"]
        
        self.page.update()
    
    def generate_maze_click(self, e):
        """Handle generate maze button click."""
        if self.solving:
            return
        
        self.status_text.value = "Generating new maze..."
        self.page.update()
        self.generate_maze()
        self.status_text.value = f"Maze generated! Ready to solve with {self.current_algorithm}."
        self.page.update()
    
    def clear_path_click(self, e):
        """Clear the solution path and algorithm visualization."""
        if self.solving:
            return
        
        for y in range(self.maze_size):
            for x in range(self.maze_size):
                cell = self.maze[y][x]
                cell.is_path = False
                cell.algorithm_state = "unvisited"
        
        self.update_maze_display()
        self.status_text.value = f"Path cleared. Ready to solve with {self.current_algorithm}."
        self.page.update()
    
    async def solve_maze_click(self, e):
        """Handle solve maze button click."""
        if self.solving:
            return
        
        self.solving = True
        self.solve_btn.disabled = True
        self.generate_btn.disabled = True
        
        # Clear previous solution
        self.clear_path_click(None)
        
        if self.current_algorithm == "DFS":
            await self.solve_dfs()
        else:
            await self.solve_bfs()
        
        self.solving = False
        self.solve_btn.disabled = False
        self.generate_btn.disabled = False
        self.page.update()
    
    async def solve_dfs(self):
        """Solve maze using Depth-First Search with visualization."""
        self.status_text.value = "Solving with DFS (Depth-First Search)..."
        self.page.update()
        
        stack = [self.start_pos]
        parent = {}
        visited = set()
        
        delay = (11 - self.speed_slider.value) * 0.05  # Convert speed to delay
        
        while stack:
            current = stack.pop()
            x, y = current
            
            if current in visited:
                continue
            
            visited.add(current)
            if not (self.maze[y][x].is_start or self.maze[y][x].is_end):
                self.maze[y][x].algorithm_state = "visiting"
            self.update_maze_display()
            await asyncio.sleep(delay)
            
            if current == self.end_pos:
                # Found the end, reconstruct path
                await self.reconstruct_path(parent, current)
                self.status_text.value = "DFS: Solution found! 🎉"
                self.page.update()
                return
            
            if not (self.maze[y][x].is_start or self.maze[y][x].is_end):
                self.maze[y][x].algorithm_state = "visited"
            
            # Explore neighbors (right, down, left, up)
            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nx, ny = x + dx, y + dy
                neighbor = (nx, ny)
                
                if (0 <= nx < self.maze_size and 0 <= ny < self.maze_size and
                    not self.maze[ny][nx].is_wall and neighbor not in visited):
                    stack.append(neighbor)
                    if neighbor not in parent:
                        parent[neighbor] = current
        
        self.status_text.value = "DFS: No solution found! 😞"
        self.page.update()
    
    async def solve_bfs(self):
        """Solve maze using Breadth-First Search with visualization."""
        self.status_text.value = "Solving with BFS (Breadth-First Search)..."
        self.page.update()
        
        queue = deque([self.start_pos])
        parent = {}
        visited = set([self.start_pos])
        
        delay = (11 - self.speed_slider.value) * 0.05  # Convert speed to delay
        
        while queue:
            # Show current frontier (queue contents) in orange
            for pos in queue:
                if pos != queue[0]:  # Don't color the current cell being processed
                    fx, fy = pos
                    if not (self.maze[fy][fx].is_start or self.maze[fy][fx].is_end):
                        self.maze[fy][fx].algorithm_state = "frontier"
            
            current = queue.popleft()
            x, y = current
            
            # Current cell being processed (yellow/amber)
            if not (self.maze[y][x].is_start or self.maze[y][x].is_end):
                self.maze[y][x].algorithm_state = "visiting"
            
            self.update_maze_display()
            await asyncio.sleep(delay)
            
            if current == self.end_pos:
                # Found the end, reconstruct path
                await self.reconstruct_path(parent, current)
                self.status_text.value = "BFS: Solution found! 🎉"
                self.page.update()
                return
            
            # Mark as visited (blue)
            if not (self.maze[y][x].is_start or self.maze[y][x].is_end):
                self.maze[y][x].algorithm_state = "visited"
            
            # Explore neighbors (right, down, left, up)
            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nx, ny = x + dx, y + dy
                neighbor = (nx, ny)
                
                if (0 <= nx < self.maze_size and 0 <= ny < self.maze_size and
                    not self.maze[ny][nx].is_wall and neighbor not in visited):
                    visited.add(neighbor)
                    queue.append(neighbor)
                    parent[neighbor] = current
        
        self.status_text.value = "BFS: No solution found! 😞"
        self.page.update()
    
    async def reconstruct_path(self, parent: dict, end_pos: Tuple[int, int]):
        """Reconstruct and visualize the solution path."""
        path = []
        current = end_pos
        
        while current in parent:
            path.append(current)
            current = parent[current]
        
        path.reverse()
        
        # Clear previous frontier states for cleaner path display
        for y in range(self.maze_size):
            for x in range(self.maze_size):
                if self.maze[y][x].algorithm_state == "frontier":
                    self.maze[y][x].algorithm_state = "visited"
        
        # Animate path reconstruction with smooth effect
        for i, pos in enumerate(path):
            x, y = pos
            if not (self.maze[y][x].is_start or self.maze[y][x].is_end):
                self.maze[y][x].is_path = True
                self.update_maze_display()
                
                # Faster animation for shorter paths, slower for longer paths
                delay = max(0.05, 0.15 - len(path) * 0.001)
                await asyncio.sleep(delay)


async def main(page: ft.Page):
    """Main application entry point."""
    maze_solver = MazeSolver(page)


if __name__ == "__main__":
    ft.app(target=main)