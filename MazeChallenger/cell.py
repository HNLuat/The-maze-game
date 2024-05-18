import pygame

class Cell:
    """
    class: Cell: mỗi ô trong mê cung
    input: 
        - x, y: đều là kiểu int: vị trí của ô
        - tile: kiểu int: kích thước mỗi ô
        - thickness: kiểu int: độ dày của tường
        - obj1_size: kiểu int: kích thước key
        - obj2_size: kiểu int: kích thước bullet
    các thông số khác:
        - walls: kiểu dictionaries: cho biêt giữa ô này với các ô xung quanh có tường không
        - obj1_here: kiểu bool: cho biết ô này có key không
        - obj2_here: kiểu bool: cho biết ô này có bullet không
        - visited: kiểu bool: cho biết ô này đã thăm chưa (chỉ được dùng trong thuật tìm đường đi và thuật tạo mê cung)
    """
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
        
    def check_cell(self, x, y, cols, rows, grid_cells):
        """
        Kiểm tra xem ô có tồn tại không
        input:
            - x, y: vị trí của ô
            - cols, rows: số cột và số hàng của mê cung
            - grid_cells: list tất cả các ô
        return : False nếu ô đó không tồn tại, trả về chính ô đó nếu tồn tại
        """
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    def check_neighbors(self, cols, rows, grid_cells):
        """
        Kiểm tra xem các ô bên cạnh đã thăm chưa và trả về các ô chưa thăm
        input:
            - cols, rows: số lượng cột và hàng trong mê cung
            - grid_cells: list tất cả các ô
        return : list các ô bên cạnh chưa thăm
        """
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

