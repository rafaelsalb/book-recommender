import numpy as np


class Graph:
    edges: list
    vertices: list

    def __init__(self, edges: list, vertices: list = None):
        self.edges = edges
        self.vertices = vertices

    @staticmethod
    def from_edge_list(edges: list, directed: bool = False):
        vertices = set()
        for edge in edges:
            vertices.add(edge[0])
            vertices.add(edge[1])
        vertices = sorted(list(vertices))
        if not directed:
            opposite = list(map(lambda row: (row[1], row[0]), edges))
            edges.extend(opposite)
        return Graph(edges, vertices)

    def adjacency_matrix(self):
        ids = {}
        for vertex in self.vertices:
            if vertex not in ids:
                ids[vertex] = len(ids)

        m = len(self.vertices)
        matrix = np.zeros((m, m), dtype='float64')

        for edge in self.edges:
            i, j = ids[edge[0]], ids[edge[1]]
            matrix[i][j] = 1
        return matrix, ids
