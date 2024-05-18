import pygame
pygame.init()
import time
import random
from maze import Maze
from cell import Cell
from monster import Monster
from S_bullet import sbullet
import math
pygame.font.init()

WIDTH, HEIGHT = 1200, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Challenger")
black_BG = pygame.Rect(0, 0, WIDTH, HEIGHT) 
BGmusic = pygame.mixer.music.load("audio/BGmusic.mp3")
pygame.mixer.music.play(-1)
FONT = pygame.font.SysFont("comicsans", 30 )
Mode = {"Easy": True, "Normal": False, "Hard": False, "Nightmare": False}

class pause_table:
    """
    class: pause_table: bảng dừng game 
    input:
        - table_WIDTH: kiểu int: chiều rộng của bảng
        - table_HEIGHT: kiểu int: chiều cao của bảng
        - table_thickness: kiểu int: độ dày của hình chữ nhật của bảng
        - element_WIDTH: kiểu int: chiều rộng của các hình chữ nhật nhỏ hơn, hitbox của nút "continue" và "return"
        - element_HEIGHT: kiểu int: chiều cao của hình chữ nhật nhỏ
        - element_thickness: kiểu int: độ dày của hình chữ nhật nhỏ
        - size: kiểu int: kích thước font chữ
    """
    def __init__(self, table_WIDTH, table_HEIGHT, table_thickness, element_WIDTH, element_HEIGHT, element_thickness, size ):
        self.Font_size = size
        self.Font =  pygame.font.SysFont("comicsans", size)
        x = (WIDTH - table_WIDTH)/2
        y = (HEIGHT - table_HEIGHT)/2
        self.table = pygame.Rect( x, y, table_WIDTH, table_HEIGHT )
        self.continue_table = pygame.Rect( x + (table_WIDTH - element_WIDTH)/2 , y + ( (1/2)*table_HEIGHT - element_HEIGHT)/2 , element_WIDTH, element_HEIGHT )
        self.return_table = pygame.Rect( x + (table_WIDTH - element_WIDTH)/2 , y + ( (1/2)*table_HEIGHT - element_HEIGHT)/2 + (1/2)*table_HEIGHT, element_WIDTH, element_HEIGHT )
        self.table_thickness = table_thickness
        self.element_thickness = element_thickness

def draw_BG():
    """
    Vẽ background
    """
    pygame.draw.rect(WIN, "black", black_BG )

def draw_button(button):
    """
    Vẽ nút play game
    input: 
        - button: kiểu dữ liệu pygame.Rect: là hitbox của nút
    """
    pygame.draw.rect(WIN, "white", button, width = 5)
    play_text = FONT.render(f"PLAY GAME", 1, "white")
    WIN.blit(play_text, ( (WIDTH - 170)/2, (HEIGHT - 45)/2 ) )

def draw_player(player, monster):
    """
    vẽ người chơi và cho cây súng xoay về hướng kẻ địch
    input:
        - player: kiểu dữ liệu pygame.Rect: là các thông số của player.
        - monster: kiểu dữ liệu Monster (trong file monster.py): là thông số của kẻ địch
    """
    player_image = pygame.image.load("images/player.png")
    player_image = pygame.transform.scale(player_image, (player.w, player.h))
    gun_image = pygame.image.load("images/gun.png")
    gun_image = pygame.transform.scale(gun_image, (player.w, player.h))
    x_dist = monster.rect.centerx - player.centerx
    y_dist = -(monster.rect.centery - player.centery)
    angle = math.degrees(math.atan2(y_dist, x_dist))
    center = (player.centerx + 10, player.centery - 2)
    if angle > 90 or angle < -90:
        gun_image = pygame.transform.flip(gun_image, flip_x = False, flip_y = True)
        center =  (player.centerx - 10, player.centery - 2)
    gun_image = pygame.transform.rotate(gun_image, angle)
    gun_rect = gun_image.get_rect(center = center)
    WIN.blit(player_image,(player.x, player.y))
    WIN.blit(gun_image, gun_rect)

