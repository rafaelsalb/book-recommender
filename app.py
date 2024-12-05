import os
from dotenv import load_dotenv
from pprint import pprint
from flask import Flask, redirect, render_template, request

from recommender import Recommender

load_dotenv()

app = Flask(__name__)

if int(os.environ.get("USE_SAMPLE_DATASET")):
    recommender: Recommender = Recommender.from_example_dataset()
else:
    DATASET_PERCENT: int = int(os.environ.get("DATASET_PERCENT"))
    recommender: Recommender = Recommender.from_goodreads_dataset(1, DATASET_PERCENT)

@app.get('/')
def index():
    print("Likes:", recommender.likes)
    books = recommender.recommend(int(os.environ.get("RECOMMEND_N", 10)))
    infos = [recommender.info_from(b) for b in books]
    pprint(infos)
    liked = recommender.liked
    liked_infos = [recommender.info_from(b) for b in liked]
    graph_image = recommender.graph_image()
    return render_template('index.html',
        books=infos,
        user_books=liked_infos,
        graph_image=graph_image
    )

@app.post('/like/<int:index>')
def like(index):
    book_index = int(index)
    recommender.like(book_index)
    return redirect('/')

@app.post('/dislike/<int:index>')
def dislike(index):
    book_index = int(index)
    recommender.dislike(book_index)
    return redirect('/')

if __name__ == '__main__':
    app.run()
