import sys
import os

import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dataset import authors, full_edge_list, genres, load_goodreads_books, names
from graph.graph import TripartedGraph
from recommender import Recommender

def small():
    small_dataset = pd.DataFrame(
        {
            "author": [["author1"], ["author1", "author2"], ["author2"]],
            "name": ["book1", "book2", "book3"],
            "genres": [["genre1"], ["genre1", "genre2"], ["genre2"]],
            "star_rating": [5, 4, 3]
        }
    )
    small_edge_list = full_edge_list(small_dataset)
    return small_dataset, small_edge_list

def sample():
    sample_dataset = pd.DataFrame(
        {
            # A
            "name": ["1984", "The Hobbit", "Harry Potter", "Harry Potter 2", "Harry Potter 3", "Harry Potter 4", "Harry Potter 5", "The Lord of the Rings"],
            # B
            "author": [["George Orwell"], ["J. R. R. Tolkien"], ["J. K. Rowling"], ["J. K. Rowling"], ["J. K. Rowling"], ["J. K. Rowling"], ["J. K. Rowling"], ["J. R. R. Tolkien"]],
            # C
            "genres": [["Dystopian"], ["Fantasy"], ["Fantasy"], ["Fantasy"], ["Fantasy"], ["Fantasy"], ["Fantasy"], ["Fantasy"]],
            "star_rating": [5, 4, 3, 4, 4, 4, 4, 5]
        }
    )
    sample_edge_list = full_edge_list(sample_dataset)
    return sample_dataset, sample_edge_list

def test_instantiate():
    dataset, edge_list = small()
    data = TripartedGraph(edge_list, names(dataset), authors(dataset), genres(dataset))
    recommender = Recommender(data)
    assert recommender is not None
    assert recommender.data is not None
    assert recommender.likes is not None
    assert recommender.splits is not None
    assert recommender.book_weight == 0.5
    assert recommender.author_weight == 0.3
    assert recommender.genre_weight == 0.2
    assert recommender.likes.shape == (7,)

def test_recommend():
    dataset, edge_list = small()
    data = TripartedGraph(edge_list, names(dataset), authors(dataset), genres(dataset))
    recommender = Recommender(data)
    top_n = recommender.recommend(3)
    titles = [data.A['vertices'][i] for i in top_n]

    print(titles)
    print(top_n)

    assert top_n is not None
    assert len(top_n) == 3

def test_like_and_recommend():
    dataset, edge_list = small()
    data = TripartedGraph(edge_list, names(dataset), authors(dataset), genres(dataset))
    recommender = Recommender(data)
    recommender.like(0)
    top_n = recommender.recommend(3)
    titles = [data.A['vertices'][i] for i in top_n]

    print(titles)
    print(top_n)

    assert top_n is not None
    assert len(top_n) == 3
    assert top_n[0] == 0

def test_example():
    dataset, edge_list = sample()
    data = TripartedGraph(edge_list, names(dataset), authors(dataset), genres(dataset))
    recommender = Recommender(data)
    n = 7

    top_n = recommender.recommend(n)
    print(recommender.names(top_n))

    recommender.like(0)
    top_n = recommender.recommend(n)
    print(recommender.names(top_n))

    recommender.dislike(0)
    top_n = recommender.recommend(n)
    print(recommender.names(top_n))

    recommender.like(1)
    top_n = recommender.recommend(n)
    print(recommender.names(top_n))

    recommender.like(6)
    top_n = recommender.recommend(n)
    print(recommender.names(top_n))

    assert top_n is not None
    assert len(top_n) == n
    assert top_n[0] == 6

def test_graph_image():
    dataset, edge_list = sample()
    data = TripartedGraph(edge_list, names(dataset), authors(dataset), genres(dataset))
    recommender = Recommender(data)
    image = recommender.graph_image()
    assert image is not None
    assert len(image) > 0

def test_info_from():
    dataset, edge_list = sample()
    data = TripartedGraph(edge_list, names(dataset), authors(dataset), genres(dataset))
    recommender = Recommender(data)
    info = recommender.info_from(0)

    print(info)

    assert info is not None
