import pygame
import sys
from stage1_sw_fg import run_stage_1
from stage2_fg_sh import run_stage_2
from stage3_sh_li import run_stage_3
from stage4_Li_ee  import run_stage_4
from stageFinal_BOSS import run_stage_5
from show_final_result import show_final_result
from main_lobby import main_lobby

def run_game_stages(screen):    
    collected_stars = 0
    total_collected_stars = 0

    collected_stars += run_stage_1(screen)
    print(f"스테이지 1 후 별 개수: {collected_stars}")
    collected_stars += run_stage_2(screen)
    print(f"스테이지 2 후 별 개수: {collected_stars}")
    collected_stars += run_stage_3(screen)
    print(f"스테이지 3 후 별 개수: {collected_stars}")
    collected_stars += run_stage_4(screen)
    print(f"스테이지 4 후 별 개수: {collected_stars}")

    total_collected_stars = run_stage_5(screen, collected_stars)
    print(f"최종 점수: {total_collected_stars}")

    show_final_result(screen, total_collected_stars)

    main_lobby(screen, run_game_stages)

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    pygame.display.set_caption("Go to school!")
    main_lobby(screen, run_game_stages)

if __name__ == "__main__":
    main()
