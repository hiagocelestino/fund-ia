from __future__ import annotations
from collections import defaultdict
import copy
from typing import List


class Board:
    def __init__(self, config_board: List[List[int]]):
        self.size = len(config_board[0])
        self.configuration = config_board
        self.blank_position = self.find_blank_position()
        self.for_comparation = tuple(tuple(row) for row in self.configuration)

    def __hash__(self):
        return hash(tuple(tuple(linha) for linha in self.configuration))

    def __repr__(self):
        repr = ""
        for i in range(self.size):
            repr += "|"
            for j in range(self.size):
                element = self.configuration[i][j]
                if element is None:
                    repr += " X"
                    continue
                repr += f" {element}"
            repr += " |\n"
        return repr

    def __eq__(self, other: Board):
        if other.size != self.size:
            return False

        return self.for_comparation == other.for_comparation
    
    def __lt__(self, other: Board):
        return self.blank_position[0] < other.blank_position[0]
    
    def find_blank_position(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.configuration[i][j] is None:
                    return (i, j)

    def possibilities_movimentation(self):
        x = self.blank_position[0]
        y = self.blank_position[1]

        movimentations_permit = set()
        possibles_movimentation = (
            (-1, 0),
            (0, -1),
            (0, 1),
            (1, 0)
        )

        for mov in possibles_movimentation:
            new_x = x + mov[0]
            new_y = y + mov[1]

            if (new_x >= 0 and new_y >= 0) and (new_x < self.size and new_y < self.size):
                movimentations_permit.add((new_x, new_y))

        return movimentations_permit

    def generate_new_possibilities(self) -> List[Board]:
        board_possibilities = []
        possibilities = self.possibilities_movimentation()
        for (x, y) in possibilities:
            new_config = [[ column for column in line]  for line in self.configuration]
            aux = new_config[x][y]
            new_config[self.blank_position[0]][self.blank_position[1]] = aux
            new_config[x][y] = None
            board_possibilities.append(Board(new_config))
        return board_possibilities
    
    def has_solution(self):
        nums = [
            self.configuration[i][j]
            for i in range(self.size)
            for j in range(self.size)
            if self.configuration[i][j] != None
        ]

        num_inversions = 0
        for i in range(len(nums)):
            for k in range(i+1, len(nums)):
                if nums[i] > nums[k]:
                    num_inversions += 1
        
        blank_row = 0
        for i in range(self.size):
            if None in self.configuration[i]:
                blank_row = self.size - i
                break

        if self.size % 2 == 1:
            return num_inversions % 2 == 0
        else:
            return (blank_row % 2 == 1) == (num_inversions % 2 == 0)

