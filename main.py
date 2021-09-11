import pygame
from environment import Environment
from constants import FPS, OBSTACLE_PERCENTAGE, WIN


def main():
    run = True
    clock = pygame.time.Clock()
    environment = Environment(WIN, OBSTACLE_PERCENTAGE)
    agent = environment.get_agent()
    start_mission = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    environment.reset()
                    agent = environment.get_agent()
                    start_mission = False
                if event.key == pygame.K_SPACE:
                    start_mission = True

                # elif environment.get_game_state() == 0:
                #     agent.inference_engine(environment)
        if start_mission and environment.get_game_state() == 0:
            agent.inference_engine(environment)

        environment.update()
        clock.tick(FPS)

    pygame.quit()




if __name__ == '__main__':
    main()




