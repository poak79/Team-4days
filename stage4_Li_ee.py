import pygame
import sys
import random

def run_stage_4(screen):
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

    student_image_idle = pygame.image.load("KNU_Student.png")
    student_image_idle = pygame.transform.scale(student_image_idle, (student_width, student_height))
    
    student_image_right = pygame.image.load("KNU_Student_right.PNG")
    student_image_right = pygame.transform.scale(student_image_right, (42, 55))

    student_image_left = pygame.image.load("KNU_Student_left.PNG")
    student_image_left = pygame.transform.scale(student_image_left, (42, 58))

    current_student_image = student_image_idle
    
    star_image = pygame.image.load("star.png")
    star_image = pygame.transform.scale(star_image, (40, 40))

    stars = [
        pygame.Rect(350, 350, 40, 40),
        pygame.Rect(700, 450, 40, 40),
    ]

    collected_stars = 0

    ground1_rect = pygame.Rect(0, 500, 1000, 100)

    ground1_image = pygame.image.load("stage4_ground1.png")
    ground1_image = pygame.transform.scale(ground1_image, (1000, 100))

    door_rect = pygame.Rect(950, 450, 50, 50)
    door_image = pygame.image.load("game_door.png")
    door_image = pygame.transform.scale(door_image, (50, 50))
    door_rect = door_image.get_rect(topleft=(950, 450))
    #door_rect = door_image.get_rect(topleft=(150, 450))  # 오류 수정을 위한 빠르게 갈 수 있는 문?

    _roket_image = pygame.image.load("stage4_rocket.png")
    _roket_image = pygame.transform.scale(_roket_image, (40, 40))

    _roket_rects = []
    _roket_speed = 5
    _roket_spawn_rate = 65

    bg_image = pygame.image.load("game_BG.png")
    bg_image = pygame.transform.scale(bg_image, (1000,600))

    clock = pygame.time.Clock()
    frame_count = 0

    pygame.mixer.init()

    collect_star_sound = pygame.mixer.Sound("collect_star_.wav")

    rect_attack_sound = pygame.mixer.Sound("rect_attack.wav")

    student_jump_sound = pygame.mixer.Sound("student_jump_.wav")

    bgm_stopped = False

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
            current_student_image = student_image_idle
        
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

        player_rect = pygame.Rect(student_x, student_y, student_width, student_height)
        on_platform = False
        
        for platform in [ground1_rect]:
            if player_rect.colliderect(platform) and velocity_y >= 0:
                student_y = platform.top - student_height
                velocity_y = 0
                student_jump = False
                on_platform = True

        if not on_platform and not student_jump:
            student_jump = True
            velocity_y = 0

        frame_count += 1
        if frame_count % _roket_spawn_rate == 0:
            _roket_y = random.choice([350, 400, 450])
            _roket_rect = pygame.Rect(screen_width, _roket_y, 40, 40)
            _roket_rects.append(_roket_rect)

        for _roket_rect in _roket_rects[:]:
            _roket_rect.x -= _roket_speed

            if player_rect.colliderect(_roket_rect):
                print("로켓을 조심하세요! 별 1개 차감됩니다.")
                if collected_stars > 0 : collected_stars -= 1
                student_x = beginning_x
                student_y = beginning_y
                velocity_y = 0
                student_jump = False
                rect_attack_sound.play()
                _roket_rects.remove(_roket_rect)
                break

            if _roket_rect.x < 0:
                _roket_rects.remove(_roket_rect)

        for star in stars[:]:
            if player_rect.colliderect(star):
                stars.remove(star)
                collected_stars += 1
                collect_star_sound.play()
                print(f"별을 획득했습니다! 현재 별 개수: {collected_stars}")

        if player_rect.colliderect(door_rect) and not bgm_stopped:
            pygame.mixer.music.stop()
            bgm_stopped = True
            print("게임 클리어! 네 번째 스테이지 완료.")
            return collected_stars

        screen.blit(bg_image, (0, 0))
        screen.blit(current_student_image, (student_x, student_y))
        screen.blit(ground1_image, ground1_rect.topleft)
        screen.blit(door_image, door_rect.topleft)

        for _roket_rect in _roket_rects:
            screen.blit(_roket_image, _roket_rect.topleft)

        for star in stars:
            screen.blit(star_image, star.topleft)

        score_text = star_score_font.render(f"     : {collected_stars}", True, CL_BLACK)
        screen.blit(score_text, (50, 20))

        pygame.display.flip()
        clock.tick(60)
