import os
from pprint import pprint
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd

from dataset import full_edge_list, full_edge_list_generator


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

    edges = []
    for edge in full_edge_list_generator(sample_dataset):
        edges.append(list(edge))
    return sample_dataset, edges

def test_full_edge_list():
    dataset, edges = sample()

    # pprint(dataset)
    pprint(edges)

    assert len(dataset) == 8
