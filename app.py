from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from hybrid_model import hybrid_recommend

# Load movies dataset
movies = pd.read_csv("data/cleaned_movies.csv")

# Flask App
app = Flask(__name__)
CORS(app)  # Enable CORS

@app.route("/")
def home():
    return jsonify({"message": "🎬 Welcome to the Movie Recommendation API! Use /recommend to get movie suggestions."})

@app.route("/recommend", methods=["GET"])
def recommend():
    user_id = request.args.get("user_id", type=int)
    movie_title = request.args.get("movie_title", type=str)
    num_recommendations = request.args.get("num_recommendations", default=5, type=int)

    if not user_id or not movie_title:
        return jsonify({"error": "Missing user_id or movie_title parameter"}), 400

    recommendations = hybrid_recommend(user_id, movie_title, num_recommendations)

    return jsonify({
        "user_id": user_id,
        "movie_title": movie_title,
        "recommendations": recommendations
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)