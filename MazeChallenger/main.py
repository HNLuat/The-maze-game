import pygame
pygame.init()
import time
import random
from maze import Maze
from cell import Cell
from monster import Monster
pygame.font.init()

WIDTH, HEIGHT = 1200, 720
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Maze")
black_BG = pygame.Rect(0, 0, WIDTH, HEIGHT) 
BGmusic = pygame.mixer.music.load("My Game/audio/BGmusic.ogg")
pygame.mixer.music.play(-1)
FONT = pygame.font.SysFont("comicsans", 30 )


class pause_table:
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
    # draw a dark background
    pygame.draw.rect(WIN, "black", black_BG )

def draw_button(button):
    # draw "play game" button 
    pygame.draw.rect(WIN, "white", button, width = 5)
    play_text = FONT.render(f"PLAY GAME", 1, "white")
    WIN.blit(play_text, ( (WIDTH - 170)/2, (HEIGHT - 45)/2 ) )

def draw_player(player):
    # draw player
    pygame.draw.rect(WIN, "white", player)

def draw_rightside(num_key, num_key_to_win, num_bullet, max_bullet):
    # draw current number of bullet and key
    bullet = pygame.image.load("My Game/images/bullet.png")
    bullet = pygame.transform.scale(bullet, (75, 75))

    key = pygame.image.load("My Game/images/key.png")
    key = pygame.transform.scale(key, (75, 75))

    WIN.blit(bullet, (800, 280))
    WIN.blit(key,(800,180))
    keys_text = FONT.render(f"Keys: {num_key}/{num_key_to_win}", 1, "white")
    bullets_text = FONT.render(F"Bullets: {num_bullet}/{max_bullet}", 1, "white")
    
    WIN.blit(keys_text, (1000, 200))
    WIN.blit(bullets_text,(1000, 300))

def draw_pause_button(P_image):
    # draw pause button
    WIN.blit(P_image, (WIDTH - 300, 20))

def draw_paused_table(P_table):
    # draw paused table, player will see this after click pause button
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
    # draw the "game over" text
    gameover_text = FONT.render(f"GAME OVER", 1, "white")
    WIN.blit(gameover_text, (450, 280))
    
    if win == 1:
        youwin_text = FONT.render(f"YOU WIN", 1, "green")
        WIN.blit(youwin_text, (465, 350))
    else :
        youwin_text = FONT.render(f"YOU LOSE", 1, "red")
        WIN.blit(youwin_text, (465, 350))

