import pandas as pd
from content_based_model import recommend_movies
from collaborative_model import recommend_movies_collaborative
from popularity_model import recommend_popular_movies

# Load cleaned movies dataset
movies = pd.read_csv("data/cleaned_movies.csv")

# Create a dictionary to map movie IDs to titles
movie_id_to_title = pd.Series(movies["title"].values, index=movies["id"]).to_dict()

def hybrid_recommend(user_id, movie_title, num_recommendations=5, weight_cb=0.6, weight_cf=0.3, weight_pop=0.1):
    """
    Generate hybrid recommendations using content-based, collaborative, and popularity-based filtering.

    Parameters:
    - user_id (int): User ID for collaborative filtering.
    - movie_title (str): Movie title for content-based filtering.
    - num_recommendations (int): Number of recommendations to return.
    - weight_cb (float): Weight for content-based filtering.
    - weight_cf (float): Weight for collaborative filtering.
    - weight_pop (float): Weight for popularity-based filtering.

    Returns:
    - List of recommended movie titles.
    """
    recommendation_scores = {}

    # ✅ Content-Based Filtering (CBF)
    try:
        content_recs = recommend_movies(movie_title, num_recommendations)
        for idx, movie in enumerate(content_recs):
            recommendation_scores[movie] = recommendation_scores.get(movie, 0) + weight_cb * (num_recommendations - idx)
    except:
        content_recs = []

    # ✅ Collaborative Filtering (CF) - Convert Movie IDs to Titles
    try:
        collab_recs = recommend_movies_collaborative(user_id, num_recommendations)
        collab_recs = [movie_id_to_title.get(movie, movie) for movie in collab_recs]  # Convert IDs to titles
        for idx, movie in enumerate(collab_recs):
            recommendation_scores[movie] = recommendation_scores.get(movie, 0) + weight_cf * (num_recommendations - idx)
    except:
        collab_recs = []

    # ✅ Popularity-Based Filtering (Trending Movies)
    try:
        pop_recs = recommend_popular_movies(num_recommendations)["title"].tolist()
        for idx, movie in enumerate(pop_recs):
            recommendation_scores[movie] = recommendation_scores.get(movie, 0) + weight_pop * (num_recommendations - idx)
    except:
        pop_recs = []

    # Remove the input movie from recommendations (if present)
    recommendation_scores.pop(movie_title, None)

    # Sort recommendations by total score
    sorted_recommendations = sorted(recommendation_scores.items(), key=lambda x: x[1], reverse=True)

    # Return top recommended movie titles
    return [movie[0] for movie in sorted_recommendations[:num_recommendations]]

# ✅ Example: Get hybrid recommendations for a user and movie
if __name__ == "__main__":
    user_id = 15
    movie_title = "The Matrix"
    print(hybrid_recommend(user_id, movie_title, num_recommendations=5))