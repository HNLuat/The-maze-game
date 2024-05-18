import pygame
from maze import Maze
from cell import Cell
from monster import Monster
import math

def checkpos(x, y, n):
    """
    kiểm tra xem vị trí hiện tại có nằm trong mê cung không
    input:
        - x,y: vị trí cần xét
        - n: kích thước mê cung
    return: 1 nếu thỏa, 0 nếu không
    """
    return x >= 0 and x <= n and y >= 0 and y <= n
        
class sbullet:
    """
    class: sbullet: viên đạn đang bay
    input: 
        - vel: tốc độ viên đạn
        - size: kích thước viên đạn
    các thông số khác:
        - image: hình ảnh của viên đạn
        - angle: góc của viên đạn
        - rect: hitbox của viên đạn hiện tại
    """
    def __init__(self, vel, size):
        self.vel = vel
        self.size = size
        shooted_bullet = pygame.image.load("images/bullet.png")
        self.image = pygame.transform.scale(shooted_bullet, (size, size))
        self.angle = 0
        self.rect = pygame.Rect(0, 0, size, size)

    def run(self, sc, maze_size):
        """
        cho viên đạn bay tiếp
        input: 
            - sc: surface để vẽ lên
            - maze_size: kích thước mê cung
        return :
            - 1 nếu viên đạn còn nằm trong mê cung
            - 0 nếu không
        """
        xvel = round(-math.sin(math.radians(self.angle))*self.vel)
        yvel = round(-math.cos(math.radians(self.angle))*self.vel)
        self.rect.x += xvel
        self.rect.y += yvel

        self.draw(sc)
        return checkpos(self.rect.x, self.rect.y, maze_size)

    def shoot(self, sc, xs, ys, xd, yd):
        """
        điều chỉnh góc độ và bắt đầu bắn viên đạn
        input:
            - sc: surface để vẽ viên đạn
            - xs, ys: vị trí hiện tại bắn viên đạn
            - xd, yd: vị trí đích đến của viên đạn
        """
        self.rect.centerx = xs
        self.rect.centery = ys
        x_dist = xd - xs
        y_dist = -(yd - ys)
        angle = math.degrees(math.atan2(y_dist, x_dist))
        self.image = pygame.transform.rotate(self.image, angle - 90)
        self.angle = angle - 90
        self.draw(sc)

    def draw(self, sc):
        """
        vẽ viên đạn
        input:
            - sc: surface để vẽ viên đạn
        """
        sc.blit(self.image, (self.rect.x, self.rect.y))