def draw_cell(cells, tile, obj1, obj1_size, obj2, obj2_size):
    # draw walls betwween cells
    x, y = cells.x * cells.tile, cells.y * cells.tile
    if cells.obj1_here :
        WIN.blit(obj1, (x + (tile - obj1_size)//2, y + (tile - obj1_size)//2) )
    if cells.obj2_here :
        WIN.blit(obj2, (x + (tile - obj2_size)//2, y + (tile - obj2_size)//2) )
    if cells.walls['top']:
        pygame.draw.line(WIN, pygame.Color('darkgreen'), (x, y), (x + cells.tile, y), cells.thickness)
    if cells.walls['right']:
        pygame.draw.line(WIN, pygame.Color('darkgreen'), (x + cells.tile, y), (x + cells.tile, y + cells.tile), cells.thickness)
    if cells.walls['bottom']:
        pygame.draw.line(WIN, pygame.Color('darkgreen'), (x + cells.tile, y + cells.tile), (x , y + cells.tile), cells.thickness)
    if cells.walls['left']:
        pygame.draw.line(WIN, pygame.Color('darkgreen'), (x, y + cells.tile), (x, y), cells.thickness)
    

def get_current_cell(x, y, grid_cells):
    # get cell (x,y) in grid_cells 
    for cell in grid_cells:
        if cell.x == x and cell.y == y:
            return cell
        
def check_move(x, y, grid_cells, tile, thickness, moving_state):
    # check if the player go through wall
    current_cell_x, current_cell_y = x // tile, y // tile
    current_cell = get_current_cell(current_cell_x, current_cell_y, grid_cells)
    current_cell_abs_x, current_cell_abs_y = current_cell_x * tile, current_cell_y * tile
    temp_moving_state = moving_state
    # change the moving state
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
    # check if the player move betwwen wall
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
    # move the player
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
    # check if the player get the bullet or the key
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
    # check if the player reach goal cell
    goal_cell_abs_x, goal_cell_abs_y = goal_cell.x * tile, goal_cell.y * tile
    if player.x >= goal_cell_abs_x and player.y >= goal_cell_abs_y:
        return True
    else:
        return False

def main():
    inHub = True
    
    # "Play game" button stats
    button_WIDTH = 200
    button_HEIGHT = 60  

    # "pause" button stat
    P_button = pygame.Rect(WIDTH - 300, 20, 100, 100)
    P_image = pygame.image.load("My Game/images/pause_button.png")
    P_image = pygame.transform.scale(P_image, (100, 100))
    P_table = pause_table(400, 300, 5, 300, 80, 5, 40)
    paused = False

    # to check if the game is over
    # gameover=0: not over yet
    # gameover=1: player win
    # gameover=-1: player lose
    gameover = 0

    # player stats
    player_size = 25
    player = pygame.Rect(4, 4, player_size, player_size)
    player_VEL = 5
    
    run = True
    clock = pygame.time.Clock()
    
    # time couting
    elapsed_time = 0
    start_time = time.time()
    paused_time = 0    
    
    # bullet stats
    bullet_size = 30
    bullet_add_increment = 5000
    num_bullet_add = 2
    bullet_count = 10000
    bullet = pygame.image.load("My Game/images/bullet.png")
    bullet = pygame.transform.scale(bullet, (bullet_size, bullet_size))
    max_bullet = 6
    num_bullet = 3

    # key stats
    key_size = 25
    key = pygame.image.load("My Game/images/key.png")
    bullet = pygame.transform.scale(bullet, (bullet_size, bullet_size))
    num_key = 0
    num_key_to_win = 10

    # check if the game start and init stuff
    game_init = 0

    # maze stats
    tile = 45
    maze_size = HEIGHT//tile
    total_grid = maze_size**2
    maze = Maze(maze_size, maze_size, tile, bullet_size, key_size)
    ids_list = []
    for i in range(total_grid):
        ids_list.append(i)
    # generate_maze
    maze.generate_maze()

    # monster stats
    monster = Monster(10, 25)
    monster_star_running_time = 3
    monster_paralyzed_time = 3
    monster_is_paralyzed = False
    paralyzed_count = 0

    while run:
        clock.tick(50)
        mouse_pos = pygame.mouse.get_pos()

        # get event and keys that player pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        keys = pygame.key.get_pressed()

        # when we are in main lobby
        if inHub:
            button = pygame.Rect(( (WIDTH - button_WIDTH)/2, (HEIGHT - button_HEIGHT)/2 ), (button_WIDTH, button_HEIGHT))
            if (button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]) or ((time.time() - start_time) >=1 and keys[pygame.K_SPACE]):
                inHub = False
                start_time = time.time()
            draw_BG()
            draw_button(button)
            pygame.display.update()
            continue 

        # when the game is over
        if gameover != 0 :
            draw_gameover(gameover)
            pygame.display.update()
            gameover_time = time.time() - start_time - elapsed_time
            if gameover_time >= 3 or (gameover_time >= 1 and keys[pygame.K_SPACE]):
                main()
                return
            continue

        # when the game is pause
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

        # check if we pause
        if (P_button.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]) or keys[pygame.K_p]:
            paused = True

        # count time, bullet and get the key the player press 
        bullet_count += 20
        elapsed_time = time.time() - start_time - paused_time
        
        # initilize stuff in game
        if not game_init:
            random.shuffle(ids_list)
            for _ in range(num_key_to_win):
                i = ids_list[_]
                maze.grid_cells[i].obj2_here = 1
            game_init = 1
        
        # check if player shoot
        if keys[pygame.K_SPACE] and num_bullet > 0 and not monster_is_paralyzed:
            num_bullet -= 1
            paralyzed_count = elapsed_time
        if elapsed_time - paralyzed_count <= monster_paralyzed_time :
            monster_is_paralyzed = True
        else :
            monster_is_paralyzed = False

        # check if the game is over
        if not monster_is_paralyzed and elapsed_time > monster_star_running_time:
            if monster.run(player, maze) == 1:
                gameover = -1
        if num_key == num_key_to_win and reached_goal(player, maze.grid_cells[-1], tile):
            gameover = 1
        

        # add more bullet
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
                    
        # move the player
        keys = pygame.key.get_pressed()
        
        MOVE(keys, player, player_VEL, maze.grid_cells, tile, maze.thickness)

        # check if the player pick the bullet and the key
        eat_state = check_eat_obj(player, maze)
        if num_bullet < max_bullet:
            num_bullet += eat_state[0]
        num_key += eat_state[1]

        # draw and display
        draw_BG()
        draw_player(player)
        monster.draw(WIN)
        for cell in maze.grid_cells:
            draw_cell(cell, tile, bullet, bullet_size, key, key_size)
        draw_pause_button(P_image)
        draw_rightside(num_key, num_key_to_win, num_bullet, max_bullet)
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()