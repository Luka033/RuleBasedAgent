import math
from constants import ROWS, COLS

def agent_is_in_given_column(piece_position, col):
    return (piece_position % ROWS) == col

def is_valid_coordinate(coordinate):
    return (0 <= coordinate < (ROWS * COLS))

def distance_between_points(point1, point2):
    x1 = point1 // ROWS
    y1 = point1 % ROWS
    x2 = point2 // ROWS
    y2 = point2 % ROWS
    return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) * 1.0)


def find_first_num_from_sublist(list, sub_list):
    """
    Takes in two lists, one is a sublist of the other list. Returns the number from the sublist
    that appears first in the list
    :param list: list of integers
    :param sub_list: sublist of the list
    :return: integer representing the number from the sublist that appeared first in the list or None
    """
    for num in list:
        for first_num_candidate in sub_list:
            if first_num_candidate == num:
                return first_num_candidate
    return None