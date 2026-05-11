from flask import Flask, render_template, request
import pickle
import pandas as pd
import os
import sys
import gdown

app = Flask(__name__)

# ===============================
# DOWNLOAD MODEL FILES IF MISSING
# ===============================

def is_valid_pickle(path):
    """Check if a file exists and is a real pickle (not an HTML error page)."""
    if not os.path.exists(path):
        return False
    # Pickle files start with bytes 0x80 (protocol) — HTML pages start with '<'
    try:
        with open(path, 'rb') as f:
            header = f.read(2)
            return header[0] == 0x80  # valid pickle protocol marker
    except Exception:
        return False

def download_file(file_id, output):
    """Download a file from Google Drive with validation and retry."""
    if is_valid_pickle(output):
        print(f"✅ {output} already exists and is valid.")
        return True

    # Remove any broken/partial file first
    if os.path.exists(output):
        print(f"⚠️  Removing corrupted {output} and re-downloading...")
        os.remove(output)

    print(f"⬇️  Downloading {output} from Google Drive...")
    try:
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        gdown.download(url, output, quiet=False, fuzzy=True)
    except Exception as e:
        print(f"❌ gdown failed for {output}: {e}")

    # Validate what we downloaded
    if is_valid_pickle(output):
        print(f"✅ {output} downloaded and validated successfully.")
        return True
    else:
        # If file exists but is not valid pickle (HTML quota page), remove it
        if os.path.exists(output):
            os.remove(output)
        print(f"❌ ERROR: {output} download failed — Google Drive quota may be exceeded.")
        print(f"   Please re-share the file or upload it to a different host.")
        return False

MOVIES_FILE_ID     = "1KhkqkBlyQ92v_sPmlvLpMhW1LFUPAKxl"
SIMILARITY_FILE_ID = "1pmLzHguIK7GcuFIT0b1jM_NXdf_LiYwN"

movies_ok     = download_file(MOVIES_FILE_ID,     "movies.pkl")
similarity_ok = download_file(SIMILARITY_FILE_ID, "similarity.pkl")

if not movies_ok or not similarity_ok:
    print("\n💥 FATAL: Could not load model files. Exiting.")
    print("   Fix: Re-share your Google Drive files or raise their quota limit.")
    sys.exit(1)

# ===============================
# LOAD DATA
# ===============================

try:
    movies     = pickle.load(open("movies.pkl", "rb"))
    similarity = pickle.load(open("similarity.pkl", "rb"))
    print("✅ Model files loaded successfully.")
    print("   Columns in dataset:", movies.columns.tolist())
except Exception as e:
    print(f"💥 FATAL: Failed to unpickle model files: {e}")
    sys.exit(1)

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
    print("💥 FATAL: No movie title column found in dataset!")
    sys.exit(1)

print(f"✅ Using title column: '{TITLE_COL}'")

# ===============================
# RECOMMEND FUNCTION
# ===============================

def recommend(movie):
    try:
        movie_index = movies[movies[TITLE_COL] == movie].index[0]
        distances   = similarity[movie_index]
        movie_list  = sorted(
            list(enumerate(distances)),
            reverse=True,
            key=lambda x: x[1]
        )[1:6]
        return [movies.iloc[i[0]][TITLE_COL] for i in movie_list]
    except Exception as e:
        print(f"⚠️  Recommendation error for '{movie}': {e}")
        return []

# ===============================
# ROUTES
# ===============================

@app.route("/", methods=["GET", "POST"])
def index():
    selected_movie  = None
    recommendations = []

    if request.method == "POST":
        selected_movie  = request.form.get("movie")
        if selected_movie:
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