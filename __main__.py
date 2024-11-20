import dataset
from pprint import pprint


def main():
    dataset.load_goodreads_books()
    books = dataset.names()
    genres = dataset.genres()
    authors = dataset.authors()
    print(dataset.dataset[:10])
    print(len([genre for genre in genres if genre is None]))
    # print(dataset.books_by_author(authors[0]))


if __name__ == "__main__":
    main()
