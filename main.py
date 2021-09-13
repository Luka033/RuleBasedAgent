import pygame
from environment import Environment
from constants import FPS, OBSTACLE_PERCENTAGE, WIN


def main():
    run = True
    clock = pygame.time.Clock()
    environment = Environment(WIN, OBSTACLE_PERCENTAGE)
    agent = environment.get_agent()
    mission_started = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
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
    main()

