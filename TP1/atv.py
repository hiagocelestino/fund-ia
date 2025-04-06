from __future__ import annotations
from collections import defaultdict, deque
import math
import random
from typing import List, Set, Tuple
import copy

def has_solution(state):
    nums = [
        num
        for num in state
        if num != None
    ]

    num_inversions = 0
    nums_ordered = nums.copy()

    for i in range(len(nums)):
        for k in range(i+1, len(nums)):
            if nums[i] > nums[k]:
                nums_ordered[i] = nums[k]
                nums_ordered[k] = nums[i]
                num_inversions += 1
    
    return num_inversions % 2 == 0

def test_has_solution():
    test_state = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 14, None]
    assert has_solution(test_state) == False


test_has_solution()

def generate_config_random(size: int) -> List[int]:
    num_elementos = size ** 2
    config = random.sample(range(0, num_elementos), num_elementos)
    index_blank = config.index(0)
    config[index_blank] = None
    return config

def generate_start_board(config: List[int], size: int) -> Tuple[List[List], Tuple[int, int]]:
    board = []
    blank_position = None
    for i in range(size):
        line = []
        for j in range(size):
            value = config.pop(0)
            if value is None:
                blank_position = (i, j)
            line.append(value)
        board.append(line)

    return board, blank_position

def generate_solution(size: int):
    num = 0
    solution = []
    for i in range(size):
        line = []
        for j in range(size):
            num += 1
            line.append(num)
        solution.append(line)

    solution[-1][-1] = None
    return solution

config_random = generate_config_random(4)
print(config_random)
board, blank_position = generate_start_board(config_random, 4)
print(board)
print(blank_position)
solution = generate_solution(4)
print(solution)

class Board:
    def __init__(self, config_board: List[List[int]]):
        self.size = len(config_board[0])
        self.configuration = config_board
        self.blank_position = self.find_blank_position()

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

        for i in range(self.size):
            for j in range(self.size):
                if self.configuration[i][j] != other.configuration[i][j]:
                    return False
        return True
    
    def find_blank_position(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.configuration[i][j] is None:
                    return (i, j)

    def possibilities_movimentation(self):
        x = self.blank_position[0]
        y = self.blank_position[1]

        movimentations_permit = defaultdict(lambda: False)
        map_movimentation = {
            'up': (-1, 0),
            'left': (0, -1),
            'right': (0, 1),
            'down': (1, 0)
        }

        for mov in map_movimentation.keys():
            new_x = x + map_movimentation[mov][0]
            new_y = y + map_movimentation[mov][1]

            if (new_x >= 0 and new_y >= 0) and (new_x < self.size and new_y < self.size):
                movimentations_permit[mov] = (new_x, new_y)

        return movimentations_permit
    
    def generate_new_possibilities(self) -> List[Board]:
        board_possibilities = []
        possibilities = self.possibilities_movimentation()
        for _, (x, y) in possibilities.items():
            new_config = copy.deepcopy(self.configuration)
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

    
board = [[11, 10, 12, 6], [None, 3, 4, 1], [13, 2, 15, 7], [14, 8, 5, 9]]
board = Board(board)
print(board.configuration)
print(board.generate_new_possibilities())

def find_solution(board: Board, solution: Board):
    if not board.has_solution():
        raise Exception("Not exists solution for this problem")

    _lambda = defaultdict(lambda: math.inf)
    _pi = defaultdict(lambda: None)

    found_solution = False
    if board == solution:
        return _lambda, _pi, board

    start = board
    queue = deque()
    queue.append(start)
    _pi[start]= None
    walked_tried = 0
    MAX = 1000000

    visited = set()
    while (len(queue) != 0 and walked_tried <= MAX):
        current_vertex: Board = queue.popleft()
        neighbors: Set[Board] = set(current_vertex.generate_new_possibilities())
        visited.add(current_vertex)
        for vertex in neighbors.difference(visited):
            if vertex not in visited and vertex.has_solution():
                _lambda[vertex] = 1 if _lambda[current_vertex] == math.inf else _lambda[current_vertex] + 1
                _pi[vertex] = current_vertex
                if vertex == solution:
                    print("ACHOUUUUU")
                    return _lambda, _pi, vertex
                queue.append(vertex)
                walked_tried += 1
                visited.add(vertex)

    return _lambda, _pi, found_solution

config = [
    [6, 14, 10, None],
    [5, 12, 3, 13],
    [9, 8, 11, 1],
    [2, 7, 15, 4]
]

board = Board(config)
board_solution = Board(solution)
_lambda, _pi, found_solution = find_solution(board, board_solution)
print(f"Nums walked: {_lambda[found_solution]}")

node = found_solution
print('-------------WALKED----------------')
while node is not None:
    print(node)
    node = _pi[node]


