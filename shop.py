import pygame

shop_img = pygame.image.load("sprites/shop/shop.png")
coin_img = pygame.image.load("sprites/shop/coin.png")

pygame.font.init()

font = pygame.font.SysFont("Arial", 18)
shotgun_cost_display = font.render("$250", False, (0, 0, 0))
machine_gun_cost_display = font.render("$350", False, (0, 0, 0))
sniper_cost_display = font.render("$500", False, (0, 0, 0))
rocket_launcher_cost_display = font.render("$750", False, (0, 0, 0))


class Shop:
    def __init__(self):
        self.selected_str = font.render("Selected", False, (0, 0, 0))
        self.unlocked_str = font.render("Unlocked", False, (0, 0, 0))
        self.first_aid_price = font.render("$500", False, (0, 0, 0))

        self.costs = [0,
                      shotgun_cost_display,
                      machine_gun_cost_display,
                      sniper_cost_display,
                      rocket_launcher_cost_display]
        self.costs_ints = [0, 250, 350, 500, 750]
        self.color = (0, 0, 0)

    def background_colors(self, screen: pygame.display, gun_data: list, money: int):
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(100, 600, 600, 100))
        for i in range(5):
            if gun_data[i] == 2:
                self.color = (255, 243, 109)
            elif gun_data[i] == 1:
                self.color = (165, 201, 253)
            else:
                if money >= self.costs_ints[i]:
                    self.color = (151, 252, 151)
                else:
                    self.color = (255, 127, 127)
            pygame.draw.rect(screen, self.color, pygame.Rect(100 + ((i+1)*16) + (i*80), 610, 82, 80))
        if money >= 500:
            self.color = (151, 252, 151)
        else:
            self.color = (255, 127, 127)
        pygame.draw.rect(screen, self.color, pygame.Rect(610, 610, 81, 80))

    def display(self, screen: pygame.display):
        screen.blit(shop_img, (100, 600))
        screen.blit(coin_img, (11, 34))
        screen.blit(self.first_aid_price, (635, 667))

    def display_text(self, screen: pygame.display, gun_data: list):
        i = 1
        while i < 6:
            if gun_data[i-1] == 2:
                screen.blit(self.selected_str, (100 + (15 + (i*16) + ((i-1)*80)), 667))
            elif gun_data[i-1] == 1:
                screen.blit(self.unlocked_str, (100 + (15 + (i*16) + ((i-1)*80)), 667))
            elif gun_data[i-1] == 0:
                screen.blit(self.costs[i-1], (100 + (30 + (i*16) + ((i-1)*80)), 667))
            i += 1

    def handle_buying_and_switching_guns(self, gun_data: list, gun_int: int, money: int, mouse_pos: tuple, key: int = -1):
        if key == -1:
            i = 1
            while i < 6:
                if (100 + (i*16) + ((i-1)*80)) < mouse_pos[0] < 100 + ((i*16) + ((i-1)*80)) + 80:
                    if 610 < mouse_pos[1] < 690:
                        if gun_int == i-1:
                            return 0, 0, 0
                        elif gun_data[i-1] == 1:
                            return 1, (i-1), 0
                        elif gun_data[i-1] == 0:
                            if money >= self.costs_ints[i-1]:
                                return 2, (i-1), self.costs_ints[i-1]
                            else:
                                return 0, 0, 0
                i += 1
            return 0, 0, 0
        else:
            if gun_int == key:
                return 0, 0, 0
            elif gun_data[key] == 1:
                return 1, key, 0
            elif gun_data[key] == 0:
                if money >= self.costs_ints[key]:
                    return 2, key, self.costs_ints[key]
                else:
                    return 0, 0, 0

    @staticmethod
    def handle_buying_first_aid(money: int, click: bool = True):
        if click:
            mouse_pos = pygame.mouse.get_pos()
            if 610 < mouse_pos[0] < 690:
                if 610 < mouse_pos[1] < 690:
                    if money >= 500:
                        return True
        else:
            if money >= 500:
                return True
        return False
