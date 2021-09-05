import pygame


class Wall:
    def __init__(self, x: int, y: int, width: int, height: int, color: tuple, border_color: tuple, border_width: int,
                 sectors: list):
        self.x_pos = x
        self.y_pos = y
        self.width = width
        self.height = height
        self.color = color
        self.border_color = border_color
        self.border_width = border_width
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.sectors = sectors

    def display(self, screen: pygame.display, cam_x, cam_y):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x_pos - cam_x, self.y_pos - cam_y, self.width,
                                                         self.height))
        pygame.draw.rect(screen, self.border_color, pygame.Rect(self.x_pos - cam_x, self.y_pos - cam_y, self.width,
                                                                self.height), self.border_width)
