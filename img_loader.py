import pygame


class ImgLoad:
    def __init__(self):
        return

    @staticmethod
    def load(screen: pygame.display):
        player = pygame.image.load("sprites/player/player.png").convert_alpha(screen)
        zombie_regular = pygame.image.load("sprites/zombie/zombie-regular.png").convert_alpha(screen)
        zombie_tank = pygame.image.load("sprites/zombie/zombie-tank.png").convert_alpha(screen)
        zombie_small = pygame.image.load("sprites/zombie/zombie-small.png").convert_alpha(screen)
        rocket = pygame.image.load("sprites/player/rocket.png")
        explosion = pygame.image.load("sprites/player/explosion.png").convert_alpha(screen)
        shop_img = pygame.image.load("sprites/shop/shop.png").convert_alpha(screen)
        coin_img = pygame.image.load("sprites/shop/coin.png").convert_alpha(screen)

        return player, zombie_regular, zombie_tank, zombie_small, rocket, explosion, shop_img, coin_img
