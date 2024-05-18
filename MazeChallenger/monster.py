import pygame
from maze import Maze
from cell import Cell

def get_current_cell(x, y, grid_cells):
    for cell in grid_cells:
        if cell.x == x and cell.y == y:
            return cell
        
class Monster:
    """
    class: Monster: kẻ địch
    input:
        - vel: tốc độ kẻ địch
        - size: kích thước kẻ địch
    các thông sô khác:
        - color: màu để vẻ kẻ địch
        - rect: kiểu pygame.Rect: thông số, hitbox của kẻ địch
    """
    def __init__(self, vel, size):
        self.vel = vel
        self.size = size
        self.color = "green"
        self.rect = pygame.Rect(0, 0, size, size)

    def run(self, player, maze):
        """
        Tìm đường và di chuyển kẻ địch:
        input: 
            - player: kiểu pygame.Rect: thông số của người chơi
            - maze: mê cung hiện tại
        return:
            - 1 nếu kẻ địch bắt được người chơi
            - 0 nếu không
        """
        player_hitbox_size = player.w // 2
        player_hitbox = pygame.Rect((player.x + (player.w - player_hitbox_size)//2, player.y + (player.h - player_hitbox_size)//2) , (player_hitbox_size, player_hitbox_size))
        if self.rect.colliderect(player_hitbox):
            return 1

        x1 = self.rect.x
        y1 = self.rect.y
        x2 = player_hitbox.centerx
        y2 = player_hitbox.centery
        current_cell_x1, current_cell_y1 = x1 // maze.tile, y1 // maze.tile
        current_cell_x2, current_cell_y2 = x2 // maze.tile, y2 // maze.tile
        current_cell1 = get_current_cell(current_cell_x1, current_cell_y1, maze.grid_cells)
        current_cell2 = get_current_cell(current_cell_x2, current_cell_y2, maze.grid_cells)
        
        if current_cell_x1 == current_cell_x2 and current_cell_y1 == current_cell_y2:
            if x1 + self.size < x2:
                self.rect.x += self.vel
            if x2 < x1:
                self.rect.x -= self.vel
            if y1 + self.size < y2:
                self.rect.y += self.vel
            if y2 < y1:
                self.rect.y -= self.vel
            return 0

        for cell in maze.grid_cells:
            cell.visited = False
        
        
        queue = []
        queue.append(current_cell2)
        parent = -1
        while len(queue):
            current_cell = queue[0]
            queue.pop(0)
            current_cell.visited = True
            neighbors = current_cell.check_neighbors(maze.cols, maze.rows, maze.grid_cells)
            for i in neighbors:
                dx = current_cell.x - i.x
                dy = current_cell.y - i.y
                if dx == 1 and current_cell.walls['left']:
                    continue
                if dx == -1 and current_cell.walls['right']:
                    continue
                if dy == 1 and current_cell.walls['top']:
                    continue
                if dy == -1 and current_cell.walls['bottom']:
                    continue
                if i.x == current_cell1.x and i.y == current_cell1.y:
                    parent = current_cell
                    break
                queue.append(i)
            if parent != -1 :
                break

        current = current_cell1
        next = parent
        moving_state = {'left': False, 'right': False, 'up': False, 'down': False}
        dx = current.x - next.x
        if dx == 1:
            moving_state['left'] = True
        elif dx == -1:
            moving_state['right'] = True
        dy = current.y - next.y
        if dy == 1:
            moving_state['up'] = True
        elif dy == -1:
            moving_state['down'] = True
        
        current_cell_x3, current_cell_y3 = (x1 + self.size) // maze.tile, (y1 + self.size) // maze.tile
        if current_cell_x3 != current_cell_x1:
            if moving_state['up'] or moving_state['down']:
                moving_state['up'] = moving_state['down'] = False
                moving_state['left'] = True

        if current_cell_y3 != current_cell_y1:
            if moving_state['left'] or moving_state['right']:
                moving_state['left'] = moving_state['right'] = False
                moving_state['up'] = True

        if moving_state['left']:
            self.rect.x -= self.vel
        if moving_state['right']:
            self.rect.x += self.vel
        if moving_state['up']:
            self.rect.y -= self.vel
        if moving_state['down']:
            self.rect.y += self.vel
        
        return 0

    def draw(self, sc):
        """
        Vẽ kẻ địch
        input:
            - sc: surface để vẻ lên
        """
        pygame.draw.rect(sc, self.color, self.rect)
