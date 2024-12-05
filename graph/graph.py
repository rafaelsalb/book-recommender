import numpy as np


class Graph:
    edges: list[tuple]
    vertices: dict

    def __init__(self, edges: list, vertices: list = None, directed: bool = False):
        self.edges = edges or []
        if not directed:
            print("FIRST ROW", edges[0])
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

    def neighbors(self, vertex_id: int, both_ways=True) -> list:
        _neighbors = [self.ids[edge[1]] for edge in self.edges if self.ids[edge[0]] == vertex_id]
        return _neighbors

    def add_edges(self, edges: list):
        self.edges.extend(edges)

class TripartedGraph(Graph):
    def __init__(self, edges: list, A: list, B: list, C: list, directed=False):
        role = lambda x, starting_idx: {"vertices": {i + starting_idx: vertex for i, vertex in enumerate(x)}, "ids": {vertex: i + starting_idx for i, vertex in enumerate(x)}}
        self.A = role(A, 0)
        self.B = role(B, len(A))
        self.C = role(C, len(A) + len(B))
        self.splits = [0, len(A), len(A) + len(B)]
        super().__init__(edges, A + B + C, directed=directed)

    def group_of(self, vertex_id):
        if vertex_id < self.splits[1]:
            return self.A
        if vertex_id < self.splits[2]:
            return self.B
        return self.C

    def in_A(self, vertex_id):
        return vertex_id < self.splits[1]

    def in_B(self, vertex_id):
        return vertex_id < self.splits[2] and vertex_id >= self.splits[1]

    def in_C(self, vertex_id):
        return vertex_id >= self.splits[2]

    def neighbors_in_A(self, vertex_id: id):
        ids = []
        for edge in self.edges:
            from_id = self.ids[edge[0]]
            to_id = self.ids[edge[1]]
            if from_id == vertex_id and self.in_A(to_id):
                ids.append(self.ids[edge[1]])
        return ids

    def neighbors_in_B(self, vertex_id: id):
        ids = []
        for edge in self.edges:
            from_id = self.ids[edge[0]]
            to_id = self.ids[edge[1]]
            if from_id == vertex_id and self.in_B(to_id):
                ids.append(self.ids[edge[1]])
        return ids

    def neighbors_in_C(self, vertex_id: id):
        ids = []
        for edge in self.edges:
            from_id = self.ids[edge[0]]
            to_id = self.ids[edge[1]]
            if from_id == vertex_id and self.in_C(to_id):
                ids.append(self.ids[edge[1]])
        return ids

    def __getitem__(self, key):
        if key == "A":
            return self.A
        elif key == "B":
            return self.B
        elif key == "C":
            return self.C
        else:
            raise KeyError(f"Invalid key {key}")
