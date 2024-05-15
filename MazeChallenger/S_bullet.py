import pygame
from maze import Maze
from cell import Cell
from monster import Monster
import math

def checkpos(x, y, n):
    return x >= 0 and x <= n and y >= 0 and y <= n
        
class sbullet:
    # class của bullet khi được bắn ra và khi đang bay
    def __init__(self, vel, size):
        self.vel = vel
        self.size = size
        shooted_bullet = pygame.image.load("My Game/images/bullet.png")
        self.image = pygame.transform.scale(shooted_bullet, (size, size))
        self.angle = 0
        self.rect = pygame.Rect(0, 0, size, size)

    def run(self, sc, maze_size):
        # kiểm tra vị trí hiện tại có phù hợp và cho viên đạn bay tiếp
        xvel = round(-math.sin(math.radians(self.angle))*self.vel)
        yvel = round(-math.cos(math.radians(self.angle))*self.vel)
        self.rect.x += xvel
        self.rect.y += yvel

        self.draw(sc)
        return checkpos(self.rect.x, self.rect.y, maze_size)

    def shoot(self, sc, xs, ys, xd, yd):
        # hàm điều chỉnh viên đạn khi người chơi bắn
        self.rect.centerx = xs
        self.rect.centery = ys
        x_dist = xd - xs
        y_dist = -(yd - ys)
        angle = math.degrees(math.atan2(y_dist, x_dist))
        self.image = pygame.transform.rotate(self.image, angle - 90)
        self.angle = angle - 90
        self.draw(sc)
        return 1

    def draw(self, sc):        
        # hàm vẽ viên đạn
        sc.blit(self.image, (self.rect.x, self.rect.y))
