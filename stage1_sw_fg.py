import pygame
import sys

def run_stage_1(screen):
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

    student_image_or = pygame.image.load("KNU_Student.PNG")  
    student_image_or = pygame.transform.scale(student_image_or, (student_width, student_height))

    student_image_right = pygame.image.load("KNU_Student_right.PNG")
    student_image_right = pygame.transform.scale(student_image_right, (42, 55))

    student_image_left = pygame.image.load("KNU_Student_left.PNG")
    student_image_left = pygame.transform.scale(student_image_left, (42, 58))

    current_student_image = student_image_or

    star_image = pygame.image.load("star.png")
    star_image = pygame.transform.scale(star_image, (40, 40))

    stars = [
        pygame.Rect(600, 40, 40, 40),
        pygame.Rect(880, 340, 40, 40),
        pygame.Rect(530, 310, 40, 40),
        pygame.Rect(700, 430, 40, 40),
        pygame.Rect(300, 430, 40, 40),

    ]

    collected_stars = 0

    ground1_rect = pygame.Rect(0, 550, 800, 50)
    ground2_rect = pygame.Rect(880, 500, 160, 5)
    ground3_rect = pygame.Rect(860, 380, 160, 5)
    ground4_rect = pygame.Rect(0, 350, 750, 40)
    ground5_rect = pygame.Rect(50, 280, 100, 20)
    ground6_rect = pygame.Rect(150, 180, 100, 20)
    ground7_rect = pygame.Rect(250, 80, 800, 40)

    ground1_image = pygame.image.load("stage1_ground1.png")
    ground1_image = pygame.transform.scale(ground1_image, (800, 50))

    ground2and3_image = pygame.image.load("stage1_ground2and3.png")
    ground2and3_image = pygame.transform.scale(ground2and3_image, (160, 20))

    ground4_image = pygame.image.load("stage1_ground4.png")
    ground4_image = pygame.transform.scale(ground4_image, (750, 40))

    ground5and6_image = pygame.image.load("stage1_ground5and6.png")
    ground5and6_image = pygame.transform.scale(ground5and6_image, (100, 20))  

    ground7_image = pygame.image.load("stage1_ground7.png")
    ground7_image = pygame.transform.scale(ground7_image, (800, 40))

    door_image = pygame.image.load("game_door.png")
    door_image = pygame.transform.scale(door_image, (50, 50))
    door_rect = door_image.get_rect(topleft=(900, 30))
    #door_rect = door_image.get_rect(topleft=(150, 400)) 

    fire1_rect = pygame.Rect(500, 50, 50, 30)
    fire2_rect = pygame.Rect(730, 50, 50, 30)
    fire3_rect = pygame.Rect(400, 320, 50, 30)
    fire4_rect = pygame.Rect(650, 320, 50, 30)
    fire5_4_rect = pygame.Rect(800, 570, 200, 20)

    fire_image = pygame.image.load("stage1_fire.png")
    fire_image = pygame.transform.scale(fire_image, (50, 30))
    four_fire_image = pygame.image.load("stage1_fire4.png")
    four_fire_image = pygame.transform.scale(four_fire_image, (200, 30))

    bg_image = pygame.image.load("game_BG.png")
    bg_image = pygame.transform.scale(bg_image, (1000, 600))

    clock = pygame.time.Clock()

    pygame.mixer.init()
    pygame.mixer.music.load("main_tema_bgm.mp3")
    pygame.mixer.music.play(-1)

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

        for ground in [ground1_rect, ground2_rect, ground3_rect, ground4_rect, ground5_rect, ground6_rect, ground7_rect]:
            if student_rect.colliderect(ground) and velocity_y >= 0:
                student_y = ground.top - student_height
                velocity_y = 0
                student_jump = False
                on_ground = True

        if not on_ground and not student_jump:
            student_jump = True
            velocity_y = 0

        for fire_rect in [fire1_rect,fire2_rect,fire3_rect,fire4_rect,fire5_4_rect]:
            if student_rect.colliderect(fire_rect):
                print("불조심 하세요! 별 1개 차감됩니다!")   
                if collected_stars > 0 :
                    collected_stars -= 1
                    student_x = beginning_x
                    student_y = beginning_y
                    velocity_y = 0
                    student_jump = False
                    rect_attack_sound.play()

        for star in stars[:]:
            if student_rect.colliderect(star):
                stars.remove(star)
                collected_stars += 1
                collect_star_sound.play()
                print(f"별을 획득했습니다! 현재 별 개수: {collected_stars}")

        if student_rect.colliderect(door_rect):
            print("게임 클리어! 첫 번째 스테이지 완료.")
            return collected_stars

        screen.blit(bg_image, (0, 0))
        screen.blit(current_student_image, (student_x, student_y))
        for star in stars:
            if star.x >= 0:
                screen.blit(star_image, star.topleft)
        screen.blit(ground1_image, ground1_rect.topleft)
        screen.blit(ground2and3_image, ground2_rect.topleft)
        screen.blit(ground2and3_image, ground3_rect.topleft)
        screen.blit(ground4_image, ground4_rect.topleft)
        screen.blit(ground5and6_image, ground5_rect.topleft)
        screen.blit(ground5and6_image, ground6_rect.topleft)
        screen.blit(ground7_image, ground7_rect.topleft)
        screen.blit(door_image, door_rect.topleft)
        
        screen.blit(fire_image, fire1_rect.topleft)
        screen.blit(fire_image, fire2_rect.topleft)
        screen.blit(fire_image, fire3_rect.topleft)
        screen.blit(fire_image, fire4_rect.topleft)
        screen.blit(four_fire_image, fire5_4_rect.topleft)

        star_text = star_score_font.render(f"    : {collected_stars}", True, CL_BLACK)
        screen.blit(star_text, (50, 20))

        pygame.display.flip()
        clock.tick(60)
