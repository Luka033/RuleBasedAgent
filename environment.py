import pygame
import numpy as np
from agent import Agent
from constants import (ROWS, COLS, GOAL_POS, START_POS, ORANGE, SQUARE_SIZE, FINISH, OBSTACLE, GREEN_BOX, RED_BOX,
                       WIDTH, HEIGHT, WHITE, BLACK, GREEN, RED, LARGE_FONT, MEDIUM_FONT, SMALL_FONT, MAXIMUM_STEPS)


class Environment:
    def __init__(self, window, obstacles_percentage):
        self.window = window
        self.obstacles_percentage = obstacles_percentage
        self.__init()

    def __init(self):
        self.grid = self.__create_grid(self.obstacles_percentage)
        self.agent = Agent()
        self.game_state = 0 # 0: on-going, 1: goal found, -1: game over

    def __display_text(self, font, text, x, y, color):
        text_label = font.render(f"{text}", 1, color)
        text_rect = text_label.get_rect(center=(x, y))
        self.window.blit(text_label, text_rect)

    def __draw_objects(self):
        for i in range((ROWS * COLS)):
            row = i // ROWS
            col = i % ROWS
            if self.agent.database[i] == 1:
                self.window.blit(GREEN_BOX, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            if self.agent.database[i] == 0:
                self.window.blit(RED_BOX, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            if self.grid[i] == 0:
                self.window.blit(OBSTACLE, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            if self.grid[i] == 3:
                self.window.blit(FINISH, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            # Numbered grid for debugging
            # self.__display_text(SMALL_FONT, i, col * SQUARE_SIZE + 10, row * SQUARE_SIZE + 10, BLACK)

        self.agent.draw(self.window)

    def __draw_grid(self):
        self.window.fill(BLACK)
        x, y = 0, 0
        while y < COLS:
            if x > 0 and x % ROWS == 0:
                y += 1
                x = 0
            if y < COLS:
                rect = pygame.Rect(x * SQUARE_SIZE + 1, y * SQUARE_SIZE + 1, SQUARE_SIZE - 2, SQUARE_SIZE - 2)
                pygame.draw.rect(self.window, ORANGE, rect)
            x += 1

    def __create_grid(self, obstacles_percentage):
        obstacles_percentage /= 100
        number_of_obstacles = int(obstacles_percentage * (ROWS * COLS))
        grid = np.ones((COLS * ROWS), dtype=int)
        np.put(grid, np.random.choice(range(COLS * ROWS), number_of_obstacles, replace=False), 0)
        # grid = [
        #     1, 1, 1, 1, 1, 1, 1, 1,
        #     0, 0, 1, 1, 1, 1, 1, 1,
        #     0, 1, 1, 1, 1, 1, 1, 1,
        #     1, 1, 1, 1, 1, 1, 1, 1,
        #     1, 1, 1, 1, 1, 1, 1, 1,
        #     1, 1, 1, 1, 1, 1, 1, 1,
        #     1, 1, 1, 1, 1, 1, 1, 1,
        #     1, 1, 1, 1, 1, 1, 1, 3,
        # ]
        grid[START_POS] = 1
        grid[GOAL_POS] = 3
        return grid

    def update(self):
        self.__draw_grid()
        self.__draw_objects()
        if self.game_state == 1:
            self.__display_text(LARGE_FONT, 'MISSION COMPLETE!', WIDTH / 2, HEIGHT / 2 - 20, GREEN)
        elif self.game_state == -1:
            self.__display_text(LARGE_FONT, 'MISSION FAILED!', WIDTH / 2, HEIGHT / 2 - 20, RED)
        self.__display_text(MEDIUM_FONT, f'STEPS: {self.get_agent().get_steps()}', WIDTH / 2, HEIGHT - SMALL_FONT.get_height(), WHITE)
        pygame.display.update()

    def reset(self):
        self.__init()

    def get_agent(self):
        return self.agent

    def get_grid(self):
        return self.grid

    def get_game_state(self):
        goal_found = self.agent.current_pos == GOAL_POS
        if goal_found:
            self.game_state = 1
        elif self.agent.get_steps() >= MAXIMUM_STEPS:
            self.game_state = -1
        else:
            self.game_state = 0
        return self.game_state
