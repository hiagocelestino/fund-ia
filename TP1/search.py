from collections import defaultdict, deque
from heapq import heapify, heappop, heappush
from typing import Set

from board import Board


def bfs(board: Board, solution: Board):
    _lambda = defaultdict(lambda: float("inf"))
    _pi = defaultdict(lambda: None)

    found_solution = False
    if board == solution:
        return _lambda, _pi, board

    start = board
    queue = deque()
    queue.append(start)
    _pi[start.for_comparation]= None
    _lambda[start.for_comparation] = 0
    walked_tried = 0

    while (queue):
        current_vertex: Board = queue.popleft()
        neighbors: Set[Board] = set(current_vertex.generate_new_possibilities())
        for vertex in neighbors:
            coast = _lambda[vertex.for_comparation]
            if coast == float("inf"):
                walked_tried += 1
                _lambda[vertex.for_comparation] = _lambda[current_vertex.for_comparation] + 1
                _pi[vertex.for_comparation] = current_vertex
                if vertex == solution:
                    return _lambda, _pi, vertex
                queue.append(vertex)
    return _lambda, _pi, found_solution


def dfs(board: Board, solution: Board):
    _lambda = defaultdict(lambda: float("inf"))
    _pi = defaultdict(lambda: None)

    found_solution = False
    if board == solution:
        return _lambda, _pi, board

    start = board
    queue = []
    queue.append(start)
    _pi[start.for_comparation]= None
    _lambda[start.for_comparation] = 0
    walked_tried = 0

    while (len(queue) != 0):
        current_vertex: Board = queue.pop()
        neighbors: Set[Board] = set(current_vertex.generate_new_possibilities())
        for vertex in neighbors:
            coast = _lambda[vertex.for_comparation]
            if coast == float("inf"):
                _lambda[vertex.for_comparation] = _lambda[current_vertex.for_comparation] + 1
                _pi[vertex.for_comparation] = current_vertex
                if vertex == solution:
                    return _lambda, _pi, vertex
                queue.append(vertex)
                walked_tried += 1

    return _lambda, _pi, found_solution

# def heuristic_quantity_position_wrong(board: Board, solution: Board):
#     size = board.size
#     count_wrong = 0
#     for i in range(size):
#         for j in range(size):
#             if solution.configuration[i][j] != board.configuration[i][j]:
#                 count_wrong += 1
#     return count_wrong

def manhattan_distance(board: Board):
    distance = 0
    for i in range(board.size):
        for j in range(board.size):
            value = board.configuration[i][j]
            if value is not None:
                value = value - 1
                x_pos = value // board.size
                y_pos = value % board.size
                distance += abs(i - x_pos) + abs(j - y_pos)
    
    return distance

def a_star(board: Board, solution: Board):
    _lambda = defaultdict(lambda : float("inf"))
    _pi = defaultdict(lambda : None)

    found_solution = False
    if board == solution:
        return _lambda, _pi, board
    
    start = board
    _lambda[start.for_comparation] = 0
    _pi[start.for_comparation]= None

    priority_queue = [(manhattan_distance(board), board)]
    heapify(priority_queue)
    found_solution = None

    num_visited = 0
    while(priority_queue):
        _, current_vertex = heappop(priority_queue)
        num_visited += 1

        neighbors: Set[Board] = current_vertex.generate_new_possibilities()
        for neighbor in neighbors:
            coast = _lambda[neighbor.for_comparation]
            if coast != float("inf"):
                continue
            tentative_dist = manhattan_distance(neighbor)
            

            if tentative_dist < _lambda[neighbor.for_comparation]:
                _lambda[neighbor.for_comparation] = tentative_dist
                heappush(priority_queue, (tentative_dist, neighbor))
                _pi[neighbor.for_comparation] = current_vertex
                if neighbor == solution:
                    return _lambda, _pi, neighbor, num_visited


    return _lambda, _pi, found_solution, num_visited

