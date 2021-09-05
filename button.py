import pygame


class Button:
    def __init__(self, text: str, font: pygame.font, size: tuple, pos: tuple,
                 color1: tuple = (255, 255, 255), color2: tuple = (114, 114, 114), growth: int = 10):
        self.text = font.render(text, False, (0, 0, 0))
        self.size = size
        self.reg_size = size
        self.changed_size = (self.reg_size[0] + growth, self.reg_size[1] + growth)
        self.pos = pos
        self.color = color1
        self.reg_color = color1
        self.changed_color = color2
        self.text_pos = (self.pos[0]-(self.text.get_width()/2), self.pos[1]-(self.text.get_height()/2))

    def display(self, screen: pygame.display, mouse: tuple):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos[0] - (self.size[0] / 2),
                                                         self.pos[1] - (self.size[1] / 2), self.size[0], self.size[1]))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(self.pos[0] - (self.size[0] / 2),
                                                        self.pos[1] - (self.size[1] / 2),
                                                        self.size[0], self.size[1]), 3)
        screen.blit(self.text, self.text_pos)

        if self.pos[0] - (self.size[0] / 2) < mouse[0] < self.pos[0] + (self.size[0] / 2) and \
                self.pos[1] - (self.size[1] / 2) < mouse[1] < self.pos[1] + (self.size[1] / 2):
            self.size = self.changed_size
            self.color = self.changed_color
        else:
            self.size = self.reg_size
            self.color = self.reg_color

    def check_click(self, mouse: tuple, events: list):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.pos[0] - (self.size[0] / 2) < mouse[0] < self.pos[0] + (self.size[0] / 2) and \
                        self.pos[1] - (self.size[1] / 2) < mouse[1] < self.pos[1] + (self.size[1] / 2):
                    return True
