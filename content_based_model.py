import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import ast

# Load cleaned movies dataset
movies = pd.read_csv("data/cleaned_movies.csv")

# Replace NaN overviews with empty strings
movies["overview"] = movies["overview"].fillna("")

# Convert genres column from list of dictionaries to a string of genres
movies['genres'] = movies['genres'].apply(lambda x: ' '.join([i['name'] for i in ast.literal_eval(x)]) if isinstance(x, str) else '')

# Convert keywords column from list of dictionaries to a string of keywords
movies['keywords'] = movies['keywords'].apply(lambda x: ' '.join([i['name'] for i in ast.literal_eval(x)]) if isinstance(x, str) else '')


# Replace NaN overviews with empty strings
movies['overview'] = movies['overview'].fillna('')

# Create a TF-IDF Vectorizer for overview
tfidf = TfidfVectorizer(stop_words='english', max_features=5000)

# Transform overview text into numerical vectors
tfidf_matrix = tfidf.fit_transform(movies['overview'])


# Compute the cosine similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Create a mapping of movie title to index
movie_indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()


def recommend_movies(title, cosine_sim=cosine_sim, num_recommendations=10):
    # Get the index of the movie
    idx = movie_indices.get(title, None)

    if idx is None:
        return "Movie not found."

    # Get similarity scores for all movies
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort movies based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get indices of top recommended movies
    movie_indices_recommended = [i[0] for i in sim_scores[1:num_recommendations + 1]]

    # Return recommended movie titles
    rec = movies['title'].iloc[movie_indices_recommended]

    return rec
