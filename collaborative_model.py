import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix, csr_matrix
from sklearn.decomposition import TruncatedSVD

# Load cleaned ratings dataset
ratings = pd.read_csv("data/cleaned_ratings.csv")

# ✅ 1️⃣ Reduce dataset size (Keep only 50,000 random ratings for demo)
ratings_sampled = ratings.sample(n=50000, random_state=42)

# ✅ 2️⃣ Keep only users who have rated at least 10 movies
user_counts = ratings_sampled["userId"].value_counts()
active_users = user_counts[user_counts >= 10].index
filtered_ratings = ratings_sampled[ratings_sampled["userId"].isin(active_users)]

# ✅ 3️⃣ Convert userId and movieId to category codes (reduces memory)
user_list = filtered_ratings["userId"].astype("category").cat.codes
movie_list = filtered_ratings["movieId"].astype("category").cat.codes
rating_values = filtered_ratings["rating"].values

# ✅ 4️⃣ Build a small sparse matrix
num_users = user_list.nunique()
num_movies = movie_list.nunique()
sparse_matrix = coo_matrix((rating_values, (user_list, movie_list)), shape=(num_users, num_movies)).tocsr()

# ✅ 5️⃣ Perform Lightweight Truncated SVD (Low Memory)
k = 10  # Reduce to just 10 latent factors
svd = TruncatedSVD(n_components=k, random_state=42)
U = svd.fit_transform(sparse_matrix)
sigma = np.diag(svd.singular_values_)
Vt = svd.components_

# ✅ 6️⃣ Compute Predicted Ratings (Compressed)
predicted_ratings = np.dot(np.dot(U, sigma), Vt)

# ✅ 7️⃣ Convert back to DataFrame (Small Size)
user_index_to_id = {index: user_id for user_id, index in
                    zip(filtered_ratings["userId"].astype("category").cat.categories, range(num_users))}
movie_index_to_id = {index: movie_id for movie_id, index in
                     zip(filtered_ratings["movieId"].astype("category").cat.categories, range(num_movies))}

predicted_ratings_df = pd.DataFrame(predicted_ratings, index=user_index_to_id.keys(), columns=movie_index_to_id.keys())


def recommend_movies_collaborative(user_id, num_recommendations=5):
    """
    Recommend movies using a lightweight collaborative filtering model.
    """
    if user_id not in predicted_ratings_df.index:
        return ["User not found."]

    # Get predicted ratings for the user
    user_ratings = predicted_ratings_df.loc[user_id].sort_values(ascending=False)

    # Get top recommended movie IDs
    recommended_movie_ids = user_ratings.index[:num_recommendations]

    return recommended_movie_ids.tolist()