from typing import List


class Tree:
    def __init__(self, verticies: List[int]):
        self.vertices = verticies
        self.edges = {vertex: set() for vertex in verticies}
    
    def add_edges(self, vertex_source: int, vertex_destination: int):
        self.edges[vertex_source].add(vertex_destination)
