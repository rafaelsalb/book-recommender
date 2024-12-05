import os
from datasets import load_dataset
from itertools import product
from joblib import Memory
import pandas as pd
import multiprocessing

memory = Memory(location='.cache', verbose=0)

@memory.cache
def load_goodreads_books(percent: int = 1, subpercent: int = 100):
    print("Loading Goodreads dataset...")
    dataset = load_dataset("BrightData/Goodreads-Books", split=f'train[:{percent}%]').to_pandas()
    print("Dataset loaded.")
    dataset = dataset.sort_values(by="num_ratings", ascending=False)

    dataset = dataset[["author", "name", "genres", "star_rating"]]
    print("Getting subset.")
    dataset = dataset.head(int(len(dataset) * subpercent / 100))
    print("Subset obtained.")

    print("Treating data.")
    dataset = dataset[dataset["genres"].apply(lambda x: x is not None)]
    dataset["genres"] = dataset["genres"].apply(lambda x: x.replace("[", "").replace("]", "").replace("\"", "").split(","))
    dataset = dataset[dataset["author"].apply(lambda x: x is not None)]
    dataset["author"] = dataset["author"].apply(lambda x: x.replace("[", "").replace("]", "").replace("\"", "").split(","))
    print("Data treated.")
    return dataset

def load_example_dataset():
    size: str = os.environ.get("EXAMPLE_DATASET_SIZE", "sm")
    dataset = pd.read_csv(f"example_dataset_{size}.csv", sep=";")
    print("Treating data.")
    dataset = dataset[dataset["genres"].apply(lambda x: x is not None)]
    dataset["genres"] = dataset["genres"].apply(lambda x: x.replace("[", "").replace("]", "").replace("\"", "").replace("\'", "").split(","))
    dataset = dataset[dataset["author"].apply(lambda x: x is not None)]
    dataset["author"] = dataset["author"].apply(lambda x: x.replace("[", "").replace("]", "").replace("\"", "").replace("\'", "").split(","))
    print("Data treated.")
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
    edges = tuple(edges)
    return edges

def full_edge_list(dataset):
    if len(dataset) > 1000:
        print("Large dataset. It would be better to use 'full_edge_list_generator' instead.")
    seen_entries = set()
    edges = []
    for col in ['author', 'genres']:
        for r in dataset[col]:
            for i in r:
                entry = edge_list(dataset, col, i)
                if entry not in seen_entries:
                    seen_entries.add(entry)
                    # edges.extend(entry)
                # yield entry
    # return edges
    return list(seen_entries)

def process_item(args):
    dataset, col, r = args
    entries = []
    for i in r:
        entry = edge_list(dataset, col, i)
        entries.append(entry)
    return entries

def full_edge_list_generator(dataset):
    seen_entries = set()
    pool = multiprocessing.Pool(processes=4)

    # Prepare the arguments for the helper function
    args = [(dataset, col, r) for col in ['author', 'genres'] for r in dataset[col]]

    # Use multiprocessing to process the items
    results = pool.map(process_item, args)

    # Flatten the results and add to seen_entries
    for result in results:
        for entry in result:
            if entry not in seen_entries:
                seen_entries.add(entry)
                yield entry

    pool.close()
    pool.join()
