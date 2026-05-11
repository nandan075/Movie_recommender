# Movie Recommender

A Machine Learning Movie Recommendation System built with Flask and deployed as a web application.

## Overview

This project implements a movie recommendation engine that uses content-based filtering to suggest movies to users based on their preferences. The application analyzes movie metadata and leverages machine learning similarity algorithms to provide personalized recommendations.

## Features

- **Content-Based Filtering**: Uses cosine similarity on movie metadata (genres, keywords, cast, and overview) to find similar movies
- **Web Interface**: User-friendly HTML frontend for easy interaction
- **Flask Backend**: Lightweight and efficient Python backend
- **Deployed Application**: Ready-to-deploy web application
- **Fast Recommendations**: Sub-1 second response time for recommendations

## ML Model

**Algorithm**: Content-Based Filtering with Cosine Similarity

The recommendation system analyzes movie attributes including:
- Genres
- Keywords
- Cast information
- Movie overview/synopsis

By calculating cosine similarity between movie feature vectors, the model identifies and recommends the top-5 most similar movies to user selections.

## Dataset

**Dataset Used**: TMDb (The Movie Database) movies dataset containing 5000+ movies

The dataset includes comprehensive metadata for each movie including genres, cast, keywords, ratings, and descriptions, enabling accurate content-based recommendations.

## Architecture & Workflow

```
User Input (Movie Selection)
        ↓
Flask Backend Processing
        ↓
Preprocessed Movie Data & Feature Extraction
        ↓
Cosine Similarity Computation
        ↓
Top-5 Similar Movie Recommendations
        ↓
Web Interface Display
```

## Performance & Results

- **Dataset Size**: 5000+ movies
- **Recommendation Response Time**: <1 second
- **Output**: Top-5 similar movie recommendations per query
- **Accuracy**: Content-based matching with cosine similarity scoring

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML
- **ML & Data Processing**: 
  - Pandas
  - NumPy
  - scikit-learn
- **Deployment**: Render

## Live Application

🎬 **Visit the deployed application**: [Movie Recommender on Render](https://movie-recommender-1-i29d.onrender.com)

## Project Structure

```
Movie_recommender/
├── README.md
├── Procfile
├── requirements.txt
├── app.py
├── templates/
└── static/
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nandan075/Movie_recommender.git
cd Movie_recommender
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The application will start locally, typically at `http://localhost:5000`

## Usage

1. Open the web application in your browser
2. Search for or select a movie
3. Click to get recommendations
4. View the top-5 similar movies based on content similarity
5. Explore different movies and get tailored suggestions

## Deployment

The application is deployed on Render and can be accessed at: https://movie-recommender-1-i29d.onrender.com

To deploy your own instance:

1. Push your code to a GitHub repository
2. Connect your repository to Render
3. Configure the deployment settings and deploy

## Requirements

See `requirements.txt` for all dependencies. Key packages include:
- Flask
- Pandas
- NumPy
- scikit-learn

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available under the MIT License.

## Author

[Nandan075](https://github.com/nandan075)

---

For more information or questions, please open an issue on the repository.
