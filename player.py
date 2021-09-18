import pygame
import math


class Player:
    def __init__(self, sprite: pygame.surface):
        self.x_pos = 400
        self.y_pos = 300
        self.x_vel = 0
        self.y_vel = 0
        self.size = 35
        self.color = (0, 0, 255)
        self.sprite = sprite
        self.rotatedSprite = self.sprite
        self.hitbox = (self.x_pos, self.y_pos, self.size, self.size)
        self.rect = self.sprite.get_rect()
        self.health = 100
        self.flash_value = 0
        self.health_bar_color = (0, 255, 0)
        self.money = 100
        self.guns_status = [2, 0, 0, 0, 0]
        self.selected_gun = 0
        self.bullet_dmg = [25, 20, 20, 75, 25]
        self.sectors = []

    def get_rect_and_sprite(self, angle):
        self.rotatedSprite = pygame.transform.rotate(self.sprite, angle)
        self.rotatedSprite.fill((self.flash_value, self.flash_value, self.flash_value),
                                special_flags=pygame.BLEND_RGB_ADD)
        self.rect = self.rotatedSprite.get_rect(center=(self.x_pos, self.y_pos))

    def display(self, screen, camera_x: float, camera_y: float):
        screen.blit(self.rotatedSprite, (self.rect.topleft[0]-camera_x, self.rect.topleft[1]-camera_y))
        # # screen.blit(self.rotatedSprite, (400-(self.rotatedSprite.get_width()/2),
        # 300-(self.rotatedSprite.get_height()/2)))
        # pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.hitbox[0]-camera_x,
        # self.hitbox[1]-camera_y, self.size, self.size), 2)
        # pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.rect[0]-camera_x,
        # self.rect[1]-camera_y, self.rect[2], self.rect[3]), 2)
        # pygame.draw.ellipse(screen, (255, 255, 255), pygame.Rect((self.hitbox[0] + self.hitbox[2]/2)-camera_x,
        # (self.hitbox[1] + self.hitbox[3]/2)-camera_y, 4, 4))
        # pygame.draw.ellipse(screen, (255, 255, 255), pygame.Rect(400, 300, 3, 3))
        # # pygame.draw.line(screen, (255, 0, 0), self.rect.center, (self.hitbox[0], self.hitbox[1]), 1)

    def move(self, dt, angle):
        self.x_pos += self.x_vel * (dt / 20)
        self.y_pos += self.y_vel * (dt / 20)

        self.x_vel *= 0.7
        self.y_vel *= 0.7

        if abs(self.x_vel) < 0.005:
            self.x_vel = 0
        if abs(self.y_vel) < 0.005:
            self.y_vel = 0

        self.get_rect_and_sprite(angle)
        self.get_hitbox(angle)

    def get_hitbox(self, angle):
        x_y = pygame.math.Vector2(10.5 * math.sin(math.radians(angle)), 10.5 * math.cos(math.radians(angle))).rotate(
            270)
        x_y_after = pygame.math.Vector2(self.rect.center[0] - x_y[0], self.rect.center[1] - x_y[1])

        self.hitbox = pygame.Rect(x_y_after[0] - 17.5, x_y_after[1] - 17.5, 35, 35)

    def check_boundaries(self, angle):
        if self.hitbox[1] + self.size > 1000:
            self.y_pos += (1000 - (self.hitbox[1] + self.size))
            self.y_vel = 0
        if self.hitbox[1] < 0:
            self.y_pos += 0 - self.hitbox[1]
            self.y_vel = 0
        if self.hitbox[0] + self.size > 1000:
            self.x_pos += (1000 - (self.hitbox[0] + self.size))
            self.x_vel = 0
        if self.hitbox[0] < 0:
            self.x_pos += 0 - self.hitbox[0]
            self.x_vel = 0
        self.get_rect_and_sprite(angle)
        self.get_hitbox(angle)

    def check_walls(self, wall_rect: pygame.Rect, angle):
        if wall_rect.colliderect(pygame.Rect(self.hitbox[0], self.hitbox[1], self.hitbox[2], self.hitbox[3])):
            if self.x_vel < 0 and self.y_vel == 0:
                self.x_pos += ((wall_rect[0] + wall_rect[2]) - self.hitbox[0])
                self.x_vel = 0
                self.get_rect_and_sprite(angle)
                self.get_hitbox(angle)
                return
            elif self.x_vel > 0 and self.y_vel == 0:
                self.x_pos += (wall_rect[0] - (self.hitbox[0] + self.hitbox[2]))
                self.x_vel = 0
                self.get_rect_and_sprite(angle)
                self.get_hitbox(angle)
                return
            if self.y_vel < 0 and self.x_vel == 0:
                self.y_pos += ((wall_rect[1] + wall_rect[3]) - self.hitbox[1])
                self.y_vel = 0
                self.get_rect_and_sprite(angle)
                self.get_hitbox(angle)
                return
            elif self.y_vel > 0 and self.x_vel == 0:
                self.y_pos += (wall_rect[1] - (self.hitbox[1] + self.hitbox[3]))
                self.y_vel = 0
                self.get_rect_and_sprite(angle)
                self.get_hitbox(angle)
                return
            if self.hitbox[0] + self.hitbox[2]/2 > wall_rect[0] + wall_rect[2]:
                self.x_pos += ((wall_rect[0] + wall_rect[2]) - self.hitbox[0])
                self.x_vel = 0
                self.get_rect_and_sprite(angle)
                self.get_hitbox(angle)
            elif self.hitbox[0] + self.hitbox[2]/2 < wall_rect[0]:
                self.x_pos += (wall_rect[0] - (self.hitbox[0] + self.hitbox[2]))
                self.x_vel = 0
                self.get_rect_and_sprite(angle)
                self.get_hitbox(angle)
            if self.hitbox[1] + self.hitbox[3]/2 > wall_rect[1] + wall_rect[3]:
                self.y_pos += ((wall_rect[1] + wall_rect[3]) - self.hitbox[1])
                self.y_vel = 0
                self.get_rect_and_sprite(angle)
                self.get_hitbox(angle)
            elif self.hitbox[1] + self.hitbox[3]/2 < wall_rect[1]:
                self.y_pos += (wall_rect[1] - (self.hitbox[1] + self.hitbox[3]))
                self.y_vel = 0
                self.get_rect_and_sprite(angle)
                self.get_hitbox(angle)

    def take_recoil(self, x_and_y: tuple):
        self.x_pos -= x_and_y[0] * 1.5
        self.y_pos -= x_and_y[1] * 1.5

    def trigger_hit(self, zombie_dmg: int):
        self.health -= zombie_dmg

    def display_health_bar(self, screen: pygame.display):
        if self.health > 50:
            self.health_bar_color = (0, 255, 0)
        elif 20 < self.health <= 50:
            self.health_bar_color = (255, 255, 0)
        elif self.health < 20:
            self.health_bar_color = (255, 0, 0)
        pygame.draw.rect(screen, self.health_bar_color, pygame.Rect(64, 15, (55 * (self.health / 100)), 13))

    def change_guns(self, action_gun_money: tuple):
        if action_gun_money[0] == 0:
            return False
        else:
            self.guns_status[self.selected_gun] = 1
            self.selected_gun = action_gun_money[1]
            self.guns_status[action_gun_money[1]] = 2
            if action_gun_money[0] == 2:
                self.money -= action_gun_money[2]
            return True

    def first_aid_purchase(self):
        self.health = 100
        self.money -= 500

    def change_guns_from_scroll(self, up_or_down: bool = True):
        if up_or_down:
            if self.selected_gun + 1 > 4:
                check = 0
            else:
                check = self.selected_gun + 1
            if self.guns_status[check] == 1:
                self.guns_status[self.selected_gun] = 1
                self.selected_gun = check
                self.guns_status[self.selected_gun] = 2
        else:
            if self.selected_gun - 1 < 0:
                check = 4
            else:
                check = self.selected_gun - 1
            if self.guns_status[check] == 1:
                self.guns_status[self.selected_gun] = 1
                self.selected_gun = check
                self.guns_status[self.selected_gun] = 2
