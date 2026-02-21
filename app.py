from flask import Flask, render_template, request
import pickle
import os

app = Flask(__name__)

# load trained data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    return [movies.iloc[i[0]].title for i in movie_list]


# HOME PAGE
@app.route('/')
def home():
    return render_template(
        'index.html',
        movie_list=movies['title'].values,
        selected_movie=None,
        recommendations=None
    )


# RECOMMENDATION ROUTE
@app.route('/recommend', methods=['POST'])
def recommend_movies():
    selected_movie = request.form.get('movie')

    if not selected_movie:
        return render_template(
            'index.html',
            movie_list=movies['title'].values,
            selected_movie=None,
            recommendations=None
        )

    recommendations = recommend(selected_movie)

    return render_template(
        'index.html',
        movie_list=movies['title'].values,
        selected_movie=selected_movie,
        recommendations=recommendations
    )


# RUN SERVER
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)