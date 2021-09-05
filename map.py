import pygame
from wall import Wall


class Map:
    def __init__(self):
        self.walls = []
        self.w1 = Wall(50, 50, 100, 100, (182, 182, 182), (0, 0, 0), 3, self.get_sector(100, 100, 2, 100))
        self.walls.append(self.w1)

    def display(self, screen, cam_x, cam_y):
        for wall in self.walls:
            wall.display(screen, cam_x, cam_y)

    @staticmethod
    def get_sector(x_pos, y_pos, x_size, y_size):
        sector_x_coords = []
        sector_y_coords = []
        sectors = []
        if 200 > x_pos >= 0 or 200 > x_pos + x_size >= 0:
            sector_x_coords.append(1)
        if 400 >= x_pos > 200 or 400 >= x_pos + x_size > 200:
            sector_x_coords.append(2)
        if 600 >= x_pos > 400 or 600 >= x_pos + x_size > 400:
            sector_x_coords.append(3)
        if 800 >= x_pos > 600 or 800 >= x_pos + x_size > 600:
            sector_x_coords.append(4)
        if 1000 >= x_pos > 800 or 1000 >= x_pos + x_size > 800:
            sector_x_coords.append(5)
        if 200 > y_pos >= 0 or 200 > y_pos + y_size >= 0:
            sector_y_coords.append(1)
        if 400 >= y_pos > 200 or 400 >= y_pos + y_size > 200:
            sector_y_coords.append(2)
        if 600 >= y_pos > 400 or 600 >= y_pos + y_size > 400:
            sector_y_coords.append(3)
        if 800 >= y_pos > 600 or 800 >= y_pos + y_size > 600:
            sector_y_coords.append(4)
        if 1000 >= y_pos > 800 or 1000 >= y_pos + y_size > 800:
            sector_y_coords.append(5)
        for i in sector_x_coords:
            for j in sector_y_coords:
                sectors.append((j - 1) * 4 + i)
        return sectors
