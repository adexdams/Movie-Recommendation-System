import pandas as pd

# Load cleaned datasets
movies = pd.read_csv("data/cleaned_movies.csv")
ratings = pd.read_csv("data/cleaned_ratings.csv")

# Remove duplicate movie IDs
movies = movies.drop_duplicates(subset="id", keep="first")

# Compute average rating per movie
average_rating = ratings.groupby("movieId")["rating"].mean()

# Compute number of ratings per movie
vote_count = ratings.groupby("movieId")["rating"].count()

# Define a threshold for popularity (top 25% most-rated movies)
m = vote_count.quantile(0.75)

# Compute mean rating across all movies
C = average_rating.mean()

# Filter movies that have votes greater than 'm'
popular_movies = vote_count[vote_count >= m].index

# Ensure movies dataset only includes popular movies
movies_popular = movies[movies["id"].isin(popular_movies)].copy()

# Compute IMDB Weighted Rating (Handling Missing Data)
movies_popular["popularity_score"] = (
    (vote_count[movies_popular["id"]].fillna(0) / (vote_count[movies_popular["id"]].fillna(0) + m) *
     average_rating[movies_popular["id"]].fillna(C)) +
    (m / (vote_count[movies_popular["id"]].fillna(0) + m) * C)
)

# Sort by popularity score
movies_popular = movies_popular.sort_values(by="popularity_score", ascending=False)

def recommend_popular_movies(n=10):
    """
    Recommend movies using popularity-based filtering.
    """
    return movies_popular[["title", "popularity_score"]].head(n).to_dict(orient="records")