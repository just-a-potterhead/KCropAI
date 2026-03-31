# src/search.py
from collections import deque

class FarmIrrigationSearch:
    """
    Demonstrates Uninformed Search (BFS) to find the shortest path 
    for an irrigation pipeline avoiding obstacles (rocks/structures) in a farm grid.
    """
    def __init__(self, grid):
        # 0 = Free land, 1 = Obstacle (Rock), 'S' = Source (Water), 'C' = Crop
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    def find_shortest_irrigation_path(self, start, target):
        """Uses Breadth-First Search (BFS) for guaranteed shortest path on an unweighted grid."""
        queue = deque([(start, [start])])
        visited = set([start])

        # Directions: Up, Down, Left, Right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            (r, c), path = queue.popleft()

            if (r, c) == target:
                return path # Path found

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                
                # Check boundaries and obstacles
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.grid[nr][nc] != 1 and (nr, nc) not in visited:
                        visited.add((nr, nc))
                        queue.append(((nr, nc), path + [(nr, nc)]))
                        
        return None # No path exists
