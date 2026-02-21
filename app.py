from flask import Flask, render_template, request
import pickle
import pandas as pd
import os
import gdown

app = Flask(__name__)


# ================================
# DOWNLOAD MODEL FILES FROM DRIVE
# ================================

def download_file(file_id, output):
    if not os.path.exists(output):
        print(f"Downloading {output}...")
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        gdown.download(url, output, quiet=False, fuzzy=True)


# Your Google Drive file IDs
MOVIES_FILE_ID = "1KhkqkBlyQ92v_sPmlvLpMhW1LFUPAKxl"
SIMILARITY_FILE_ID = "1pmLzHguIK7GcuFIT0b1jM_NXdf_LiYwN"


# Download if not present
download_file(MOVIES_FILE_ID, "movies.pkl")
download_file(SIMILARITY_FILE_ID, "similarity.pkl")


# ================================
# LOAD MODEL FILES
# ================================

movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))


# ================================
# RECOMMENDATION FUNCTION
# ================================

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies


# ================================
# ROUTES
# ================================

@app.route("/", methods=["GET", "POST"])
def index():
    selected_movie = None
    recommendations = []

    if request.method == "POST":
        selected_movie = request.form.get("movie")
        recommendations = recommend(selected_movie)

    movie_list = movies["title"].values

    return render_template(
        "index.html",
        movies=movie_list,
        recommendations=recommendations,
        selected_movie=selected_movie
    )


# ================================
# RUN APP (LOCAL ONLY)
# ================================

if __name__ == "__main__":
    app.run(debug=True)