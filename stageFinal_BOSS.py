import pygame
import sys
import random

def run_stage_5(screen, collected_stars):
    screen_width = 1000
    screen_height = 600

    student_width = 33
    student_height = 47
    student_x = 30
    student_y = 450
    student_speed = 5
    student_jump = False
    jump_height = 10
    student_gravity = 0.5
    velocity_y = 0

    CL_BLACK = (0, 0, 0)
    CL_RED = (255, 0, 0)

    student_image_idle = pygame.image.load("KNU_Student.png")
    student_image_idle = pygame.transform.scale(student_image_idle, (student_width, student_height))
    
    student_image_right = pygame.image.load("KNU_Student_right.PNG")
    student_image_right = pygame.transform.scale(student_image_right, (42, 55))

    student_image_left = pygame.image.load("KNU_Student_left.PNG")
    student_image_left = pygame.transform.scale(student_image_left, (42, 58))

    current_student_image = student_image_idle

    ground1_rect = pygame.Rect(0, 500, 1000, 100)

    ground1_image = pygame.image.load("stage4_ground1.png")
    ground1_image = pygame.transform.scale(ground1_image, (1000, 100))

    door_image = pygame.image.load("game_door.png")
    door_image = pygame.transform.scale(door_image, (50, 50))
    door_rect = door_image.get_rect(topleft=(950, 450))

    st_boss_image = pygame.image.load("stage_Boss_senior.png")
    st_boss_image = pygame.transform.scale(st_boss_image, (120, 180))
    st_boss_face_image = pygame.image.load("stage_final_face.png")
    st_boss_face_image = pygame.transform.scale(st_boss_face_image, (40, 41))
    st_boss_face_rect = st_boss_face_image.get_rect(topleft=(160, 10))
    st_boss_rect = st_boss_image.get_rect(topleft=(750, 320))
    st_boss_health = 40

    _bullets = []
    _bullet_speed = 10
    _bullet_width = 10
    _bullet_height = 5
    last_shot_time = 0
    shot_interval = 300

    YL_ghost_rects = []
    YL_ghost_speed = 2
    YL_ghost_image = pygame.image.load("stage_boss_Y_ghost.png")
    YL_ghost_image = pygame.transform.scale(YL_ghost_image, (30, 30))

    YL_bus_rects = []
    YL_bus_speed = -5
    YL_bus_image = pygame.image.load("stage_boss_bus.png")
    YL_bus_image = pygame.transform.scale(YL_bus_image, (70, 30))
    YL_bus_shot_time = 0

    bg_image = pygame.image.load("game_BG.png")
    bg_image = pygame.transform.scale(bg_image, (1000, 600))

    clock = pygame.time.Clock()
    score_boss_font = pygame.font.Font(None, 36) 
    
    pygame.mixer.init()
    pygame.mixer.music.load("boss_bgm.mp3")
    pygame.mixer.music.play(-1)

    bgm_stopped = False

    rect_attack_sound = pygame.mixer.Sound("rect_attack.wav")
    gun_sound_sound = pygame.mixer.Sound("gun_sound.wav")
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
            current_student_image = student_image_idle
        
        if keys[pygame.K_SPACE] and not student_jump:
            student_jump = True
            velocity_y = -jump_height
            student_jump_sound.play()
        if keys[pygame.K_z]:
            current_time = pygame.time.get_ticks()
            
            if current_time - last_shot_time > shot_interval:
                bullet_x = student_x + student_width
                bullet_y = student_y + student_height // 2 - _bullet_height // 2
                _bullets.append(pygame.Rect(bullet_x, bullet_y, _bullet_width, _bullet_height))
                last_shot_time = current_time
                gun_sound_sound.play()

        if student_x < 0:
            student_x = 0
        if student_x > screen_width - student_width:
            student_x = screen_width - student_width

        if student_jump:
            student_y += velocity_y
            velocity_y += student_gravity

        student_rect = pygame.Rect(student_x, student_y, student_width, student_height)
        on_platform = False
        
        if student_rect.colliderect(ground1_rect) and velocity_y >= 0:
            student_y = ground1_rect.top - student_height
            velocity_y = 0
            student_jump = False
            on_platform = True

        if not on_platform and not student_jump:
            student_jump = True
            velocity_y = 0

        if student_rect.colliderect(door_rect)and not bgm_stopped:
            pygame.mixer.music.stop()
            bgm_stopped = True
            return collected_stars

        for bullet in _bullets[:]:
            bullet.x += _bullet_speed
            if bullet.x > screen_width:
                _bullets.remove(bullet)
            if st_boss_rect and st_boss_rect.colliderect(bullet):
                _bullets.remove(bullet)
                st_boss_health -= 1
                if st_boss_health <= 0:
                    print("보스를 처치했습니다!")
                    st_boss_rect = None
                    YL_ghost_rects.clear()
                    YL_bus_rects.clear()

        current_time = pygame.time.get_ticks()
        if st_boss_rect and current_time - YL_bus_shot_time > 2000:
            YL_bus_rects.append(pygame.Rect(700, 470, 70, 30))
            YL_bus_shot_time = current_time

        for YL_bus_rect in YL_bus_rects[:]:
            YL_bus_rect.x += YL_bus_speed
            if YL_bus_rect.x < 0:
                YL_bus_rects.remove(YL_bus_rect)
            elif YL_bus_rect.colliderect(student_rect):
                YL_bus_rects.remove(YL_bus_rect)
                if collected_stars > 0 :
                    collected_stars -= 1
                    rect_attack_sound.play()

        if st_boss_rect and random.random() < 0.05:
            YL_ghost_x = random.randint(0, 500)
            YL_ghost_rects.append(pygame.Rect(YL_ghost_x, 0, 30, 30))

        for YL_ghost_rect in YL_ghost_rects[:]:
            YL_ghost_rect.y += YL_ghost_speed
            if YL_ghost_rect.colliderect(student_rect):
                YL_ghost_rects.remove(YL_ghost_rect)
                if collected_stars > 0 :
                    collected_stars -= 1
                    rect_attack_sound.play()
            if YL_ghost_rect.y > 470:
                YL_ghost_rects.remove(YL_ghost_rect)

        screen.blit(bg_image, (0, 0))
        screen.blit(current_student_image, (student_x, student_y))
        screen.blit(ground1_image, ground1_rect.topleft)

        for YL_ghost_rect in YL_ghost_rects:
            screen.blit(YL_ghost_image, YL_ghost_rect.topleft)

        for YL_bus_rect in YL_bus_rects:
            screen.blit(YL_bus_image, YL_bus_rect.topleft)

        for bullet in _bullets:
            pygame.draw.rect(screen, CL_RED, bullet)

        if not st_boss_rect:
            screen.blit(door_image, door_rect.topleft)
        
        if st_boss_rect:
            screen.blit(st_boss_image, st_boss_rect.topleft)
            screen.blit(st_boss_face_image, st_boss_face_rect.topleft)

            health_text = score_boss_font.render(f": {st_boss_health}", True, CL_BLACK)
            screen.blit(health_text, (220, 20))
  

        score_text = score_boss_font.render(f"     : {collected_stars}", True, CL_BLACK)
        screen.blit(score_text, (50, 20))

        pygame.display.flip()
        clock.tick(60)
