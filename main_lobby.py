import pygame
import sys

def main_lobby(screen, run_game_stages):
    pygame.mixer.init()

    pygame.mixer.music.load("main_lobby_bgm.mp3")
    pygame.mixer.music.play(-1)

    mouse_one_click_sound = pygame.mixer.Sound("mouse_sound.wav")

    game_guide_image = pygame.image.load("game_guide.png")
    game_guide_image = pygame.transform.scale(game_guide_image, (550, 500))

    bg_image = pygame.image.load("main_lobby_screen.png")
    bg_image = pygame.transform.scale(bg_image, (1000, 600))

    start_bt_image = pygame.image.load("game_start_bt.png")
    start_bt_image = pygame.transform.scale(start_bt_image, (180, 50))

    guide_bt_image = pygame.image.load("game_guide_bt.png")
    guide_bt_image = pygame.transform.scale(guide_bt_image, (180, 50))

    quit_bt_image = pygame.image.load("game_quit_bt.png")
    quit_bt_image = pygame.transform.scale(quit_bt_image, (180, 50))

    start_bt_rect = start_bt_image.get_rect(center=(500, 425))
    guide_bt_rect = guide_bt_image.get_rect(center=(500, 490))
    quit_bt_rect = quit_bt_image.get_rect(center=(500, 555)) 

    show_guide = False
    bgm_stopped = False  

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_bt_rect.collidepoint(mouse_pos) and not bgm_stopped:
                    pygame.mixer.music.stop()
                    bgm_stopped = True
                    mouse_one_click_sound.play()  
                    run_game_stages(screen)  
                    return  
                elif guide_bt_rect.collidepoint(mouse_pos):
                    show_guide = True
                    mouse_one_click_sound.play()  
                elif quit_bt_rect.collidepoint(mouse_pos):
                    mouse_one_click_sound.play()  
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN and show_guide:
                show_guide = False

        screen.blit(bg_image, (0, 0))

        screen.blit(start_bt_image, start_bt_rect.topleft) 
        screen.blit(guide_bt_image, guide_bt_rect.topleft)  
        screen.blit(quit_bt_image, quit_bt_rect.topleft)  

        if show_guide:
            screen.blit(game_guide_image, (220,50))

        pygame.display.flip()
