import pygame
import math


class Projectile:
    def __init__(self, x, y, x_vel, y_vel, bullet_dmg: int, start_time: int, life: int, player_or_zombie: int):
        self.player_or_zombie = player_or_zombie
        self.x_pos = x
        self.y_pos = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.dmg = bullet_dmg
        self.sectors = []
        self.bullet_start_time = start_time
        self.life = life

    def move(self, dt):
        self.x_pos += (self.x_vel * dt/8)
        self.y_pos += (self.y_vel * dt/8)


class Bullet(Projectile):
    def __init__(self, x, y, x_vel, y_vel, bullet_dmg: int, start_time: int, life: int, player_or_zombie: int):
        super().__init__(x, y, x_vel, y_vel, bullet_dmg, start_time, life, player_or_zombie)
        self.rocket = False
        self.size = 7
        self.hitbox = (self.x_pos, self.y_pos, self.size, self.size)
        self.a = 0
        self.b = 0

    def display(self, screen: pygame.display, camera_x, camera_y):
        pygame.draw.ellipse(screen, (25, 103, 255), pygame.Rect(self.x_pos-camera_x, self.y_pos-camera_y, self.hitbox[2], self.hitbox[3]))
        self.a = camera_x
        self.b = camera_y

    def get_hitbox(self):
        self.hitbox = pygame.Rect(self.x_pos, self.y_pos, self.size, self.size)


class Rocket(Projectile):
    def __init__(self, x, y, x_vel, y_vel, angle, start_time, life, player_or_zombie: int, rocket: pygame.surface):
        super().__init__(x, y, x_vel, y_vel, 50, start_time, life, player_or_zombie)
        self.sprite = rocket
        self.angle = angle
        self.rotated_sprite = pygame.transform.rotate(self.sprite, angle)
        self.rect = self.rotated_sprite.get_rect(center=self.sprite.get_rect(topleft=(self.x_pos, self.y_pos)).center)
        self.rocket = True

        self.len_center_to_corner = math.sqrt(163.25)
        self.angle1 = math.degrees(math.acos(242/(22*self.len_center_to_corner)))
        self.angle2 = 180 - (2*self.angle1)
        self.angles = [self.angle + self.angle1, self.angle + self.angle2, self.angle + self.angle1 + 180,
                       self.angle + self.angle2 + 180]

        self.hitbox = self.get_rect_from_corner_positions(self.get_corners_positions(self.get_center_of_rocket()))

    def display(self, screen: pygame.display, cam_x, cam_y):
        screen.blit(self.rotated_sprite, (self.rect.topleft[0]-cam_x, self.rect.topleft[1]-cam_y))
        # pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.rect), 2)
        # pygame.draw.ellipse(screen, (255, 255, 255), pygame.Rect(self.rect.center[0]-2, self.rect.center[1]-2, 4, 4))
        # pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.hitbox), 2)

    def move(self, dt):
        self.x_pos += (self.x_vel * dt/8)
        self.y_pos += (self.y_vel * dt/8)

    def get_hitbox(self):
        self.hitbox = self.get_rect_from_corner_positions(self.get_corners_positions(self.get_center_of_rocket()))
        self.rect = self.rotated_sprite.get_rect(center=self.sprite.get_rect(topleft=(self.x_pos, self.y_pos)).center)

    def get_center_of_rocket(self):
        x_y = pygame.math.Vector2(6 * math.sin(math.radians(self.angle)),
                                  6 * math.cos(math.radians(self.angle))).rotate(90)
        updated_x_y = [self.rect.center[0] - x_y[0], self.rect.center[1] - x_y[1]]

        return updated_x_y

    def get_corners_positions(self, x_y: list):
        corner_positions = []

        for i in range(4):
            xy = pygame.math.Vector2(self.len_center_to_corner * math.sin(math.radians(self.angles[i])),
                                     self.len_center_to_corner * math.cos(math.radians(self.angles[i]))).rotate(90)
            updated_xy = [x_y[0] - xy[0], x_y[1] - xy[1]]
            corner_positions.append(updated_xy)

        return corner_positions

    @staticmethod
    def get_rect_from_corner_positions(corner_positions: list):
        x_positions = []
        y_positions = []
        for i in corner_positions:
            x_positions.append(i[0])
            y_positions.append(i[1])

        min_x = min(x_positions)
        min_y = min(y_positions)
        max_x = max(x_positions)
        max_y = max(y_positions)

        return pygame.Rect(min_x, min_y, max_x-min_x, max_y-min_y)
