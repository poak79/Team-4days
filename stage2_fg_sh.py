import pygame
import sys
import random

def run_stage_2(screen):
    screen_width = 1000
    screen_height = 600
    
    student_width = 33
    student_height = 47
    student_x = 30
    student_y = screen_height - student_height - 10
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
        pygame.Rect(130, 460, 40, 40),
        pygame.Rect(510, 420, 40, 40),
        pygame.Rect(680, 320, 40, 40),
    ]

    collected_stars = 0

    ground1_rect = pygame.Rect(0, 590, 200, 300)
    ground2_rect = pygame.Rect(200, 580, 50, 300)
    ground3_rect = pygame.Rect(250, 560, 50, 300)
    ground4_rect = pygame.Rect(300, 540, 50, 300)
    ground5_rect = pygame.Rect(350, 520, 50, 300)
    ground6_rect = pygame.Rect(400, 500, 50, 300)
    ground7_rect = pygame.Rect(450, 480, 50, 300)
    ground8_rect = pygame.Rect(500, 460, 50, 300)
    ground9_rect = pygame.Rect(550, 440, 50, 300)
    ground10_rect = pygame.Rect(600, 420, 50, 300)
    ground11_rect = pygame.Rect(650, 400, 50, 300)
    ground12_rect = pygame.Rect(700, 380, 50, 300)
    ground13_rect = pygame.Rect(750, 360, 250, 300)

    ground1_image = pygame.image.load("stage2_ground1.png")
    ground1_image = pygame.transform.scale(ground1_image, (200, 300))

    ground2_12_image = pygame.image.load("stage2_ground2_12.png")
    ground2_12_image = pygame.transform.scale(ground2_12_image, (50, 300))

    ground13_image = pygame.image.load("stage2_ground13.png")
    ground13_image = pygame.transform.scale(ground13_image, (250, 300))

    door_image = pygame.image.load("game_door.png")
    door_image = pygame.transform.scale(door_image, (50, 50))
    door_rect = door_image.get_rect(topleft=(900, 310))
    #door_rect = door_image.get_rect(topleft=(150, 530))  # 오류 수정을 위한 빠르게 갈 수 있는 문?

    wh_ghost_image = pygame.image.load("stage2_ghost.png")
    wh_ghost_image = pygame.transform.scale(wh_ghost_image, (30, 40))
    wh_ghost_rect = pygame.Rect(750, 320, 30, 40)
    wh_ghost_direction = 1

    _rain_image = pygame.image.load("stage2_rain.png")
    _rain_image = pygame.transform.scale(_rain_image, (40, 40))

    _rain_rects = []
    _rain_speed = 5
    _rain_spawn_rate = 20 

    bg_image = pygame.image.load("game_BG.png")
    bg_image = pygame.transform.scale(bg_image, (1000, 600))

    clock = pygame.time.Clock()
    frame_count = 0

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
        on_ground = False

        for ground in [ground1_rect, ground2_rect, ground3_rect, ground4_rect, ground5_rect, ground6_rect, ground7_rect, ground8_rect, ground9_rect, ground10_rect, ground11_rect, ground12_rect, ground13_rect]:
            if student_rect.colliderect(ground) and velocity_y >= 0:
                student_y = ground.top - student_height
                velocity_y = 0
                student_jump = False
                on_ground = True

        if not on_ground and not student_jump:
            student_jump = True
            velocity_y = 0

        wh_ghost_rect.x += 2 * wh_ghost_direction
        if wh_ghost_rect.x <= 750 or wh_ghost_rect.x >= 950:
            wh_ghost_direction *= -1

        if student_rect.colliderect(wh_ghost_rect):
            print("유령을 조심하세요! 별 1개 차감됩니다.")
            if collected_stars > 0 : collected_stars -= 1
            student_x = beginning_x
            student_y = beginning_y
            velocity_y = 0
            student_jump = False
            rect_attack_sound.play()

        frame_count += 1
        if frame_count % _rain_spawn_rate == 0:
            _rain_x = random.randint(200, 700)
            _rain_rect = pygame.Rect(_rain_x, -40, 40, 40)
            _rain_rects.append(_rain_rect)

        for _rain_rect in _rain_rects:
            _rain_rect.y += _rain_speed + 1

            if student_rect.colliderect(_rain_rect):
                print("빗물을 조심하세요! 별 1개 차감됩니다.")
                if collected_stars > 0 : collected_stars -= 1
                student_x = beginning_x
                student_y = beginning_y
                velocity_y = 0
                student_jump = False
                rect_attack_sound.play()
                _rain_rects.clear()
                break

            if _rain_rect.y > screen_height:
                _rain_rects.remove(_rain_rect)

        if student_rect.colliderect(door_rect):
            print("게임 클리어! 두 번째 스테이지 완료.")
            return collected_stars

        for star in stars[:]:
            if student_rect.colliderect(star):
                stars.remove(star)
                collected_stars += 1
                collect_star_sound.play()
                print(f"별을 획득했습니다! 현재 별 개수: {collected_stars}")

        screen.blit(bg_image, (0, 0))
        screen.blit(current_student_image, (student_x, student_y))

        screen.blit(ground1_image, ground1_rect.topleft)
        screen.blit(ground2_12_image, ground2_rect.topleft)
        screen.blit(ground2_12_image, ground3_rect.topleft)
        screen.blit(ground2_12_image, ground4_rect.topleft)
        screen.blit(ground2_12_image, ground5_rect.topleft)
        screen.blit(ground2_12_image, ground6_rect.topleft)
        screen.blit(ground2_12_image, ground7_rect.topleft)
        screen.blit(ground2_12_image, ground8_rect.topleft)
        screen.blit(ground2_12_image, ground9_rect.topleft)
        screen.blit(ground2_12_image, ground10_rect.topleft)
        screen.blit(ground2_12_image, ground11_rect.topleft)
        screen.blit(ground2_12_image, ground12_rect.topleft)
        screen.blit(ground13_image, ground13_rect.topleft)

        screen.blit(door_image, door_rect.topleft)

        screen.blit(wh_ghost_image, wh_ghost_rect.topleft)

        for _rain_rect in _rain_rects:
            screen.blit(_rain_image, _rain_rect.topleft)

        for star in stars:
            if star.x >= 0:
                screen.blit(star_image, star.topleft)

        score_text = star_score_font.render(f"     : {collected_stars}", True, CL_BLACK)
        screen.blit(score_text, (50, 20))

        pygame.display.flip()
        clock.tick(60)
