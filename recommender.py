import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

import dataset
from graph.graph import TripartedGraph
from ppr import personalized_pagerank


class Recommender:
    def __init__(self, data: TripartedGraph):
        self.data: TripartedGraph = data

        self.book_weight: float = 0.5
        self.author_weight: float = 0.3
        self.genre_weight: float = 0.2

        n: int = len(data.vertices)

        self.splits = data.splits

        self.likes: np.ndarray = np.zeros(n)
        self.liked: list[int] = []

    @staticmethod
    def from_goodreads_dataset(percent: int = 1, subpercent: int = 100):
        sub = dataset.load_goodreads_books(percent=percent, subpercent=subpercent)
        print("Size of dataset:", len(sub))
        print("Generating edge list...")
        edge_list = []
        for edge in dataset.full_edge_list_generator(sub):
            edge_list.extend(edge)
            print(f"{len(edge_list)} edges...", end='\r')
        print(len(edge_list), "edges.")
        print("Generating graph...")
        data = TripartedGraph(edge_list, dataset.names(sub), dataset.authors(sub), dataset.genres(sub))
        print("Done.")
        return Recommender(data)

    @staticmethod
    def from_example_dataset():
        sub = dataset.load_example_dataset()
        edge_list = []
        for edge in dataset.full_edge_list_generator(sub):
            edge_list.extend(edge)
        data = TripartedGraph(edge_list, dataset.names(sub), dataset.authors(sub), dataset.genres(sub))
        return Recommender(data)

    def recommend(self, n: int) -> np.ndarray:
        adj_matrix: np.ndarray = self.data.adjacency_matrix()
        if np.all(self.likes == 0):
            e: np.ndarray = np.ones((len(self.data.vertices))) / len(self.data.vertices)
        else:
            e: np.ndarray = self.likes / np.sum(self.likes)
        ranking, _ = personalized_pagerank(adj_matrix, e)
        top_n: np.ndarray = np.argsort(ranking)[::-1]
        only_books = [i.item() for i in top_n if i < self.splits[1] and i not in self.liked][:n]
        return only_books

    def like(self, book_index: int):
        self.likes[book_index] = self.book_weight
        self.liked.append(book_index)

    def dislike(self, book_index: int):
        self.likes[book_index] = 0
        try:
            self.liked.remove(book_index)
        except ValueError:
            return

    # TODO: remove dupes from authors and genres for a given book
    def info_from(self, book_index: int):
        book = self.data.vertices[book_index]
        authors = list(set(self.data.neighbors_in_B(book_index))) #[author for author in self.data.neighbors(book_index)]# if self.data.in_B(author)]
        genres = list(set(self.data.neighbors_in_C(book_index)))
        return {
            "index": book_index,
            "book": book,
            "authors": self.names('B', authors),
            "genres": self.names('C', genres),
        }

    def names(self, group: str, indexes: np.ndarray) -> list:
        return [self.data[group]['vertices'][i] for i in indexes]

    def graph_image(self):
        G = nx.Graph()
        G.add_edges_from(self.data.edges)

        mapping = {node: i for i, node in enumerate(G.nodes())}
        G = nx.relabel_nodes(G, mapping)

        labels = {mapping[node]: node for node in mapping}

        node_colors = ['turquoise' for _ in range(len(G.nodes()))]

        plt.figure(figsize=(10, 10))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, labels=labels, node_color=node_colors, font_size=10, node_size=200, font_color='black')

        plt.savefig('static/graph.svg', format='svg')
        plt.close()

        return 'static/graph.svg'
