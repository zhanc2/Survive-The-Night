import pygame
from player import Player
from projectile import Bullet, Rocket
from zombies import Zombie
from shop import Shop
from explosion import Explosion
from button import Button
from camera import Camera
from map import Map
import random
import math

pygame.font.init()


class Game:
    def __init__(self, screen: pygame.display, difficulty: int, mode: int):
        self.font = pygame.font.SysFont('Mistral', 22)
        self.bigger_font = pygame.font.SysFont('Mistral', 50)

        self.difficulty = 1+((difficulty-2)*0.1)
        self.mode = mode

        self.color = 22
        self.backgroundColour = (self.color, self.color, self.color)

        self.screen = screen
        self.clock = pygame.time.Clock()

        self.playerOne = Player()
        self.player_flash_time = 0
        self.hit_time = 0
        self.health_str = self.font.render("Health: ", False, (0, 0, 0))
        self.coins_display = self.font.render(":  " + str(self.playerOne.money), False, (0, 0, 0))

        self.shooting = False
        self.e_shooting = False
        self.reset_shot = False

        self.bullets = []
        self.explosions = []
        self.time_since_last_shot = 0
        self.bullet_sectors = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                               [], [], []]

        self.round_int = -1
        self.round_data = [[3, 0, 0],
                           [5, 0, 0],
                           [5, 1, 0],
                           [6, 1, 0],
                           [7, 2, 0],
                           [5, 0, 1],
                           [5, 1, 1],
                           [7, 2, 1],
                           [10, 3, 3],
                           [15, 0, 0],
                           [0, 6, 0],
                           [0, 0, 10],
                           [12, 5, 7],
                           [13, 6, 8],
                           [0, 10, 8],
                           [15, 2, 10],
                           [18, 5, 10]]
        self.round_display = self.font.render("Round: " + str(self.round_int+1), False, (0, 0, 0))

        self.zombie_spawn_random_num = 0
        self.zombie_spawn_x_y = (0, 0)
        self.round_zombies = []
        self.round_zombies_to_be_spawned = self.round_zombies
        self.time_since_last_spawn = 0
        self.zombie_to_be_spawned = 0
        self.zombie_spawn_delay = 750

        self.round_going = False
        self.round_start_time = 0

        self.running = True
        self.paused = False
        self.paused_str_1 = self.bigger_font.render("Game Paused", False, (0, 0, 0))
        self.paused_str_2 = self.bigger_font.render("Press Esc to Continue", False, (0, 0, 0))
        self.paused_time = 0
        self.game_end = 0
        self.won_or_lose = 0

        self.shop = Shop()
        self.menu_button_from_pause = Button("Menu", self.bigger_font, (300, 100), (400, 520))

        self.camera = Camera()
        self.player_pos = self.bigger_font.render(str(self.playerOne.x_pos) + "  " + str(self.playerOne.y_pos), False,
                                                  (255, 255, 255))

        self.map = Map()
        self.wall_sectors = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                             [], []]
        for wall in self.map.walls:
            for sector in wall.sectors:
                self.wall_sectors[sector-1].append(wall)

    def background(self):
        self.screen.fill(self.backgroundColour)
        self.color = 42 + (8 * self.round_int)
        self.backgroundColour = (self.color, self.color, self.color)
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(0 - self.camera.x_pos, 0 - self.camera.y_pos, 1000, 1000),
                         3)
        # for i in range(5):
        #     pygame.draw.line(self.screen, (0, 0, 0), ((i*200) - self.camera.x_pos, 0 - self.camera.y_pos),
        #                      ((i*200) - self.camera.x_pos, 1000 - self.camera.y_pos))
        #     pygame.draw.line(self.screen, (0, 0, 0), (0 - self.camera.x_pos, (i*200) - self.camera.y_pos),
        #                      (1000 - self.camera.x_pos, (i*200) - self.camera.y_pos))

    def update_camera(self):
        self.camera.update(self.playerOne.x_pos-400, self.playerOne.y_pos-300)

    @staticmethod
    def get_x_and_y_value(mx, my, px, py, sniper: bool = None):
        mouse_dis = (mx-px, my-py)

        if sniper:
            speed = 4
        else:
            speed = 2

        if mouse_dis[0] == 0:
            if mouse_dis[1] > 0:
                return 0, speed
            else:
                return 0, speed * -1
        if mouse_dis[1] == 0:
            if mouse_dis[0] > 0:
                return speed, 0
            else:
                return speed * -1, 0

        ratio = mouse_dis[0]/mouse_dis[1]
        opp_ratio = mouse_dis[1]/mouse_dis[0]

        x_y = [(speed / math.sqrt((opp_ratio * opp_ratio + 1))), (speed / math.sqrt(ratio * ratio + 1))]

        if mouse_dis[0] > 0:
            if mouse_dis[1] < 0:
                return [x_y[0], x_y[1] * -1]
            else:
                return [x_y[0], x_y[1]]
        else:
            if mouse_dis[1] > 0:
                return [x_y[0] * -1, x_y[1]]
            else:
                return [x_y[0] * -1, x_y[1] * -1]

    @staticmethod
    def get_angle(mx, my, px, py):
        dis_to_p = [mx - px, my - py]
        if dis_to_p[0] == 0:
            if dis_to_p[1] < 0:
                return 90
            else:
                return 270
        elif dis_to_p[1] == 0:
            if dis_to_p[0] < 0:
                return 180
            else:
                return 0
        else:
            tan_angle = dis_to_p[1] / dis_to_p[0]
            angle_to_mouse = math.degrees(math.atan(tan_angle))
            if dis_to_p[0] < 0:
                if dis_to_p[1] < 0:
                    angle_to_mouse *= -1
                    angle_to_mouse += 180
                else:
                    angle_to_mouse -= 180
                    angle_to_mouse *= -1
            else:
                angle_to_mouse *= -1
            return angle_to_mouse

    @staticmethod
    def get_x_and_y_from_angle(angle):
        if angle == 0:
            return 2, 0
        if angle == 180:
            return -2, 0
        if angle == 90:
            return 0, -2
        if angle == 270:
            return 0, 2

        x_and_y = [2 * math.sin(math.radians(90-angle)), 2 * math.sin(math.radians(angle))]

        if 0 < angle < 90:
            x_and_y[1] *= -1
        elif 0 > angle > -90 or 270 < angle < 360:
            x_and_y[1] *= -1
        elif 90 < angle < 180:
            x_and_y[1] *= -1
        elif 180 < angle < 270 or -90 > angle > -180:
            x_and_y[1] *= -1

        return x_and_y

    @staticmethod
    def check_rect_collisions(rect1, rect2):
        return rect1.colliderect(rect2)

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
                sectors.append((j-1)*4 + i)
        return sectors

    def check_inputs(self, mouse_and_others, keys, mouse_pos):
        for event in mouse_and_others:
            if event.type == pygame.QUIT:
                self.running = False
                self.won_or_lose = 0
                return 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not self.e_shooting:
                        self.shooting = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if not self.e_shooting:
                        self.shooting = False
                elif event.button == 4:
                    self.playerOne.change_guns_from_scroll()
                    self.reset_shot = True
                if event.button == 5:
                    self.playerOne.change_guns_from_scroll(False)
                    self.reset_shot = True
                self.reset_shot = self.playerOne.change_guns(self.shop.handle_buying_and_switching_guns(
                    self.playerOne.guns_status, self.playerOne.selected_gun, self.playerOne.money, mouse_pos))
                if self.shop.handle_buying_first_aid(self.playerOne.money):
                    self.playerOne.first_aid_purchase()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = True
                if event.key == pygame.K_1:
                    self.reset_shot = self.playerOne.change_guns(self.shop.handle_buying_and_switching_guns(
                        self.playerOne.guns_status, self.playerOne.selected_gun, self.playerOne.money, mouse_pos, 0))
                if event.key == pygame.K_2:
                    self.reset_shot = self.playerOne.change_guns(self.shop.handle_buying_and_switching_guns(
                        self.playerOne.guns_status, self.playerOne.selected_gun, self.playerOne.money, mouse_pos, 1))
                if event.key == pygame.K_3:
                    self.reset_shot = self.playerOne.change_guns(self.shop.handle_buying_and_switching_guns(
                        self.playerOne.guns_status, self.playerOne.selected_gun, self.playerOne.money, mouse_pos, 2))
                if event.key == pygame.K_4:
                    self.reset_shot = self.playerOne.change_guns(self.shop.handle_buying_and_switching_guns(
                        self.playerOne.guns_status, self.playerOne.selected_gun, self.playerOne.money, mouse_pos, 3))
                if event.key == pygame.K_5:
                    self.reset_shot = self.playerOne.change_guns(self.shop.handle_buying_and_switching_guns(
                        self.playerOne.guns_status, self.playerOne.selected_gun, self.playerOne.money, mouse_pos, 4))
                if event.key == pygame.K_6:
                    if self.shop.handle_buying_first_aid(self.playerOne.money, False):
                        self.playerOne.first_aid_purchase()
                if event.key == pygame.K_e:
                    if self.shooting:
                        self.shooting = False
                        self.e_shooting = False
                    else:
                        self.shooting = True
                        self.e_shooting = True

        if keys[pygame.K_d]:
            self.playerOne.x_vel += 0.75
        if keys[pygame.K_a]:
            self.playerOne.x_vel -= 0.75
        if keys[pygame.K_s]:
            self.playerOne.y_vel += 0.75
        if keys[pygame.K_w]:
            self.playerOne.y_vel -= 0.75

    def do_map(self):
        self.map.display(self.screen, self.camera.x_pos, self.camera.y_pos)

    def handle_player(self, d_time, mouse):
        angle = self.get_angle(mouse[0], mouse[1], 400, 300)
        self.playerOne.get_rect_and_sprite(angle)
        self.playerOne.get_hitbox(angle)
        self.playerOne.move(d_time, angle)
        self.playerOne.check_boundaries(angle)
        self.playerOne.sectors = self.get_sector(self.playerOne.hitbox[0], self.playerOne.hitbox[1],
                                                 self.playerOne.hitbox[2], self.playerOne.hitbox[3])
        # for sector in self.playerOne.sectors:
        #     for wall in self.wall_sectors[sector-1]:
        #         self.playerOne.check_walls(wall.rect, angle)
        self.camera.update(self.playerOne.x_pos-400, self.playerOne.y_pos-300)
        self.playerOne.display(self.screen, self.camera.x_pos, self.camera.y_pos)
        if self.playerOne.flash_value > 0:
            if pygame.time.get_ticks() - self.player_flash_time > 75:
                self.playerOne.flash_value = 0
        self.playerOne.display_health_bar(self.screen)
        self.screen.blit(self.health_str, (12, 10))

    def handle_bullet_spawning(self, mouse_pos):
        if self.shooting:
            time = pygame.time.get_ticks()
            if self.playerOne.selected_gun == 0 or self.playerOne.selected_gun == 2:
                if self.playerOne.selected_gun == 0:
                    shot_delay = 500
                    random_offset = random.randint(-4, 4)
                    life = 1500
                else:
                    shot_delay = 150
                    random_offset = random.randint(-10, 10)
                    life = 2000
                if time - self.time_since_last_shot > shot_delay:
                    x_and_y = self.get_x_and_y_from_angle(self.get_angle(mouse_pos[0], mouse_pos[1], 400, 300)
                                                          + random_offset)
                    bullet = Bullet(self.playerOne.rect.center[0], self.playerOne.rect.center[1],
                                    x_and_y[0], x_and_y[1],
                                    self.playerOne.bullet_dmg[self.playerOne.selected_gun], time, life)
                    self.bullets.append(bullet)
                    self.playerOne.take_recoil(x_and_y)
                    self.time_since_last_shot = pygame.time.get_ticks()
                    self.camera.update(self.playerOne.x_pos - 400, self.playerOne.y_pos - 300)
            elif self.playerOne.selected_gun == 1:
                if time - self.time_since_last_shot > 700:
                    for i in range(5):
                        angle = self.get_angle(mouse_pos[0], mouse_pos[1], 400, 300) + (7 * (i-2))
                        x_and_y = self.get_x_and_y_from_angle(angle)
                        bullet = Bullet(self.playerOne.rect.center[0], self.playerOne.rect.center[1],
                                        x_and_y[0], x_and_y[1],
                                        self.playerOne.bullet_dmg[self.playerOne.selected_gun], time, 500)
                        self.bullets.append(bullet)
                        self.playerOne.take_recoil(x_and_y)
                    self.time_since_last_shot = pygame.time.get_ticks()
                    self.camera.update(self.playerOne.x_pos - 400, self.playerOne.y_pos - 300)
            elif self.playerOne.selected_gun == 3:
                if time - self.time_since_last_shot > 750:
                    x_and_y = self.get_x_and_y_value(mouse_pos[0], mouse_pos[1], 400, 300, True)
                    bullet = Bullet(self.playerOne.rect.center[0], self.playerOne.rect.center[1],
                                    x_and_y[0], x_and_y[1],
                                    self.playerOne.bullet_dmg[self.playerOne.selected_gun], time, 5000)
                    self.bullets.append(bullet)
                    self.playerOne.take_recoil(x_and_y)
                    self.time_since_last_shot = pygame.time.get_ticks()
                    self.camera.update(self.playerOne.x_pos - 400, self.playerOne.y_pos - 300)
            elif self.playerOne.selected_gun == 4:
                if time - self.time_since_last_shot > 1000:
                    angle = self.get_angle(mouse_pos[0], mouse_pos[1], 400, 300)
                    x_and_y = self.get_x_and_y_from_angle(angle)
                    bullet = Rocket(self.playerOne.rect.center[0], self.playerOne.rect.center[1], x_and_y[0],
                                    x_and_y[1], angle, time, 5000)
                    self.bullets.append(bullet)
                    for i in range(5):
                        self.playerOne.take_recoil(x_and_y)
                    self.time_since_last_shot = pygame.time.get_ticks()
                    self.camera.update(self.playerOne.x_pos - 400, self.playerOne.y_pos - 300)

    def handle_bullet_general(self, d_time):
        for bullet in self.bullets:
            bullet.display(self.screen, self.camera.x_pos, self.camera.y_pos)
            bullet.move(d_time)
            bullet.sectors = self.get_sector(bullet.hitbox[0], bullet.hitbox[1], bullet.hitbox[2], bullet.hitbox[3])
            for sector in bullet.sectors:
                if bullet not in self.bullet_sectors[sector-1]:
                    self.bullet_sectors[sector-1].append(bullet)
            for sector in range(len(self.bullet_sectors)):
                if sector+1 not in bullet.sectors:
                    if bullet in self.bullet_sectors[sector]:
                        self.bullet_sectors[sector].remove(bullet)
            bullet.get_hitbox()
            if bullet.hitbox[0] > 1000 or bullet.hitbox[0] < -30:
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
                for bullet_sector in bullet.sectors:
                    if bullet in self.bullet_sectors[bullet_sector - 1]:
                        self.bullet_sectors[bullet_sector - 1].remove(bullet)
                return
            elif bullet.hitbox[1] > 1000 or bullet.hitbox[1] < -30:
                if bullet in self.bullets:
                    self.bullets.remove(bullet)
                for bullet_sector in bullet.sectors:
                    if bullet in self.bullet_sectors[bullet_sector - 1]:
                        self.bullet_sectors[bullet_sector - 1].remove(bullet)
                return
            if pygame.time.get_ticks() - bullet.bullet_start_time > bullet.life:
                bullet_comparison = bullet
                sectors_removed_from = bullet.sectors
                self.bullets.remove(bullet)
                for bullet_sector in sectors_removed_from:
                    if bullet_comparison in self.bullet_sectors[bullet_sector - 1]:
                        self.bullet_sectors[bullet_sector - 1].remove(bullet_comparison)

    def handle_zombie_spawning(self):
        if len(self.round_zombies) == 0 and len(self.round_zombies_to_be_spawned) == 0:
            self.round_going = False
            self.round_start_time = pygame.time.get_ticks()
            self.round_int += 1
            if self.round_int == len(self.round_data)-1:
                if self.mode == 2:
                    self.round_data.append([(self.round_int-4)+random.randint(-3, 3),
                                            (self.round_int-10)+random.randint(-3, 3),
                                            (self.round_int-8)+random.randint(-3, 3)])
            self.round_zombies_to_be_spawned = []
            self.round_display = self.font.render("Round: " + str(self.round_int+1), False, (0, 0, 0))
            if 8 > self.round_int > 4:
                self.zombie_spawn_delay = 900
            elif self.round_int > 8:
                self.zombie_spawn_delay = 1000
            for i in range(len(self.round_data[self.round_int])):
                for j in range(self.round_data[self.round_int][i]):
                    self.zombie_spawn_random_num = random.randint(1, 4)
                    if self.zombie_spawn_random_num == 1:
                        self.zombie_spawn_x_y = (random.randint(0, 1000), -20)
                    elif self.zombie_spawn_random_num == 2:
                        self.zombie_spawn_x_y = (-20, random.randint(0, 1000))
                    elif self.zombie_spawn_random_num == 3:
                        self.zombie_spawn_x_y = (random.randint(0, 1000), 1000)
                    else:
                        self.zombie_spawn_x_y = (1000, random.randint(0, 1000))
                    zombie = Zombie(i, self.zombie_spawn_x_y, self.difficulty)
                    self.round_zombies.append(zombie)

        if self.round_going:
            time = pygame.time.get_ticks()
            if time - self.time_since_last_spawn > self.zombie_spawn_delay:
                if len(self.round_zombies) > 0:
                    self.zombie_to_be_spawned = random.choice(self.round_zombies)
                    self.round_zombies_to_be_spawned.append(self.zombie_to_be_spawned)
                    self.round_zombies.remove(self.zombie_to_be_spawned)

                self.time_since_last_spawn = pygame.time.get_ticks()

    def handle_zombies_general(self, d_time):
        if self.round_going:
            for zombie in self.round_zombies_to_be_spawned:
                angle = self.get_angle(self.playerOne.rect.center[0],
                                       self.playerOne.rect.center[1], zombie.rect.center[0], zombie.rect.center[1])
                zombie.get_hitbox(angle)
                zombie.get_rect_and_sprite(angle)
                zombie.display(self.screen, self.camera.x_pos, self.camera.y_pos)
                zombie.move(self.get_x_and_y_value(self.playerOne.rect.center[0], self.playerOne.rect.center[1],
                                                   zombie.rect.center[0], zombie.rect.center[1]), d_time)
                zombie.sectors = self.get_sector(zombie.hitbox[0], zombie.hitbox[1], zombie.size, zombie.size)
                for sector in zombie.sectors:
                    for bullet in self.bullet_sectors[sector-1]:
                        if self.check_rect_collisions(zombie.hitbox, bullet.hitbox):
                            zombie.trigger_hit(bullet.dmg)
                            bullet_comparison = bullet
                            sectors_removed_from = bullet.sectors
                            if bullet in self.bullets:
                                self.bullets.remove(bullet)
                            for bullet_sector in sectors_removed_from:
                                if bullet_comparison in self.bullet_sectors[bullet_sector-1]:
                                    self.bullet_sectors[bullet_sector-1].remove(bullet_comparison)
                            self.hit_time = pygame.time.get_ticks()
                            zombie.flash_value = 150
                            if bullet.rocket:
                                explosion = Explosion(bullet.hitbox.center[0], bullet.hitbox.center[1],
                                                      pygame.time.get_ticks())
                                self.explosions.append(explosion)
                            break
                    # for wall in self.wall_sectors[sector-1]:
                    #     return
                for explosion in self.explosions:
                    if self.check_rect_collisions(zombie.hitbox, explosion.explosion_hitbox):
                        zombie.trigger_hit(1)
                        self.hit_time = pygame.time.get_ticks()
                        zombie.flash_value = 150
                if zombie.flash_value > 0:
                    if pygame.time.get_ticks() - self.hit_time > 75:
                        zombie.flash_value = 0
                if zombie.health <= 0:
                    self.playerOne.money += zombie.money_drop
                    self.round_zombies_to_be_spawned.remove(zombie)
                if self.check_rect_collisions(zombie.hitbox, self.playerOne.hitbox):
                    if pygame.time.get_ticks() - zombie.last_hit_on_player > 400:
                        self.playerOne.trigger_hit(zombie.dmg)
                        self.playerOne.flash_value = 150
                        zombie.last_hit_on_player = pygame.time.get_ticks()
        else:
            t = pygame.time.get_ticks() - self.round_start_time
            round_message = self.bigger_font.render("Next round Starting in " + str(3 - round(t / 1000)), False,
                                                    (0, 0, 0))
            self.screen.blit(round_message, (200, 200))
            if t > 3000:
                self.round_going = True

    def replace_cursor(self, mouse_pos):
        pygame.mouse.set_visible(False)
        pygame.draw.line(self.screen, (0, 0, 0), (mouse_pos[0], mouse_pos[1]-10), (mouse_pos[0], mouse_pos[1]+10))
        pygame.draw.line(self.screen, (0, 0, 0), (mouse_pos[0]-10, mouse_pos[1]), (mouse_pos[0]+10, mouse_pos[1]))

    def check_game_end(self):
        if self.round_int == len(self.round_data) - 1:
            if len(self.round_zombies_to_be_spawned) == 0:
                self.running = False
                self.won_or_lose = 1
                pygame.mouse.set_visible(True)

        if self.playerOne.health < 1:
            self.running = False
            self.won_or_lose = 2
            pygame.mouse.set_visible(True)

    def display_round(self):
        self.screen.blit(self.round_display, (720, 10))

    def check_game_paused(self, mouse: tuple, events: list):
        pygame.draw.rect(self.screen, self.backgroundColour, pygame.Rect(200, 110, 400, 150))
        self.screen.blit(self.paused_str_1, (280, 120))
        self.screen.blit(self.paused_str_2, (223, 200))
        pygame.mouse.set_visible(True)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = False
            if event.type == pygame.QUIT:
                self.running = False
                self.won_or_lose = 0
                self.paused = False
                return 0
            if event.type == pygame.MOUSEBUTTONUP:
                if 250 < mouse[0] < 550 and 470 < mouse[1] < 570:
                    self.won_or_lose = 0
                    self.paused = False
                    return 1

    def display_shop(self):
        self.shop.background_colors(self.screen, self.playerOne.guns_status, self.playerOne.money)
        self.shop.display(self.screen)
        self.shop.display_text(self.screen, self.playerOne.guns_status)
        self.coins_display = self.font.render(":  " + str(self.playerOne.money), False, (0, 0, 0))
        self.screen.blit(self.coins_display, (38, 35))

    def handle_explosions(self):
        for i in self.explosions:
            i.display(self.screen, self.camera.x_pos, self.camera.y_pos)
            time = pygame.time.get_ticks()
            if time - i.start_time > 200:
                self.explosions.remove(i)

    def back_to_menu_from_paused(self, mouse: tuple, events: list):
        self.menu_button_from_pause.display(self.screen, mouse)
        if self.menu_button_from_pause.check_click(mouse, events):
            self.running = False
            self.won_or_lose = 0
            self.paused = False
            return True
