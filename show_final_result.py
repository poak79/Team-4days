import pygame
import sys

def show_final_result(screen, collected_stars):
    dw_font_DGM = "C:\\Users\\park0\\OneDrive\\바탕 화면\\DungGeunMo.ttf"
    font_size1 = 250
    font_size2 = 20
    score_font = pygame.font.Font(dw_font_DGM, font_size1)
    continue_font = pygame.font.Font(dw_font_DGM, font_size2)
    
    pygame.mixer.init()
    pygame.mixer.music.load("show_final.wav")
    pygame.mixer.music.play(1)  

    clock = pygame.time.Clock()
    collected_stars = int(collected_stars)

    bg_image = pygame.image.load("final_show.png")
    bg_image = pygame.transform.scale(bg_image, (1000, 600))

    my_grade = "F"
    my_score = collected_stars
    if my_score >= 11:
        my_grade = "A+"
    elif 5 <= my_score <= 10:
        my_grade = "B+"
    elif 1 <= my_score <= 4:
        my_grade = "C+"
    else:
        my_grade = "F"

    result_text_score = score_font.render(f"     {my_grade}", True, (255, 255, 153))
    continue_text = continue_font.render("메인 로비로 가려면 아무 키나 눌러주세요!",True, (255, 255, 153))
    
    start_time = pygame.time.get_ticks()

    show_text = False 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and show_text:
                return
        
        _now_time = pygame.time.get_ticks()
        if _now_time - start_time >= 3000:
            show_text = True

        screen.blit(bg_image, (0, 0))

        if show_text:
            screen.blit(result_text_score, (25, 95))
            screen.blit(continue_text, ((1000 - continue_text.get_width()) // 2, 400)) 
        
        pygame.display.flip()
        clock.tick(60)
