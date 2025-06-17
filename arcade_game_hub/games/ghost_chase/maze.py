"""
Maze generation for Ghost Chase game.
"""
import random

class Maze:
    """Maze class for Ghost Chase game."""
    
    def __init__(self, width, height):
        """Initialize the maze.
        
        Args:
            width: Width of the maze in cells
            height: Height of the maze in cells
        """
        self.width = width
        self.height = height
        self.grid = [[1 for _ in range(width)] for _ in range(height)]  # 1 = wall, 0 = path
        self.ghost_paths = []  # List of coordinates where ghost can pass through walls
        
        # Generate the maze using depth-first search
        self._generate_maze()
        
        # Create ghost paths (special walls that ghosts can pass through)
        self._create_ghost_paths()
    
    def _generate_maze(self):
        """Generate a random maze using depth-first search algorithm."""
        # Start with all walls
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = 1
        
        # Start at a random cell
        start_x = random.randint(0, self.width // 2 - 1) * 2 + 1
        start_y = random.randint(0, self.height // 2 - 1) * 2 + 1
        
        # Make sure the starting point is a path
        self.grid[start_y][start_x] = 0
        
        # Create a stack for backtracking
        stack = [(start_x, start_y)]
        visited = set([(start_x, start_y)])
        
        # Directions: (dx, dy)
        directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
        
        # DFS to carve paths
        while stack:
            x, y = stack[-1]
            
            # Find unvisited neighbors
            neighbors = []
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width and 0 <= ny < self.height and 
                    (nx, ny) not in visited):
                    neighbors.append((nx, ny, dx, dy))
            
            if neighbors:
                # Choose a random neighbor
                nx, ny, dx, dy = random.choice(neighbors)
                
                # Remove the wall between current cell and chosen neighbor
                self.grid[y + dy // 2][x + dx // 2] = 0
                self.grid[ny][nx] = 0
                
                # Mark as visited and add to stack
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                # Backtrack
                stack.pop()
        
        # Ensure the entrance (top-left) and exit (bottom-right) are open
        self.grid[1][1] = 0  # Entrance
        self.grid[self.height - 2][self.width - 2] = 0  # Exit
        
        # Make sure there's a path from entrance to exit
        self._ensure_path()
    
    def _ensure_path(self):
        """Ensure there's a path from entrance to exit."""
        # Simple approach: create a direct path if needed
        if not self._has_path():
            # Create a simple path from entrance to exit
            for x in range(1, self.width - 1):
                self.grid[1][x] = 0
            for y in range(1, self.height - 1):
                self.grid[y][self.width - 2] = 0
    
    def _has_path(self):
        """Check if there's a path from entrance to exit using BFS."""
        start = (1, 1)
        end = (self.width - 2, self.height - 2)
        
        # BFS
        queue = [start]
        visited = set([start])
        
        # Directions: (dx, dy)
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        
        while queue:
            x, y = queue.pop(0)
            
            if (x, y) == end:
                return True
            
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width and 0 <= ny < self.height and 
                    self.grid[ny][nx] == 0 and (nx, ny) not in visited):
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        
        return False
    
    def _create_ghost_paths(self):
        """Create special paths that only ghosts can use."""
        # Add some walls that ghosts can pass through
        num_ghost_paths = random.randint(3, 6)
        
        for _ in range(num_ghost_paths):
            # Find a wall that's not on the border
            while True:
                x = random.randint(1, self.width - 2)
                y = random.randint(1, self.height - 2)
                
                if self.grid[y][x] == 1:
                    # Check if it's not a border wall
                    if (0 < x < self.width - 1 and 0 < y < self.height - 1):
                        self.ghost_paths.append((x, y))
                        break
    
    def is_wall(self, x, y):
        """Check if the given coordinates are a wall.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if the cell is a wall, False otherwise
        """
        # Check bounds
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        
        return self.grid[y][x] == 1
    
    def is_ghost_path(self, x, y):
        """Check if the given coordinates are a ghost path.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if the cell is a ghost path, False otherwise
        """
        return (x, y) in self.ghost_paths
