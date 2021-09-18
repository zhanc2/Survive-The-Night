import pygame
from game import Game
from start_end import StartEnd
from img_loader import ImgLoad


pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800, 700))

load_Img = ImgLoad()
sprites = load_Img.load(screen)

first_layer = True
while first_layer:
    start_end = StartEnd(screen)
    while start_end.start_menu_going:
        events = pygame.event.get()
        if start_end.reading_instructions:
            start_end.instructions(events)
        else:
            start_end.start_screen(events)
            start_end.choose_difficulty_mode()
            start_end.do_clouds()
        if start_end.quit_from_start_menu(events):
            first_layer = False
        pygame.display.flip()

    if start_end.start_game:
        not_quit = True

        while not_quit:
            start_end.restart = False
            game = Game(screen, start_end.difficulty, start_end.mode, sprites[0], sprites[1], sprites[2], sprites[3],
                        sprites[4], sprites[5])

            while game.running:
                mouse = pygame.mouse.get_pos()
                events = pygame.event.get()
                keys = pygame.key.get_pressed()
                if game.paused:
                    dt = game.clock.tick(120)
                    paused = game.check_game_paused(mouse, events)
                    if paused == 0:
                        not_quit = False
                        first_layer = False
                    elif paused == 1:
                        break
                    start_end.restart_button_display(mouse, events, True)
                    if game.back_to_menu_from_paused(mouse, events):
                        not_quit = False
                else:
                    dt = game.clock.tick(120)
                    game.background()
                    # game.do_map()
                    if game.check_inputs(events, keys, mouse) == 0:
                        not_quit = False
                        first_layer = False
                    game.handle_player(dt, mouse)
                    game.update_camera()
                    game.handle_bullet_spawning(mouse)
                    game.handle_bullet_general(dt)
                    game.handle_zombie_spawning()
                    game.handle_zombies_general(dt)
                    game.check_game_end()
                    game.display_round()
                    game.display_shop()
                    game.handle_explosions()
                    game.replace_cursor(mouse)

                pygame.display.flip()

            if not game.won_or_lose == 0:
                pygame.mouse.set_visible(True)
                start_end.start_menu_going = True
                while start_end.start_menu_going:
                    mouse = pygame.mouse.get_pos()
                    events = pygame.event.get()
                    start_end.quit_from_end_menu(events)
                    if game.won_or_lose == 1:
                        start_end.win_screen()
                    elif game.won_or_lose == 2:
                        start_end.lose_screen()
                    if start_end.stop:
                        not_quit = False
                        first_layer = False
                    start_end.restart_button_display(mouse, events)
                    if start_end.to_menu_from_end(mouse, events):
                        not_quit = False
                    if start_end.restart:
                        break
                    pygame.display.flip()