def draw_rightside(num_key, num_key_to_win, num_bullet, max_bullet):
    """
    Vẽ các thứ ở góc phải màn hình khi chơi bao gồm số key hiện có, số bullet hiện có và hướng dẫn chơi
    input:
        - num_key: kiểu int: số lượng key mà người chơi hiện có
        - num_bullet: kiểu int: số lượng bullet mà người chơi hiện có
        - num_key_to_win: kiểu int: số lượng key mà người chơi cần có để thắng
        - max_bullet: kiểu int: số lượng bullet tối đa mà người chơi có thể có 
    """
    bullet = pygame.image.load("images/bullet.png")
    bullet = pygame.transform.scale(bullet, (75, 75))

    key = pygame.image.load("images/key.png")
    key = pygame.transform.scale(key, (75, 75))

    WIN.blit(bullet, (800, 280))
    WIN.blit(key,(800,180))
    keys_text = FONT.render(f"Keys: {num_key}/{num_key_to_win}", 1, "white")
    bullets_text = FONT.render(F"Bullets: {num_bullet}/{max_bullet}", 1, "white")
    
    WIN.blit(keys_text, (1000, 200))
    WIN.blit(bullets_text,(1000, 300))

    howtoplay_text1 = FONT.render("COLLECT ALL KEYS AND", 1, "white")
    howtoplay_text2 = FONT.render("REACH THE GOAL TO WIN", 1, "white")
    shoot_text = FONT.render("SPACE TO SHOOT", 1, "white")
    movement_text = FONT.render("ARROW KEY TO MOVE", 1, "white")

    WIN.blit(movement_text, (800, 400))
    WIN.blit(shoot_text, (800, 475))
    WIN.blit(howtoplay_text1, (800, 550))
    WIN.blit(howtoplay_text2, (800, 600))

def draw_pause_button():
    """
    Vẽ nút dừng game
    """
    P_image = pygame.image.load("images/pause_button.png")
    P_image = pygame.transform.scale(P_image, (100, 100))
    WIN.blit(P_image, (WIDTH - 300, 20))

def draw_paused_table(P_table):
    """
    Vẽ bảng dừng game.
    input:
        - P_table: kiểu pause_table: thông số của bảng dừng game
    """
    ct = P_table.continue_table
    rt = P_table.return_table
    F = P_table.Font
    sz = P_table.Font_size
    t = P_table.table
    pygame.draw.rect(WIN, "white", t, P_table.table_thickness)
    pygame.draw.rect(WIN, "white", ct, P_table.element_thickness)
    pygame.draw.rect(WIN, "white", rt, P_table.element_thickness)
    continue_text = F.render(f"CONTINUE", 1, "white")
    return_text = F.render(f"RETURN", 1, "white")
    WIN.blit(continue_text, (ct.x + round((ct.width - 0.63*8*sz)/2) , ct.y + round((ct.height - 1.5*sz)/2) ) )
    WIN.blit(return_text, (rt.x + round((rt.width - 0.63*6*sz)/2) , rt.y + round((rt.height - 1.5*sz)/2) ) ) 

def draw_gameover(win):
    """
    Vẽ dòng chữ hiện lên khi kết thúc game
    input:
        - win: kiểu bool: cho biết người chơi thắng hay thua
    """
    gameover_text = FONT.render(f"GAME OVER", 1, "white")
    WIN.blit(gameover_text, (450, 280))
    
    if win == 1:
        youwin_text = FONT.render(f"YOU WIN", 1, "green")
        WIN.blit(youwin_text, (465, 350))
    else :
        youwin_text = FONT.render(f"YOU LOSE", 1, "red")
        WIN.blit(youwin_text, (465, 350))

