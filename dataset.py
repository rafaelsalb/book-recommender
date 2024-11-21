from itertools import product
from datasets import load_dataset

dataset = None

def load_goodreads_books(percent: int = 10):
    global dataset
    dataset = load_dataset("BrightData/Goodreads-Books", split=f'train[:{percent}%]').to_pandas()
    dataset = dataset.sort_values(by="num_ratings", ascending=False)

    dataset = dataset[["author", "name", "genres", "star_rating"]]
    dataset = dataset[dataset["genres"].apply(lambda x: x is not None)]
    dataset["genres"] = dataset["genres"].apply(lambda x: x.replace("[", "").replace("]", "").replace("\"", "").split(","))
    dataset = dataset[dataset["author"].apply(lambda x: x is not None)]
    dataset["author"] = dataset["author"].apply(lambda x: x.replace("[", "").replace("]", "").replace("\"", "").split(","))
    return dataset

def unique_in_multivalue(dataset, col):
    _col = dataset[col]
    entries = set()
    for row in _col:
        values = [x for x in row]
        for value in values:
            entries.add(value)
    entries = sorted(list(entries))
    return entries

def authors(dataset):
    return unique_in_multivalue(dataset, "author")

def names(dataset):
    return list(sorted(dataset["name"].tolist()))

def genres(dataset):
    return unique_in_multivalue(dataset, "genres")

def books_by_author(dataset, author):
    return dataset[dataset["author"].apply(lambda x: author in x)]

def books_by_genre(dataset, genre):
    return dataset[dataset["genres"].apply(lambda x: genre in x)]

def edge_list(dataset, col, value):
    subset = dataset[dataset[col].apply(lambda x: value in x)]["name"]
    edges = product([value], subset)
    return edges
