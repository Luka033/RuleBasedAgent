import pygame
import sys
from environment import Environment
from constants import FPS, WINDOW


def main(environment_file=None):
    run = True
    clock = pygame.time.Clock()
    environment = Environment(WINDOW, environment_file)

    agent = environment.get_agent()
    mission_started = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_SPACE and mission_started and environment.get_game_state() == 0:
                #     agent.inference_engine(environment)
                if event.key == pygame.K_r:
                    environment.reset()
                    agent = environment.get_agent()
                    mission_started = False

                if event.key == pygame.K_SPACE:
                    mission_started = True

        if mission_started and environment.get_game_state() == 0:
            agent.inference_engine(environment)

        environment.update()
        clock.tick(FPS)

    pygame.quit()




if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main()