def draw_cell(cells, obj1, obj1_size, obj2, obj2_size):
    """
    Vẽ tường xung quanh 1 ô và key và bullet nếu có trong ô
    input:
        - cells: kiểu Cell (trong file cell): thông số của 1 ô
        - obj1: kiểu pygame image: hình của bullet
        - obj2: kiểu pygame image: hình của key
        - obj1_size: kích thước của hình bullet (hình vuông)
        - obj2_size: kích kích thước của hình key (hình vuông)
    """ 
    x, y = cells.x * cells.tile, cells.y * cells.tile
    if cells.obj1_here :
        WIN.blit(obj1, (x + (cells.tile - obj1_size)//2, y + (cells.tile - obj1_size)//2) )
    if cells.obj2_here :
        WIN.blit(obj2, (x + (cells.tile - obj2_size)//2, y + (cells.tile - obj2_size)//2) )
    if cells.walls['top']:
        pygame.draw.line(WIN, pygame.Color('darkgreen'), (x, y), (x + cells.tile, y), cells.thickness)
    if cells.walls['right']:
        pygame.draw.line(WIN, pygame.Color('darkgreen'), (x + cells.tile, y), (x + cells.tile, y + cells.tile), cells.thickness)
    if cells.walls['bottom']:
        pygame.draw.line(WIN, pygame.Color('darkgreen'), (x + cells.tile, y + cells.tile), (x , y + cells.tile), cells.thickness)
    if cells.walls['left']:
        pygame.draw.line(WIN, pygame.Color('darkgreen'), (x, y + cells.tile), (x, y), cells.thickness)
    
def draw_door(tile):
    """
    Vẽ cánh cửa ở ô đích
    input:
        - kích thước mỗi ô
    """
    door_image = pygame.image.load("images/door.png")
    door_image = pygame.transform.scale(door_image, (tile - 5, tile - 5))
    WIN.blit(door_image, (HEIGHT - tile + 5, HEIGHT - tile ))

def draw_Mode_button(easy_mode_button, normal_mode_button, hard_mode_button, nightmare_mode_button):
    """
    Vẽ các nút chọn độ khó và cho biết độ khó đang chọn
    input: 
        - easy_mode_button: kiểu pygame.Rect: thông số của nút chọn độ khó "easy"
        - normal_mode_button: kiểu pygame.Rect: thông số của nút chọn độ khó "normal"
        - hard_mode_button: kiểu pygame.Rect: thông số của nút chọn độ khó "hard"
        - nightmare_mode_button: kiểu pygame.Rect: thông số của nút chọn độ khó "nightmare"
    """
    pygame.draw.rect(WIN, "green", easy_mode_button, width = 10)
    pygame.draw.rect(WIN, "orange", normal_mode_button, width = 10)
    pygame.draw.rect(WIN, "red", hard_mode_button, width = 10)
    pygame.draw.rect(WIN, "purple", nightmare_mode_button, width = 10)
    if Mode["Easy"]:
        pygame.draw.rect(WIN, "green", easy_mode_button)
    if Mode["Normal"]:
        pygame.draw.rect(WIN, "orange", normal_mode_button)
    if Mode["Hard"]:
        pygame.draw.rect(WIN, "red", hard_mode_button)
    if Mode["Nightmare"]:
        pygame.draw.rect(WIN, "purple", nightmare_mode_button)
    easy_mode_text = FONT.render(f"EASY", 1, "white")
    normal_mode_text = FONT.render(f"NORMAL", 1, "white")
    hard_mode_text = FONT.render(f"HARD", 1, "white")
    nightmare_mode_text = FONT.render(f"NIGHTMARE", 1, "white")
    
    WIN.blit(easy_mode_text, (110, HEIGHT - 75))
    WIN.blit(normal_mode_text, (390, HEIGHT - 75))
    WIN.blit(hard_mode_text, (710, HEIGHT - 75))
    WIN.blit(nightmare_mode_text, (960, HEIGHT - 75))


def get_current_cell(x, y, grid_cells):
    """
    Hàm lấy ô ở vị trí (x,y)
    input:
        - x, y: cả 2 đều kiểu int : vị trí của ô
        - grid_cells: list chứa tất cả các ô
    """
    for cell in grid_cells:
        if cell.x == x and cell.y == y:
            return cell
        
def check_move(x, y, grid_cells, tile, thickness, moving_state):
    """
    kiểm tra xem người chơi có di chuyển đụng tường hay không
    input:
        - x, y: đều là kiểu int: vị trí người chơi
        - grid_cells: list chứa tất cả các ô
        - tile: kiểu int: kích thước mỗi ô
        - thickness: kiểu int: độ dày của tường
        - moving_state: kiểu dictionaries: cho biết: trạng thái di chuyển hiện tại của người chơi
    return: kiểu dictionaries: trạng thái di chuyển mới của người chơi
    """
    current_cell_x, current_cell_y = x // tile, y // tile
    current_cell = get_current_cell(current_cell_x, current_cell_y, grid_cells)
    current_cell_abs_x, current_cell_abs_y = current_cell_x * tile, current_cell_y * tile
    temp_moving_state = moving_state
    if moving_state['left']:
        if current_cell.walls['left']:
            if x <= current_cell_abs_x + thickness :
                temp_moving_state['left'] = False
    if moving_state['right']:
        if current_cell.walls['right']:
            if x >= current_cell_abs_x + tile - thickness :
                temp_moving_state['right'] = False
    if moving_state['up']:
        if current_cell.walls['top']:
            if y <= current_cell_abs_y + thickness :
                temp_moving_state['up'] = False
    if moving_state['down']:
        if current_cell.walls['bottom']:
            if y >= current_cell_abs_y + tile - thickness :
                temp_moving_state['down'] = False
    return temp_moving_state

def check_move2(direction, vel, x1, x2, y, grid_cells, tile):
    """
    kiểm tra xem người chơi có đi vào giữa tường không
    input: 
        - direction: kiểu string: cho biết hướng đi hiện tại của người chơi
        - vel: kiểu int: cho biết tốc độ của người chơi
        - x1, x2, y: đều là kiểu int: cho biết vị trí của người chơi ở góc trái trên, trái dưới, hoặc là góc trái trên, phải trên
        - grid_cells: list chứa tất cả các ô
        - tile: kích thước ô
    return: trả về 0 hoặc 1 là người chơi có thể di chuyển tiếp hay không
    """
    current_cell_x1, current_cell_x2, current_cell_y = x1 // tile, x2 // tile, y // tile
    if direction == "left" or direction == "right" :
        current_cell_1 = get_current_cell(current_cell_y, current_cell_x1, grid_cells)
        current_cell_2 = get_current_cell(current_cell_y, current_cell_x2, grid_cells)
    else :
        current_cell_1 = get_current_cell(current_cell_x1, current_cell_y, grid_cells)
        current_cell_2 = get_current_cell(current_cell_x2, current_cell_y, grid_cells)
    if current_cell_1 == current_cell_2 :
        return 1
    
    if direction == "left" or direction == "up" :
        if y - vel < current_cell_y * tile :
            return 0
    if direction == "right" or direction == "down":
        if y + vel > current_cell_y * tile + tile :
            return 0
    return 1

def MOVE(keys, player, vel, grid_cells, tile, thickness):
    """
    Di chuyển người chơi
    input:
        - keys: kiểu dictionaries: các phím mà người chơi ấn
        - player: kiểu pygame.Rect: thông số người chơi
        - vel: tốc độ người chơi
        - grid_cells: list chứa tất cả các ô
        - tile: kích thước mỗi ô
        - thickness: dộ dày các bức tường
    """
    moving_state = {'left' : keys[pygame.K_LEFT], 'right' : keys[pygame.K_RIGHT], 'up' : keys[pygame.K_UP], 'down' : keys[pygame.K_DOWN] }
    temp_state = check_move(player.x, player.y, grid_cells, tile, thickness, moving_state)
    temp_state = temp_state and check_move(player.x + player.w, player.y, grid_cells, tile, thickness, moving_state)
    temp_state = temp_state and check_move(player.x, player.y + player.h, grid_cells, tile, thickness, moving_state)
    temp_state = temp_state and check_move(player.x + player.w, player.y + player.h, grid_cells, tile, thickness, moving_state)
    moving_state = temp_state
    if moving_state['left'] :
        player.x -= vel * check_move2("left", vel, player.y, player.y + player.h, player.x, grid_cells, tile)
    if moving_state['right'] :
        player.x += vel * check_move2("right", vel, player.y, player.y + player.h , player.x + player.w, grid_cells, tile)
    if moving_state['up'] :
        player.y -= vel * check_move2("up", vel, player.x, player.x + player.w, player.y, grid_cells, tile)
    if moving_state['down'] :
        player.y += vel * check_move2("down", vel, player.x, player.x + player.w, player.y + player.h, grid_cells, tile)
    

def check_eat_obj(player, maze):
    """
    kiểm tra xem người chơi có nhặt key hay bullet không
    input:
        - player: kiểu pygame.Rect: thông số của người chơi
        - maze: kiểu Maze (trong file maze): mê cung hiện tại
    return: x1, x2: kiểu bool: cho biết người chơi có nhặt key hay bullet không
    """
    eat1 = 0
    eat2 = 0
    for cell in maze.grid_cells :
        if cell.obj1_here and not eat1:
            if player.colliderect(cell.obj1):
                cell.obj1_here = 0
                eat1 = 1
        if cell.obj2_here and not eat2:
            if player.colliderect(cell.obj2):
                cell.obj2_here = 0
                eat2 = 1
    return eat1, eat2

def reached_goal(player, goal_cell, tile):
    """
    kiểm tra xem người chơi đến đích hay không
    input:
        - player: kiểu pygame.Rect: thông số người chơi
        - goal_cell: kiểu Cell: thông số ô đích
        - tile: kích thước mỗi ô
    return: True hoặc False cho biết người chơi đã đên ô đích chưa
    """
    goal_cell_abs_x, goal_cell_abs_y = goal_cell.x * tile, goal_cell.y * tile
    if player.x >= goal_cell_abs_x and player.y >= goal_cell_abs_y:
        return True
    else:
        return False

def check_choose_mode(mouse_pos, easy_mode_button, normal_mode_button, hard_mode_button, nightmare_mode_button):
    """
    kiểm tra xem người chơi có chọn chế độ chơi không, và thay đổi chế độ chơi
    input:
        - mouse_pos: vị trí con trỏ chuột trên màn hình
        - easy_mode_button: kiểu pygame.Rect: thông số của nút chọn độ khó "easy"
        - normal_mode_button: kiểu pygame.Rect: thông số của nút chọn độ khó "normal"
        - hard_mode_button: kiểu pygame.Rect: thông số của nút chọn độ khó "hard"
        - nightmare_mode_button: kiểu pygame.Rect: thông số của nút chọn độ khó "nightmare"
    """
    easy = easy_mode_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]
    normal = normal_mode_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]
    hard = hard_mode_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]
    nightmare = nightmare_mode_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]

    if easy or normal or hard or nightmare:
        Mode["Easy"] = False
        Mode["Normal"] = False
        Mode["Hard"] = False
        Mode["Nightmare"] = False

    if (easy_mode_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]):
        Mode["Easy"] = True
    if (normal_mode_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]):
        Mode["Normal"] = True
    if (hard_mode_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]):
        Mode["Hard"] = True
    if (nightmare_mode_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]):
        Mode["Nightmare"] = True

