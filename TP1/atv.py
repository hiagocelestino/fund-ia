from __future__ import annotations
from datetime import datetime
import random
from typing import List, Tuple
from board import Board
from gif import generate_gif
from search import a_star, bfs, dfs

import cProfile

def generate_config_random(size: int) -> List[int]:
    num_elementos = size ** 2
    config = random.sample(range(0, num_elementos), num_elementos)
    index_blank = config.index(0)
    config[index_blank] = None
    return config

def generate_start_board(config: List[int], size: int) -> Tuple[List[List], Tuple[int, int]]:
    board = []
    for i in range(size):
        line = []
        for j in range(size):
            value = config.pop(0)
            line.append(value)
        board.append(line)

    return board

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

size = 4
solution = generate_solution(size)

board = None
while board is None:
    config = generate_config_random(size)
    config = generate_start_board(config, size)
    board_try = Board(config)
    if board_try.has_solution():
        board = board_try

board_solution = Board(solution)
start = datetime.now()

# _lambda, _pi, found_solution = bfs(board, board_solution)
# _lambda, _pi, found_solution = dfs(board, board_solution)
_lambda, _pi, found_solution, num_visited = a_star(board, board_solution)
print(f"Time: {(datetime.now() - start)}s")
print(f"Nums walked: {num_visited}")

# node = found_solution
# print('-------------SOLUTION----------------')
# print(node)
print('-------------WALKED----------------')

walked = []
next = found_solution
while next:
    value = _pi[next.for_comparation]
    if value:
        walked.append(value.__str__())
    next = value
walked.insert(0, found_solution.__str__())
walked.insert(0, "XXXX")

# generate_gif(reversed(walked))
