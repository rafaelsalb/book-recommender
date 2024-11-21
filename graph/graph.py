import numpy as np


class Graph:
    edges: list
    vertices: dict

    def __init__(self, edges: list, vertices: list = None, directed: bool = False):
        self.edges = edges or []
        if not directed:
            opposite = list(map(lambda row: (row[1], row[0]), edges))
            edges.extend(opposite)

        self.vertices = {}
        self.ids = {}
        for vertex in vertices:
            if vertex not in self.vertices:
                n = len(self.vertices)
                # value = vertex # use flyweight?
                self.vertices[n] = vertex
                self.ids[vertex] = n

    @staticmethod
    def from_edge_list(edges: list, directed: bool = False):
        vertices = set()
        for edge in edges:
            vertices.add(edge[0])
            vertices.add(edge[1])
        vertices = {v: i for v, i in enumerate(sorted(list(vertices)))}
        if not directed:
            opposite = list(map(lambda row: (row[1], row[0]), edges))
            edges.extend(opposite)
        return Graph(edges, vertices)

    def adjacency_matrix(self):
        m = len(self.vertices)
        matrix = np.zeros((m, m), dtype='float64')

        for edge in self.edges:
            i, j = self.ids[edge[0]], self.ids[edge[1]]
            matrix[i][j] = 1
        return matrix

    def add_edges(self, edges: list):
        self.edges.extend(edges)

class TripartedGraph(Graph):
    def __init__(self, edges: list, A: list, B: list, C: list, directed=False):
        role = lambda x, starting_idx: {"vertices": {i + starting_idx: vertex for i, vertex in enumerate(x)}, "ids": {vertex: i + starting_idx for i, vertex in enumerate(x)}}
        self.A = role(A, 0)
        self.B = role(B, len(A))
        self.C = role(C, len(A) + len(B))
        super().__init__(edges, A + B + C, directed=directed)