def main():
    """
    khai báo các chỉ số khác và chạy vòng lặp game
    """
    inHub = True
    
    button_WIDTH = 200
    button_HEIGHT = 60  

    easy_mode_button = pygame.Rect(0, HEIGHT - 100, 300, 200)
    normal_mode_button = pygame.Rect(300, HEIGHT - 100, 300, 200)
    hard_mode_button = pygame.Rect(600, HEIGHT - 100, 300, 200)
    nightmare_mode_button = pygame.Rect(900, HEIGHT - 100, 300, 200)

    P_button = pygame.Rect(WIDTH - 300, 20, 100, 100)
    P_table = pause_table(400, 300, 5, 300, 80, 5, 40)
    paused = False

    gameover = 0

    player_size = 40
    player = pygame.Rect(4, 4, player_size, player_size)
    player_VEL = 5
    
    run = True
    clock = pygame.time.Clock()
    
    elapsed_time = 0
    start_time = time.time()
    paused_time = 0
    last_shoot_time = time.time()
    
    bullet_size = 25
    bullet_add_increment = 3000
    num_bullet_add = 1
    bullet_count = 3000
    bullet = pygame.image.load("images/bullet.png")
    bullet = pygame.transform.scale(bullet, (bullet_size, bullet_size))
    max_bullet = 12
    num_bullet = 6
    
    bullet_vel = 20
    shooted_bullet_size = 20
    list_shooted_bullet = []

    key_size = 30
    key = pygame.image.load("images/key.png")
    key = pygame.transform.scale(key, (key_size, key_size))
    num_key = 0
    num_key_to_win = 10

    game_init = 0

    tile = 60
    maze_size = HEIGHT//tile
    total_grid = maze_size**2
    maze = Maze(maze_size, maze_size, tile, bullet_size, key_size)
    ids_list = []
    for i in range(total_grid-1):
        ids_list.append(i)
    maze.generate_maze()

    monster = Monster(5, 40)
    monster_star_running_time = 4
    monster_paralyzed_time = 4
    monster_is_paralyzed = False
    paralyzed_count = 0
    while run:
        clock.tick(50)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()

        if inHub:
            button = pygame.Rect(( (WIDTH - button_WIDTH)/2, (HEIGHT - button_HEIGHT)/2 ), (button_WIDTH, button_HEIGHT))
            if (button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]) or ((time.time() - start_time) >=0.5 and keys[pygame.K_SPACE]):
                inHub = False
                start_time = time.time()
            draw_BG()
            check_choose_mode(mouse_pos, easy_mode_button, normal_mode_button, hard_mode_button, nightmare_mode_button)
            draw_Mode_button(easy_mode_button, normal_mode_button, hard_mode_button, nightmare_mode_button)
            draw_button(button)
            pygame.display.update()
            continue 
        
        if gameover != 0 :
            draw_gameover(gameover)
            pygame.display.update()
            gameover_time = time.time() - start_time - elapsed_time
            if gameover_time >= 3 or (gameover_time >= 0.5 and keys[pygame.K_SPACE]):
                main()
                return
            continue

        if paused:
            paused_time = time.time() - start_time - elapsed_time
            draw_paused_table(P_table)
            if P_table.continue_table.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] :
                paused = False
            if P_table.return_table.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0] :
                main()
                return 
            pygame.display.update()
            continue

        if (P_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]) or keys[pygame.K_p]:
            paused = True

        bullet_count += 20
        elapsed_time = time.time() - start_time - paused_time
        
        if not game_init:
            last_shoot_time = time.time()
            if Mode["Normal"]:
                max_bullet = 6
                num_bullet = 3
                monster.vel = 6
                monster.color = "orange"
                monster_star_running_time = 3.5
                monster_paralyzed_time = 3.5
                bullet_add_increment = 3500
            if Mode["Hard"]:
                max_bullet = 6
                num_bullet = 3
                monster.vel = 8
                monster.color = "red"
                monster_star_running_time = 3
                monster_paralyzed_time = 3
                bullet_add_increment = 4000
            if Mode["Nightmare"]:
                max_bullet = 6
                num_bullet = 3
                monster.vel = 10
                monster.color = "purple"
                monster_star_running_time = 2.5
                monster_paralyzed_time = 2.5
                bullet_add_increment = 4500
                bullet_count = 0
            random.shuffle(ids_list)
            for _ in range(num_key_to_win):
                i = ids_list[_]
                maze.grid_cells[i].obj2_here = 1
            game_init = 1
        
        if elapsed_time - paralyzed_count >= monster_paralyzed_time:
            monster_is_paralyzed = False

        if not monster_is_paralyzed and elapsed_time > monster_star_running_time:
            if monster.run(player, maze) == 1:
                gameover = -1
                continue
        if num_key == num_key_to_win and reached_goal(player, maze.grid_cells[-1], tile):
            gameover = 1
        
        if bullet_count >= bullet_add_increment:
            random.shuffle(ids_list)
            num = 0
            for _ in range(total_grid):
                i = ids_list[_]
                if not maze.grid_cells[i].obj1_here and not maze.grid_cells[i].obj2_here:
                    num += 1
                    maze.grid_cells[i].obj1_here = 1
                    if num == num_bullet_add :
                        break
            bullet_count = 0
                    
        MOVE(keys, player, player_VEL, maze.grid_cells, tile, maze.thickness)

        eat_state = check_eat_obj(player, maze)
        if num_bullet < max_bullet: 
            num_bullet += eat_state[0]
        num_key += eat_state[1]



        draw_BG()
        draw_door(tile)
        for cell in maze.grid_cells:
            draw_cell(cell, bullet, bullet_size, key, key_size)
        draw_player(player, monster)
        monster.draw(WIN)
        if len(list_shooted_bullet) > 0:
            lst_pop = []
            for i in range(len(list_shooted_bullet)):
                s_bullet = list_shooted_bullet[i]
                flag = False
                if s_bullet.run(WIN, HEIGHT) == 0:
                    flag = True
                if s_bullet.rect.colliderect(monster.rect):
                    monster_is_paralyzed = True
                    paralyzed_count = elapsed_time
                    flag = True
                if flag:
                    lst_pop.append(i)
            for i in lst_pop:
                list_shooted_bullet.pop(i)

        if keys[pygame.K_SPACE] and num_bullet > 0 and time.time() - last_shoot_time >= 0.5:
            shooted_bullet = sbullet(bullet_vel, shooted_bullet_size)
            list_shooted_bullet.append(shooted_bullet)
            shooted_bullet.shoot(WIN, player.centerx, player.centery, monster.rect.centerx, monster.rect.centery)
            last_shoot_time = time.time()
            num_bullet -= 1

        draw_pause_button()
        draw_rightside(num_key, num_key_to_win, num_bullet, max_bullet)
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    """
    Gọi lại hàm main
    """
    main()
