import pygame
import math

zombie_type = ["regular", "tank", "small"]
health = [100, 200, 75]
speed = [0.75, 0.4, 0.9]
dmg = [10, 20, 15]
zombie_regular = pygame.image.load("sprites/zombie/zombie-regular.png")
zombie_tank = pygame.image.load("sprites/zombie/zombie-tank.png")
zombie_small = pygame.image.load("sprites/zombie/zombie-small.png")

sprites = [zombie_regular, zombie_tank, zombie_small]


class Zombie:
    def __init__(self, type_int, x_and_y: tuple, difficulty_multiply: float):
        self.x_pos = x_and_y[0]
        self.y_pos = x_and_y[1]
        self.sectors = []

        self.difficulty_multiplier = difficulty_multiply

        self.type = zombie_type[type_int]
        self.health = health[type_int] * self.difficulty_multiplier
        self.speed = speed[type_int] * self.difficulty_multiplier
        self.dmg = dmg[type_int] * self.difficulty_multiplier
        self.sprite = sprites[type_int]
        self.rect = self.sprite.get_rect()
        self.rotated_sprite = self.sprite
        self.flash_value = 0
        self.last_hit_on_player = 0

        self.size = self.sprite.get_height()
        self.sprite_size = self.sprite.get_width()

        self.hitbox = (self.x_pos, self.y_pos, self.size, self.size)

        self.money = [10, 20, 15]
        self.money_drop = self.money[type_int]
        if self.difficulty_multiplier > 1:
            self.money_drop += 5

    def get_rect_and_sprite(self, angle):
        self.rotated_sprite = pygame.transform.rotate(self.sprite, angle)
        self.rotated_sprite.fill((self.flash_value, self.flash_value, self.flash_value),
                                 special_flags=pygame.BLEND_RGB_ADD)
        self.rect = self.rotated_sprite.get_rect(center=self.sprite.get_rect(topleft=(self.x_pos, self.y_pos)).center)

    def display(self, screen: pygame.display, cam_x, cam_y):
        screen.blit(self.rotated_sprite, (self.rect.topleft[0]-cam_x, self.rect.topleft[1]-cam_y))

    def move(self, x_and_y_vel, dt):
        self.x_pos += x_and_y_vel[0] * dt/15 * self.speed
        self.y_pos += x_and_y_vel[1] * dt/15 * self.speed

    def get_hitbox(self, angle):
        x_y = pygame.math.Vector2((self.sprite_size-self.size)/2 * math.sin(math.radians(angle)),
                                  (self.sprite_size-self.size)/2 * math.cos(math.radians(angle))).rotate(270)
        x_y_after = pygame.math.Vector2(self.rect.center[0] - x_y[0], self.rect.center[1] - x_y[1])

        hitbox = pygame.Rect(x_y_after[0] - (self.size/2), x_y_after[1] - (self.size/2), self.size, self.size)

        self.hitbox = hitbox

    def trigger_hit(self, bullet_dmg):
        self.health -= bullet_dmg
