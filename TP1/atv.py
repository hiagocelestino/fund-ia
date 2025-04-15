from __future__ import annotations
from datetime import datetime
import random
from typing import List, Tuple
from board import Board
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


# config = [
#     [6, 14, 10, None],
#     [5, 12, 3, 13],
#     [9, 8, 11, 1],
#     [2, 7, 15, 4]
# ]
size = 3
solution = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, None]
]

board = None
while board is None:
    config = generate_config_random(size)
    config = generate_start_board(config, size)
    board_try = Board(config)
    if board_try.has_solution():
        board = board_try

board = [[5, 6, 7],
 [4, None, 8],
 [3, 2, 1]]

board = Board(board)

board_solution = Board(solution)
start = datetime.now()

# _lambda, _pi, found_solution = bfs(board, board_solution)
# _lambda, _pi, found_solution = dfs(board, board_solution)
_lambda, _pi, found_solution, num_visited = a_star(board, board_solution)
print(f"Time: {(datetime.now() - start)}s")
# print(f"Nums walked: {num_visited}")

node = found_solution

print('-------------SOLUTION----------------')
print(node)
print('-------------WALKED----------------')
# while node is not None:
#     print(node)
#     node = _pi[node]

