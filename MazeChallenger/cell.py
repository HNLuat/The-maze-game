# %%
# cell.py
import pygame

class Cell:
    def __init__(self, x, y, tile, thickness, obj1_size, obj2_size):
        self.x, self.y, self.tile = x, y, tile
        self.obj1_here = 0
        self.obj2_here = 0
        x, y = self.x * tile, self.y * tile
        self.obj1 = pygame.Rect(x + (tile - obj1_size)//2, y + (tile - obj1_size)//2, obj1_size, obj1_size)
        self.obj2 = pygame.Rect(x + (tile - obj2_size)//2, y + (tile - obj2_size)//2, obj1_size, obj2_size)
        self.thickness = thickness
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False
        
    # checks if cell does exist and returns it if it does
    def check_cell(self, x, y, cols, rows, grid_cells):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    # checking cell neighbors of current cell if visited (carved) or not
    def check_neighbors(self, cols, rows, grid_cells):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1, cols, rows, grid_cells)
        right = self.check_cell(self.x + 1, self.y, cols, rows, grid_cells)
        bottom = self.check_cell(self.x, self.y + 1, cols, rows, grid_cells)
        left = self.check_cell(self.x - 1, self.y, cols, rows, grid_cells)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return neighbors

# %%
