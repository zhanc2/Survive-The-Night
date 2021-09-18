import pygame
from button import Button
import random

lose_screen = pygame.image.load("sprites/misc/lose-screen.png")
win_screen = pygame.image.load("sprites/misc/win-screen.png")


class StartEnd:
    def __init__(self, screen: pygame.display):
        self.start_menu_going = True
        self.game_start_time = 0
        self.screen = screen

        self.title_font = pygame.font.SysFont('Mistral', 70)
        self.bigger_font = pygame.font.SysFont('Mistral', 45)
        self.medium_font = pygame.font.SysFont('Mistral', 30)

        self.start_button = Button("Start", self.bigger_font, (300, 100), (400, 340))
        self.instruction_button = Button("How to Play", self.bigger_font, (300, 100), (400, 587))
        self.restart_button_from_end = Button("Restart", self.bigger_font, (200, 100), (275, 630))
        self.restart_button_from_pause = Button("Restart", self.bigger_font, (300, 100), (400, 390))
        self.menu_button_from_end = Button("Menu", self.bigger_font, (200, 100), (525, 630))

        self.lose_message1 = self.bigger_font.render("You Lost!", False, (0, 0, 0))
        self.lose_message2 = self.bigger_font.render("Better Luck Next Time!", False, (0, 0, 0))
        self.win_message1 = self.bigger_font.render("Congratulations, You Won!", False, (0, 0, 0))
        self.win_message2 = self.bigger_font.render("Please Play Again!", False, (0, 0, 0))
        self.title_name = self.title_font.render("Survive the Night", False, (255, 255, 255))

        self.start_game = True
        self.restart = False
        self.stop = False

        self.instructions_1 = pygame.image.load("sprites/instructions/instructions-1.png")
        self.instructions_2 = pygame.image.load("sprites/instructions/instructions-2.png")
        self.instructions_2_2 = pygame.image.load("sprites/instructions/instructions-2-2.png")
        self.instructions_3 = pygame.image.load("sprites/instructions/instructions-3.png")
        self.instructions_4 = pygame.image.load("sprites/instructions/instructions-4.png")
        self.instructions_pngs = [self.instructions_1, self.instructions_2, self.instructions_3, self.instructions_4]
        self.instructions_page = 1
        self.player_sprite = pygame.transform.scale(pygame.image.load("sprites/player/player.png"), (72, 45))
        self.coins_sprite = pygame.transform.scale(pygame.image.load("sprites/shop/coin.png"), (45, 45))
        self.health_txt = self.medium_font.render("Health: ", False, (0, 0, 0))
        self.coins_txt = self.medium_font.render(": $100", False, (0, 0, 0))
        self.z1 = pygame.transform.scale(pygame.image.load("sprites/zombie/zombie-regular.png"), (69, 53))
        self.z2 = pygame.transform.scale(pygame.image.load("sprites/zombie/zombie-tank.png"), (95, 71))
        self.z3 = pygame.transform.scale(pygame.image.load("sprites/zombie/zombie-small.png"), (62, 44))

        self.instructions_next_text = self.medium_font.render("Next", False, (0, 0, 0))
        self.instructions_back_text = self.medium_font.render("Back", False, (0, 0, 0))
        self.instructions_menu_text = self.medium_font.render("Menu", False, (0, 0, 0))

        self.reading_instructions = False

        self.difficulty = 2
        self.mode = 1
        self.easy_display = self.medium_font.render("Easy", False, (0, 0, 0))
        self.norm_display = self.medium_font.render("Normal", False, (0, 0, 0))
        self.hard_display = self.medium_font.render("Hard", False, (0, 0, 0))
        self.classic_display = self.medium_font.render("Classic", False, (0, 0, 0))
        self.endless_display = self.medium_font.render("Endless", False, (0, 0, 0))

        self.cloud1_png = pygame.image.load("sprites/misc/cloud1.png")
        self.cloud2_png = pygame.image.load("sprites/misc/cloud2.png")
        self.cloud_choices = [self.cloud1_png, self.cloud2_png]
        self.clouds = []
        for i in range(20):
            if i < 10:
                cloud = Clouds(random.choice(self.cloud_choices), False)
            else:
                cloud = Clouds(random.choice(self.cloud_choices), True)
            self.clouds.append(cloud)
        self.start_time = pygame.time.get_ticks()

    def start_screen(self, events):
        self.screen.fill((22, 22, 22))
        self.screen.blit(self.title_name, (212, 90))
        # 90+37 = 127

        mouse = pygame.mouse.get_pos()

        self.start_button.display(self.screen, mouse)
        self.instruction_button.display(self.screen, mouse)

        if self.start_button.check_click(mouse, events):
            self.start_menu_going = False
        if self.instruction_button.check_click(mouse, events):
            self.reading_instructions = True

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if 405 < mouse[1] < 455:
                    if 250 < mouse[0] < 340:
                        self.difficulty = 1
                    elif 355 < mouse[0] < 445:
                        self.difficulty = 2
                    elif 460 < mouse[0] < 550:
                        self.difficulty = 3
                elif 472 < mouse[1] < 522:
                    if 250 < mouse[0] < 392:
                        self.mode = 1
                    if 408 < mouse[0] < 550:
                        self.mode = 2

    def do_clouds(self):
        for cloud in self.clouds:
            cloud.display(self.screen)
            cloud.move()
            if pygame.time.get_ticks() - self.start_time > 5500:
                cloud.start_time_end = True

    def quit_from_start_menu(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.start_menu_going = False
                self.start_game = False
                return True

    def choose_difficulty_mode(self):
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(250, 405, 90, 50))
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(355, 405, 90, 50))
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(460, 405, 90, 50))
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(250, 405, 90, 50), 3)
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(355, 405, 90, 50), 3)
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(460, 405, 90, 50), 3)

        pygame.draw.rect(self.screen, (255, 255, 0), pygame.Rect(250+((self.difficulty-1)*105), 405, 90, 50), 6)

        self.screen.blit(self.easy_display, (273, 415))
        self.screen.blit(self.norm_display, (365, 415))
        self.screen.blit(self.hard_display, (481, 415))

        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(250, 472, 142, 50))
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(408, 472, 142, 50))
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(250, 472, 142, 50), 3)
        pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(408, 472, 142, 50), 3)

        pygame.draw.rect(self.screen, (255, 255, 0), pygame.Rect(250 + ((self.mode - 1) * 157), 472, 142, 50), 6)

        self.screen.blit(self.classic_display, (288, 483))
        self.screen.blit(self.endless_display, (442, 483))

    def quit_from_end_menu(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.start_menu_going = False
                self.stop = True

    def lose_screen(self):
        self.screen.fill((182, 182, 182))
        self.screen.blit(lose_screen, (162, 207))
        self.screen.blit(self.lose_message1, (340, 50))
        self.screen.blit(self.lose_message2, (240, 100))

    def win_screen(self):
        self.screen.fill((182, 182, 182))
        self.screen.blit(win_screen, (60, 100))
        self.screen.blit(self.win_message1, (200, 20))
        self.screen.blit(self.win_message2, (260, 80))

    def restart_button_display(self, mouse: tuple, events: list, pause: bool = False):
        if pause:
            self.restart_button_from_pause.display(self.screen, mouse)
        else:
            self.restart_button_from_end.display(self.screen, mouse)
            if self.restart_button_from_end.check_click(mouse, events):
                self.restart = True
                self.start_menu_going = False

    def instructions(self, events):
        self.screen.blit(self.instructions_pngs[self.instructions_page-1], (0, 0))
        if not self.instructions_page == 3 and not self.instructions_page == 4:
            pygame.draw.rect(self.screen, (182, 182, 182), pygame.Rect(0, 225, 600, 475))
        if self.instructions_page == 4:
            pygame.draw.rect(self.screen, (182, 182, 182), pygame.Rect(0, 410, 600, 290))
            self.screen.blit(self.z1, (50, 500))
            self.screen.blit(self.z2, (250, 492))
            self.screen.blit(self.z3, (450, 505))

        if not self.instructions_page == len(self.instructions_pngs):
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(520, 10, 70, 40))
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(520, 10, 70, 40), 3)
            self.screen.blit(self.instructions_next_text, (532, 15))
        if not self.instructions_page == 1:
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(10, 10, 70, 40))
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(10, 10, 70, 40), 3)
            self.screen.blit(self.instructions_back_text, (21, 15))
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(265, 10, 70, 40))
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(265, 10, 70, 40), 3)
            self.screen.blit(self.instructions_menu_text, (273, 15))

        if self.instructions_page == 1:
            self.screen.blit(self.player_sprite, (270, 370))
            pygame.draw.line(self.screen, (0, 0, 0), (295, 205), (295, 365), 3)
        if self.instructions_page == 2:
            self.screen.blit(self.health_txt, (7, 230))
            pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(95, 237, 75, 25))
            self.screen.blit(self.coins_sprite, (7, 265))
            self.screen.blit(self.coins_txt, (44, 265))
            self.screen.blit(self.instructions_2_2, (0, 305))

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                mouse = pygame.mouse.get_pos()
                if 520 < mouse[0] < 590 and 10 < mouse[1] < 50:
                    if not self.instructions_page == len(self.instructions_pngs):
                        self.instructions_page += 1
                elif 10 < mouse[0] < 80 and 10 < mouse[1] < 50:
                    if not self.instructions_page == 1:
                        self.instructions_page -= 1
                elif 265 < mouse[0] < 335 and 10 < mouse[1] < 50:
                    if not self.instructions_page == 1:
                        self.instructions_page = 1
                        self.reading_instructions = False

    def to_menu_from_end(self, mouse, events):
        self.menu_button_from_end.display(self.screen, mouse)
        if self.menu_button_from_end.check_click(mouse, events):
            self.start_menu_going = False
            return True


class Clouds:
    def __init__(self, cloud: pygame.surface, left_or_right: bool):
        if left_or_right:
            self.x_pos = random.randint(182, 382)
        else:
            self.x_pos = random.randint(272, 472)
        self.y_pos = random.randint(50, 120)
        self.sprite = cloud
        if self.x_pos + self.sprite.get_width()/2 > 400:
            self.direction = 1
        else:
            self.direction = -1
        self.transparency = 120
        self.sprite.set_alpha(self.transparency)
        self.start_time_end = False
        self.time_since_last_direction_change = 0
        self.multiply = 0.5

    def display(self, screen: pygame.display):
        screen.blit(self.sprite, (self.x_pos, self.y_pos))

    def move(self):
        if self.start_time_end:
            if pygame.time.get_ticks() - self.time_since_last_direction_change > 4000:
                self.direction = random.choice([-1, 1])
                self.time_since_last_direction_change = pygame.time.get_ticks()
            self.x_pos += (self.direction * 0.2)
        else:
            self.x_pos += (self.direction * 0.5)
