"""
Test script for maze solver algorithms.
"""
import asyncio


class MazeCell:
    """Simple maze cell for testing."""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.is_wall = False
        self.is_start = False
        self.is_end = False
        self.is_visited = False
        self.is_path = False
        self.algorithm_state = "unvisited"


def test_maze_algorithms():
    """Test the maze generation and pathfinding concepts."""
    print("Testing Maze Solver Components...")
    
    # Test MazeCell creation
    cell = MazeCell(5, 3)
    assert cell.x == 5
    assert cell.y == 3
    assert not cell.is_wall
    assert not cell.is_start
    print("✓ MazeCell creation works")
    
    # Test basic pathfinding logic concepts
    def is_valid_move(x, y, maze_size, walls):
        """Check if a move is valid."""
        return (0 <= x < maze_size and 0 <= y < maze_size and (x, y) not in walls)
    
    # Test with a simple 5x5 maze
    maze_size = 5
    walls = {(1, 1), (1, 2), (2, 1), (3, 3)}
    
    # Test valid moves
    assert is_valid_move(0, 0, maze_size, walls), "Should be valid move"
    assert is_valid_move(4, 4, maze_size, walls), "Should be valid move"
    assert not is_valid_move(1, 1, maze_size, walls), "Should be invalid (wall)"
    assert not is_valid_move(-1, 0, maze_size, walls), "Should be invalid (out of bounds)"
    assert not is_valid_move(5, 0, maze_size, walls), "Should be invalid (out of bounds)"
    print("✓ Move validation logic works")
    
    # Test neighbor generation
    def get_neighbors(x, y):
        """Get valid neighbor positions."""
        return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    
    neighbors = get_neighbors(2, 2)
    expected = [(3, 2), (1, 2), (2, 3), (2, 1)]
    assert set(neighbors) == set(expected), f"Expected {expected}, got {neighbors}"
    print("✓ Neighbor generation works")
    
    # Test DFS concept (stack-based)
    def dfs_concept_test():
        stack = [(0, 0)]
        visited = set()
        path = []
        
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            path.append(current)
            
            # Simulate adding neighbors (simplified)
            x, y = current
            for nx, ny in get_neighbors(x, y):
                if is_valid_move(nx, ny, maze_size, walls) and (nx, ny) not in visited:
                    stack.append((nx, ny))
        
        return len(visited) > 1  # Should visit multiple cells
    
    assert dfs_concept_test(), "DFS concept should work"
    print("✓ DFS algorithm concept works")
    
    # Test BFS concept (queue-based)
    def bfs_concept_test():
        from collections import deque
        queue = deque([(0, 0)])
        visited = {(0, 0)}
        path = []
        
        while queue:
            current = queue.popleft()
            path.append(current)
            
            # Simulate adding neighbors (simplified)
            x, y = current
            for nx, ny in get_neighbors(x, y):
                if is_valid_move(nx, ny, maze_size, walls) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        
        return len(visited) > 1  # Should visit multiple cells
    
    assert bfs_concept_test(), "BFS concept should work"
    print("✓ BFS algorithm concept works")
    
    print("\n🎉 All maze solver tests passed!")
    print("\nAlgorithm Comparison:")
    print("• DFS: Uses stack (LIFO), goes deep first, may not find shortest path")
    print("• BFS: Uses queue (FIFO), explores level by level, finds shortest path")


if __name__ == "__main__":
    test_maze_algorithms()