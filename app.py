from flask import Flask, render_template, request
import pickle
import pandas as pd
import os
import gdown

app = Flask(__name__)

# ===============================
# DOWNLOAD MODEL FILES IF MISSING
# ===============================

def download_file(file_id, output):
    if not os.path.exists(output):
        print(f"Downloading {output}...")
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        gdown.download(url, output, quiet=False, fuzzy=True)

MOVIES_FILE_ID = "1KhkqkBlyQ92v_sPmlvLpMhW1LFUPAKxl"
SIMILARITY_FILE_ID = "1pmLzHguIK7GcuFIT0b1jM_NXdf_LiYwN"

download_file(MOVIES_FILE_ID, "movies.pkl")
download_file(SIMILARITY_FILE_ID, "similarity.pkl")

# ===============================
# LOAD DATA
# ===============================

movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

print("Columns in dataset:", movies.columns)

# ===============================
# AUTO DETECT TITLE COLUMN
# ===============================

possible_columns = ["title", "movie_title", "name", "original_title"]

TITLE_COL = None
for col in possible_columns:
    if col in movies.columns:
        TITLE_COL = col
        break

if TITLE_COL is None:
    raise Exception("No movie title column found!")

print("Using column:", TITLE_COL)

# ===============================
# RECOMMEND FUNCTION
# ===============================

def recommend(movie):
    movie_index = movies[movies[TITLE_COL] == movie].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended = []
    for i in movie_list:
        recommended.append(movies.iloc[i[0]][TITLE_COL])

    return recommended

# ===============================
# ROUTES
# ===============================

@app.route("/", methods=["GET", "POST"])
def index():
    selected_movie = None
    recommendations = []

    if request.method == "POST":
        selected_movie = request.form.get("movie")
        recommendations = recommend(selected_movie)

    movie_list = movies[TITLE_COL].values

    return render_template(
        "index.html",
        movies=movie_list,
        recommendations=recommendations,
        selected_movie=selected_movie
    )

# ===============================
# RUN SERVER (RENDER COMPATIBLE)
# ===============================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)