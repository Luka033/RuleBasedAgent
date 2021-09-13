import pygame
pygame.font.init()


WIN = pygame.display.set_mode()
OBSTACLE_PERCENTAGE = 30
ROWS, COLS = 48, 28
START_POS = 245
GOAL_POS = 1245
FPS = 30
WIDTH, HEIGHT = pygame.display.get_surface().get_size()
SQUARE_SIZE = WIDTH // max(ROWS, COLS)
ROTATION = 45
MAXIMUM_STEPS = 200
AGENT_STACK_SIZE = 20
AGENT_MOVE_DELAY = 500

LARGE_FONT = pygame.font.SysFont("comicsans", 100)
MEDIUM_FONT = pygame.font.SysFont("comicsans", 30)
SMALL_FONT = pygame.font.SysFont("comicsans", 15)


ROVER = pygame.transform.scale(pygame.image.load('assets/rover.png'), (SQUARE_SIZE, SQUARE_SIZE))

FINISH = pygame.transform.scale(pygame.image.load('assets/finish.png'), (SQUARE_SIZE, SQUARE_SIZE))
OBSTACLE = pygame.transform.scale(pygame.image.load('assets/mountain.png'), (SQUARE_SIZE, SQUARE_SIZE))
GREEN_BOX = pygame.transform.scale(pygame.image.load('assets/green_box.png'), (SQUARE_SIZE, SQUARE_SIZE))
RED_BOX = pygame.transform.scale(pygame.image.load('assets/red_box.png'), (SQUARE_SIZE, SQUARE_SIZE))

WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (34, 139, 34)

