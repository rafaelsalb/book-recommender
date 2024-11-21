import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graph.graph import Graph, TripartedGraph

def test_graph():
    vertices = ['A', 'B', 'C', 'D', 'E']
    edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'A')]
    graph = Graph(edges, vertices)
    matrix = graph.adjacency_matrix()

    print(graph.vertices)
    print(graph.ids)
    print(graph.edges)
    print(matrix)

    assert graph.vertices == {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E'}
    assert graph.ids == {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    assert graph.edges == [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'A'), ('B', 'A'), ('C', 'B'), ('D', 'C'), ('E', 'D'), ('A', 'E')]

def test_triparted_graph():
    A = ['A1', 'A2', 'A3']
    B = ['B1', 'B2', 'B3']
    C = ['C1', 'C2', 'C3']
    edges = [
        ('A1', 'B1'),
        ('A1', 'B2'),
        ('A2', 'B2'),
        ('A2', 'B3'),
        ('A3', 'B3'),
        ('B1', 'C1'),
        ('B2', 'C2'),
        ('B2', 'C2'),
        ('B3', 'C3'),
    ]
    graph = TripartedGraph(edges, A, B, C, directed=False)
    matrix = graph.adjacency_matrix()

    print(graph.A)
    print(graph.B)
    print(graph.C)
    print(graph.vertices)
    print(graph.ids)
    print(graph.edges)
    print(matrix)

    assert graph.A == {'vertices': {0: 'A1', 1: 'A2', 2: 'A3'}, 'ids': {'A1': 0, 'A2': 1, 'A3': 2}}
    assert graph.B == {'vertices': {3: 'B1', 4: 'B2', 5: 'B3'}, 'ids': {'B1': 3, 'B2': 4, 'B3': 5}}
    assert graph.C == {'vertices': {6: 'C1', 7: 'C2', 8: 'C3'}, 'ids': {'C1': 6, 'C2': 7, 'C3': 8}}
    assert graph.vertices == {0: 'A1', 1: 'A2', 2: 'A3', 3: 'B1', 4: 'B2', 5: 'B3', 6: 'C1', 7: 'C2', 8: 'C3'}
    assert graph.ids == {'A1': 0, 'A2': 1, 'A3': 2, 'B1': 3, 'B2': 4, 'B3': 5, 'C1': 6, 'C2': 7, 'C3': 8}
    assert graph.adjacency_matrix().tolist() == [
        [0., 0., 0., 1., 1., 0., 0., 0., 0.], # A1
        [0., 0., 0., 0., 1., 1., 0., 0., 0.], # A2
        [0., 0., 0., 0., 0., 1., 0., 0., 0.], # A3
        [1., 0., 0., 0., 0., 0., 1., 0., 0.], # B1
        [1., 1., 0., 0., 0., 0., 0., 1., 0.], # B2
        [0., 1., 1., 0., 0., 0., 0., 0., 1.], # B3
        [0., 0., 0., 1., 0., 0., 0., 0., 0.], # C1
        [0., 0., 0., 0., 1., 0., 0., 0., 0.], # C2
        [0., 0., 0., 0., 0., 1., 0., 0., 0.], # C3
    ]
