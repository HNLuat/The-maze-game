import pygame
from cell import Cell
from random import choice


class Maze:
    """
    class: Maze: mê cung hiện tại
    input:
        - cols, rows, số hàng số cột của mê cung
        - tile: kích thước mỗi ô trong mê cung
        - obj1_size, obj2_size: lần lượt là kích thước của key và bullet
    các thông số khác:
        - thichness: độ dày của tường
        - grid_cells: list tất cả các ô của mê cung
    """
    def __init__(self, cols, rows, tile, obj1_size, obj2_size):
        self.cols = cols
        self.rows = rows
        self.tile = tile
        self.thickness = 5
        self.grid_cells = [Cell(col, row, tile, self.thickness, obj1_size, obj2_size) for row in range(self.rows) for col in range(self.cols)]
        
    def remove_walls(self, current, next):
        """
        Phá tường giữa 2 ô
        input:
            - current, next: kiểu cells: là 2 ô cần phá tường ở giữa
        """
        dx = current.x - next.x
        if dx == 1:
            current.walls['left'] = False
            next.walls['right'] = False
        elif dx == -1:
            current.walls['right'] = False
            next.walls['left'] = False
        dy = current.y - next.y
        if dy == 1:
            current.walls['top'] = False
            next.walls['bottom'] = False
        elif dy == -1:
            current.walls['bottom'] = False
            next.walls['top'] = False
            
    def generate_maze(self):
        """
        Tạo mê cung
        return: grid_cells: list tất cả các ô sau khi phá tường
        """
        current_cell = self.grid_cells[0]
        array = []
        break_count = 1
        while break_count != len(self.grid_cells):
            current_cell.visited = True
            neighbors = current_cell.check_neighbors(self.cols, self.rows, self.grid_cells)
            next_cell = choice(neighbors) if neighbors else False
            if next_cell:
                next_cell.visited = True
                break_count += 1
                array.append(current_cell)
                self.remove_walls(current_cell, next_cell)
                current_cell = next_cell
            elif array:
                current_cell = array.pop()
        return self.grid_cells

