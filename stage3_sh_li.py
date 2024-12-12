import pygame
import sys

def run_stage_3(screen):
    screen_width = 1000
    screen_height = 600

    student_width = 33
    student_height = 47
    student_x = 30
    student_y = 450
    student_speed = 5
    student_jump = False
    jump_height = 9
    student_gravity = 0.5
    velocity_y = 0

    beginning_x = student_x
    beginning_y = student_y

    CL_BLACK = (0, 0, 0)

    pygame.font.init()
    star_score_font = pygame.font.Font(None, 36)

    student_image_or = pygame.image.load("KNU_Student.png")
    student_image_or = pygame.transform.scale(student_image_or, (student_width, student_height))

    student_image_right = pygame.image.load("KNU_Student_right.PNG")
    student_image_right = pygame.transform.scale(student_image_right, (42, 55))

    student_image_left = pygame.image.load("KNU_Student_left.PNG")
    student_image_left = pygame.transform.scale(student_image_left, (42, 58))

    current_student_image = student_image_or

    star_image = pygame.image.load("star.png")
    star_image = pygame.transform.scale(star_image, (40, 40))
    stars = [
        pygame.Rect(200, 460, 40, 40),
        pygame.Rect(430, 260, 40, 40),
        pygame.Rect(350, 50, 40, 40),
        pygame.Rect(900, 500, 40, 40)
    ]

    collected_stars = 0

    ground1_rect = pygame.Rect(0, 500, 250, 100)
    ground2_rect = pygame.Rect(380, 500, 50, 10)
    ground3_rect = pygame.Rect(600, 500, 50, 10)
    ground4_rect = pygame.Rect(750, 500, 50, 10)
    ground5_rect = pygame.Rect(900, 350, 200, 10)
    ground6_rect = pygame.Rect(820, 420, 200, 10)
    ground7_rect = pygame.Rect(640, 350, 80, 10)
    ground8_rect = pygame.Rect(790, 300, 50, 10)
    ground9_rect = pygame.Rect(570, 250, 100, 10)
    ground10_rect = pygame.Rect(400, 300, 100, 10)
    ground11_rect = pygame.Rect(100, 300, 200, 10)
    ground12_rect = pygame.Rect(0, 250, 100, 10)
    ground13_rect = pygame.Rect(0, 150, 100, 10)
    ground14_rect = pygame.Rect(250, 100, 200, 10)
    ground15_rect = pygame.Rect(700, 100, 400, 10)
    ground16_rect = pygame.Rect(580, 100, 30, 10)
    ground17_rect = pygame.Rect(850, 540, 100, 10)

    ground1_image = pygame.image.load("stage3_ground1.png")
    ground1_image = pygame.transform.scale(ground1_image, (250, 100))

    ground3_1_image = pygame.image.load("stage3_ground_WH_31.png")
    ground3_1_image = pygame.transform.scale(ground3_1_image, (30, 10))

    ground5_1_image = pygame.image.load("stage3_ground_WH_51.png")
    ground5_1_image = pygame.transform.scale(ground5_1_image, (50, 10))

    ground8_1_image = pygame.image.load("stage3_ground_WH_81.png")
    ground8_1_image = pygame.transform.scale(ground5_1_image, (80, 10))

    ground10_1_image = pygame.image.load("stage3_ground_WH_101.png")
    ground10_1_image = pygame.transform.scale(ground5_1_image, (100, 10))

    ground20_1_image = pygame.image.load("stage3_ground_WH_201.png")
    ground20_1_image = pygame.transform.scale(ground5_1_image, (200, 10))

    ground40_1_image = pygame.image.load("stage3_ground_WH_401.png")
    ground40_1_image = pygame.transform.scale(ground5_1_image, (400, 10))

    door_rect = pygame.Rect(950, 50, 50, 50)
    door_image = pygame.image.load("game_door.png")
    door_image = pygame.transform.scale(door_image, (50, 50))
    door_rect = door_image.get_rect(topleft=(900, 50))
    #door_rect = door_image.get_rect(topleft=(150, 400))  # 오류 수정을 위한 빠르게 갈 수 있는 문?
    
    a_trick_rect = pygame.Rect(570, 350, 70, 10)

    trickground_image = pygame.image.load("stage3_trickground.png")
    trickground_image = pygame.transform.scale(trickground_image, (70, 10))   


    _pond_rect = pygame.Rect(250, 560, 800, 50)
    _pond_image = pygame.image.load("stage3_water.png")
    _pond_image = pygame.transform.scale(_pond_image, (800, 50))

    bg_image = pygame.image.load("game_BG.png")
    bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))

    clock = pygame.time.Clock()

    pygame.mixer.init()

    collect_star_sound = pygame.mixer.Sound("collect_star_.wav")

    rect_attack_sound = pygame.mixer.Sound("rect_attack.wav")

    student_jump_sound = pygame.mixer.Sound("student_jump_.wav")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            student_x -= student_speed
            current_student_image = student_image_left
        elif keys[pygame.K_RIGHT]:
            student_x += student_speed
            current_student_image = student_image_right
        else:
            current_student_image = student_image_or

        if keys[pygame.K_SPACE] and not student_jump:
            student_jump = True
            velocity_y = -jump_height
            student_jump_sound.play()

        if student_x < 0:
            student_x = 0
        if student_x > screen_width - student_width:
            student_x = screen_width - student_width

        if student_jump:
            student_y += velocity_y
            velocity_y += student_gravity

        student_rect = pygame.Rect(student_x, student_y, student_width, student_height)
        on_platform = False
        for ground in [ground1_rect, ground2_rect, ground3_rect,
                       ground4_rect, ground5_rect, ground6_rect, 
                       ground7_rect, ground8_rect, ground9_rect, 
                       ground10_rect, ground11_rect, ground12_rect, 
                       ground13_rect, ground14_rect, ground15_rect, 
                       ground16_rect,ground17_rect]:
            if student_rect.colliderect(ground) and velocity_y >= 0:
                student_y = ground.top - student_height
                velocity_y = 0
                student_jump = False
                on_platform = True

        if not on_platform and not student_jump:
            student_jump = True
            velocity_y = 0

        for star in stars[:]:
            if student_rect.colliderect(star):
                stars.remove(star)
                collected_stars += 1
                collect_star_sound.play()
                print(f"별을 획득했습니다! 현재 별 개수: {collected_stars}")

        if student_rect.colliderect(door_rect):
            print("게임 클리어! 세 번째 스테이지 완료.")
            return collected_stars

        if student_rect.colliderect(_pond_rect):
            print("연못에 빠지지 않게 조심하세요! 별 1개 차감됩니다.")
            if collected_stars > 0 : collected_stars -= 1
            student_x = beginning_x
            student_y = beginning_y
            student_jump = False
            rect_attack_sound.play()
            velocity_y = 0

        screen.blit(bg_image, (0, 0))
        screen.blit(current_student_image, (student_x, student_y))
        screen.blit(ground1_image, ground1_rect.topleft)
        screen.blit(ground5_1_image, ground2_rect.topleft)
        screen.blit(ground5_1_image, ground3_rect.topleft)
        screen.blit(ground5_1_image, ground4_rect.topleft)
        screen.blit(ground20_1_image, ground5_rect.topleft)
        screen.blit(ground20_1_image, ground6_rect.topleft)
        screen.blit(ground8_1_image, ground7_rect.topleft)
        screen.blit(ground5_1_image, ground8_rect.topleft)
        screen.blit(ground10_1_image, ground9_rect.topleft)
        screen.blit(ground10_1_image, ground10_rect.topleft)
        screen.blit(ground20_1_image, ground11_rect.topleft)
        screen.blit(ground10_1_image, ground12_rect.topleft)
        screen.blit(ground10_1_image, ground13_rect.topleft)
        screen.blit(ground20_1_image, ground14_rect.topleft)
        screen.blit(ground40_1_image, ground15_rect.topleft)
        screen.blit(ground3_1_image, ground16_rect.topleft)
        screen.blit(trickground_image, a_trick_rect.topleft)
        screen.blit(ground10_1_image, ground17_rect.topleft)

        screen.blit(door_image, door_rect.topleft)
        screen.blit(_pond_image, _pond_rect.topleft)

        for star in stars:
            screen.blit(star_image, star.topleft)


        score_text = star_score_font.render(f"     : {collected_stars}", True, CL_BLACK)
        screen.blit(score_text, (50, 20))

        pygame.display.flip()
        clock.tick(60)
