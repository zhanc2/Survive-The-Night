import pygame

explosion = pygame.image.load("sprites/player/explosion.png")


class Explosion:
    def __init__(self, x, y, time: int):
        self.x = x
        self.y = y
        self.explosion_hitbox = pygame.Rect(self.x - 30, self.y - 30, 60, 60)
        self.start_time = time
        self.sprite = explosion

    def display(self, screen: pygame.display, cam_x, cam_y):
        screen.blit(self.sprite, (self.explosion_hitbox[0]-cam_x, self.explosion_hitbox[1]-cam_y))
