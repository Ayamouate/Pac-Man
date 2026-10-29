from maze.screens import ScreensMixin
from collections import deque

class Ghost():
    def __init__(self, color, direction, spawn_pos, current_pos, state):
        self.color = color
        self.direction = direction
        self.spawn_pos = spawn_pos
        self.current_pos = current_pos
        self.state = state
        self.inside = ScreensMixin()
        self.parent = {}

    def get_neighbors(self, maze, cell):
        neighbors = []
        x, y = cell[0], cell[1]
        cell = int(maze.maze[y][x])

        if not cell & 1 and self.inside._inside(maze,x, y -1):
            neighbors.append((x, y - 1))
        if not cell & 2 and self.inside._inside(maze, x+ 1, y):
            neighbors.append((x + 1, y))
        if not cell & 4 and self.inside._inside(maze, x, y + 1):
            neighbors.append((x , y + 1))

        if not cell & 8 and self.inside._inside(maze, x -1 , y):
            neighbors.append((x-1, y))
        return neighbors
    
    def shortest_path(self,maze, target_pos):

        queue = deque([self.current_pos])
        visited = {self.current_pos}
        self.parent = {self.current_pos :None}
        while queue:
            cell = queue.popleft()
            if  cell == target_pos:
                break
            neighbors = self.get_neighbors(maze, cell)
            for neighbor in neighbors:
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                queue.append(neighbor)
                self.parent[neighbor] = cell
            
        if target_pos not in self.parent:
            return []

        path = []
        cell = target_pos

        while cell is not None:
            path.append(cell)
            cell = self.parent[cell]

        path.reverse()
        return path
    
    def move(self, maze, target_pos):
        path = self.shortest_path(maze, target_pos)
        if len(path) >= 2 :
            next_direction = path[1]
            return next_direction
        return
    