from flask import Flask, render_template, request
import pickle
import os
import gdown

app = Flask(__name__)

# ==============================
# DOWNLOAD MODEL FILES IF MISSING
# ==============================

def download_file(file_id, output):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output, quiet=False)

# movies.pkl
if not os.path.exists("movies.pkl"):
    print("Downloading movies.pkl...")
    download_file("1KhkqkBlyQ92v_sPmlvLpMhW1LFUPAKxl", "movies.pkl")

# similarity.pkl
if not os.path.exists("similarity.pkl"):
    print("Downloading similarity.pkl...")
    download_file("1pmLzHguIK7GcuFIT0b1jM_NXdf_LiYwN", "similarity.pkl")

# ==============================
# LOAD DATA
# ==============================

movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

movie_list = movies["title"].values


# ==============================
# RECOMMEND FUNCTION
# ==============================

def recommend(movie):
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended = []

    for i in distances[1:6]:
        recommended.append(movies.iloc[i[0]].title)

    return recommended


# ==============================
# ROUTES
# ==============================

@app.route("/", methods=["GET", "POST"])
def home():
    selected_movie = None
    recommendations = []

    if request.method == "POST":
        selected_movie = request.form.get("movie")
        recommendations = recommend(selected_movie)

    return render_template(
        "index.html",
        movies=movie_list,
        recommendations=recommendations,
        selected_movie=selected_movie
    )


# ==============================
# RUN
# ==============================

if __name__ == "__main__":
    app.run(debug=True)