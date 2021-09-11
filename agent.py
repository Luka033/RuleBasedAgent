import pygame
import numpy as np
from constants import (COLS, START_POS, GOAL_POS, ROWS, SQUARE_SIZE, ROTATION,
                       ROVER, AGENT_STACK_SIZE, AGENT_MOVE_DELAY)
from utils import agent_is_in_given_column, is_valid_coordinate, distance_between_points, find_first_num_from_sublist


class Agent:
    ROTATION_MOVE_COORDINATES = {
        0: -ROWS,
        45: -(ROWS - 1),
        90: 1,
        135: (ROWS + 1),
        180: ROWS,
        225: (ROWS - 1),
        270: -1,
        315: -(ROWS + 1)
    }

    def __init__(self):
        self.rotation_angle = 180
        self.current_pos = START_POS
        self.database = self.__init_database()
        self.moves_stack = []
        self.steps = 0

    def __init_database(self):
        """
        Initialized the agents database to an array of 2s (unknown coordinate)
        :return: an array representing the agents database (known surrounding)
        """
        database = np.full((ROWS * COLS), 2, dtype=int)
        database[START_POS] = 1
        database[GOAL_POS] = 3
        return database

    def inference_engine(self, environment):
        """
        Main driver of decision making. Uses helper functions to make decision and finally move
        :param environment: the current environment class instance to interact in
        """
        self.sonar(environment.get_grid())
        environment.update()
        pygame.time.wait(AGENT_MOVE_DELAY // 2)
        possible_moves = self.calculate_valid_moves()
        if (set(possible_moves).issubset(set(self.moves_stack))):
            next_move = find_first_num_from_sublist(self.moves_stack, possible_moves)
            next_destination = next_move - self.current_pos if next_move is not None else self.current_pos
        else:
            next_destination = self.get_next_move(possible_moves)
        self.make_move(next_destination)

        environment.update()
        pygame.time.wait(AGENT_MOVE_DELAY // 2)

    def sonar(self, current_grid):
        """
        Sends a sonar signal in three directions, 9, 12, and 3 a clock relative to the agents current
        rotation. Sonar will update unknown coordinates in the agent database until it hits an obstacle or wall.
        :param current_grid: an array representing the current grid
        """
        piece_position = self.current_pos
        move_coordinates = [  # get the coordinates of 9, 12, and 3 a clock relative to the agents current rotation
            self.ROTATION_MOVE_COORDINATES[self.__get_new_rotation(-ROTATION)],
            self.ROTATION_MOVE_COORDINATES[self.rotation_angle],
            self.ROTATION_MOVE_COORDINATES[self.__get_new_rotation(ROTATION)],
        ]
        for current_offset in move_coordinates:
            destination_coordinate = piece_position

            while (is_valid_coordinate(destination_coordinate)):
                if self.__is_first_column_exclusion(destination_coordinate, current_offset) or \
                        self.__is_last_column_exclusion(destination_coordinate, current_offset):
                    break

                destination_coordinate += current_offset
                if is_valid_coordinate(destination_coordinate):
                    if current_grid[destination_coordinate] == 1 or current_grid[destination_coordinate] == 3:
                        self.database[destination_coordinate] = 1
                    elif current_grid[destination_coordinate] == 0:
                        self.database[destination_coordinate] = 0
                        break

    def calculate_valid_moves(self):
        """
        Calculates all the possible moves the agent can take from the given position
        :return: an array containing the indices of valid coordinates
        """
        possible_moves = []
        piece_position = self.current_pos

        for current_offset in self.ROTATION_MOVE_COORDINATES.values():
            destination_coordinate = piece_position + current_offset
            if is_valid_coordinate(destination_coordinate):
                if self.__is_first_column_exclusion(piece_position, current_offset) or \
                        self.__is_last_column_exclusion(piece_position, current_offset) or \
                        self.database[destination_coordinate] != 1:
                    continue
                possible_moves.append(destination_coordinate)
        return possible_moves

    def get_next_move(self, possible_moves):
        """
        Returns the next move based on certain criteria
        :param possible_moves: an array of possible moves
        :return: an integer representing the next move to take
        """
        next_destination_coordinate = self.current_pos
        shortest_distance = float('inf')
        for move in possible_moves:
            distance = distance_between_points(move, GOAL_POS)
            if distance < shortest_distance and move not in self.moves_stack:
                shortest_distance = distance
                next_destination_coordinate = move - self.current_pos

        return next_destination_coordinate

    def make_move(self, move):
        """
        Moves the agent and updates the move stack and agent database
        :param move: an integer representing the move to make
        """
        move_made = False
        if move == -ROWS:  # NORTH
            if 0 < self.rotation_angle <= 180:
                self.rotation_angle = self.__get_new_rotation(-ROTATION)
            elif self.rotation_angle > 180:
                self.rotation_angle = self.__get_new_rotation(ROTATION)
            else:
                move_made = True

        elif move == -(ROWS - 1):  # NORTH-EAST
            if 45 < self.rotation_angle <= 225:
                self.rotation_angle = self.__get_new_rotation(-ROTATION)
            elif 45 > self.rotation_angle or self.rotation_angle > 225:
                self.rotation_angle = self.__get_new_rotation(ROTATION)
            else:
                move_made = True

        elif move == 1:  # EAST
            if 90 < self.rotation_angle <= 270:
                self.rotation_angle = self.__get_new_rotation(-ROTATION)
            elif self.rotation_angle < 90 or self.rotation_angle > 270:
                self.rotation_angle = self.__get_new_rotation(ROTATION)
            else:
                move_made = True

        elif move == (ROWS + 1):  # SOUTH-EAST
            if 135 < self.rotation_angle < 315:
                self.rotation_angle = self.__get_new_rotation(-ROTATION)
            elif self.rotation_angle < 135 or self.rotation_angle >= 315:
                self.rotation_angle = self.__get_new_rotation(ROTATION)
            else:
                move_made = True

        elif move == ROWS:  # SOUTH
            if self.rotation_angle > 180:
                self.rotation_angle = self.__get_new_rotation(-ROTATION)
            elif 0 <= self.rotation_angle < 180:
                self.rotation_angle = self.__get_new_rotation(ROTATION)
            else:
                move_made = True

        elif move == (ROWS - 1):  # SOUTH-WEST
            if self.rotation_angle < 45 or self.rotation_angle > 225:
                self.rotation_angle = self.__get_new_rotation(-ROTATION)
            elif 45 <= self.rotation_angle < 225:
                self.rotation_angle = self.__get_new_rotation(ROTATION)
            else:
                move_made = True

        elif move == -1:  # WEST
            if 270 > self.rotation_angle >= 90:
                self.rotation_angle = self.__get_new_rotation(ROTATION)
            elif self.rotation_angle > 270 or self.rotation_angle < 90:
                self.rotation_angle = self.__get_new_rotation(-ROTATION)
            else:
                move_made = True

        elif move == -(ROWS + 1):  # NORTH-WEST
            if 135 < self.rotation_angle < 315:
                self.rotation_angle = self.__get_new_rotation(ROTATION)
            elif self.rotation_angle <= 135 or self.rotation_angle > 315:
                self.rotation_angle = self.__get_new_rotation(-ROTATION)
            else:
                move_made = True
        else:  # No valid moves, just rotate
            self.rotation_angle = self.__get_new_rotation(-ROTATION)

        if move_made:
            self.current_pos += self.ROTATION_MOVE_COORDINATES[self.rotation_angle]
            self.database[self.current_pos] = 1

        self.steps += 1
        self.__update_move_stack(self.current_pos)

    def get_steps(self):
        return self.steps

    def draw(self, win):
        row = self.current_pos // ROWS
        col = self.current_pos % ROWS
        rotated_image = pygame.transform.rotate(ROVER, 360 - self.rotation_angle)
        new_rect = rotated_image.get_rect(center=ROVER.get_rect(center=(col * SQUARE_SIZE + ROVER.get_width() // 2,
                                                                        row * SQUARE_SIZE + ROVER.get_height() // 2)).center)
        win.blit(rotated_image, new_rect)

    def __is_first_column_exclusion(self, current_position, candidate_offset):
        """
        :param current_position: integer representing the agents current position
        :param candidate_offset: offset from the current position to make sure its not an exclusion
        :return: boolean representing whether or not the current position is a first column exclusion
        """
        return agent_is_in_given_column(current_position, 0) and (
                candidate_offset == -1 or candidate_offset == -(ROWS + 1) or candidate_offset == (ROWS - 1))

    def __is_last_column_exclusion(self, current_position, candidate_offset):
        """
        :param current_position: integer representing the agents current position
        :param candidate_offset: offset from the current position to make sure its not an exclusion
        :return: boolean representing whether or not the current position is a last column exclusion
        """
        return agent_is_in_given_column(current_position, ROWS - 1) and (
                candidate_offset == -(ROWS - 1) or candidate_offset == 1 or candidate_offset == (ROWS + 1))

    def __update_move_stack(self, most_recent_move):
        if most_recent_move not in self.moves_stack:
            self.moves_stack.append(most_recent_move)
        if len(self.moves_stack) > AGENT_STACK_SIZE:
            self.moves_stack.pop(0)

    def __get_new_rotation(self, rotation):
        current_rotation = self.rotation_angle
        # current_rotation += rotation
        # # TODO: Optimize
        # if current_rotation < 0:
        #     current_rotation = 360 - abs(rotation)
        # elif current_rotation == 360:
        #     current_rotation = 0
        # else:
        #     current_rotation = current_rotation % 360
        # return current_rotation
        current_rotation += rotation
        current_rotation %= 360
        return current_rotation

    def print_database(self):  # Mainly for debugging
        print("======= CURRENT DATABASE ============")
        for i in range(0, len(self.database), ROWS):
            print(self.database[i: i + ROWS])
