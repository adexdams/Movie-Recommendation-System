import streamlit as st
import requests

# Streamlit Page Config
st.set_page_config(page_title="Movie Recommendation System", page_icon="🎬", layout="wide")

# Backend API URL (Update with deployed API URL when hosted)
API_BASE_URL = "http://127.0.0.1:5000"

# Streamlit UI - Header
st.markdown("<h1 style='text-align: center; color: gold;'>🎬 Movie Recommendation System</h1>", unsafe_allow_html=True)

# User ID Input
user_id = st.text_input("Enter your User ID", value="15")


# Function to validate if the User ID exists
def validate_user_id(user_id):
    try:
        user_id = int(user_id)  # Convert to integer
        response = requests.get(
            f"{API_BASE_URL}/recommend?user_id={user_id}&movie_title=The Matrix&num_recommendations=5")

        # If API returns an error, the user ID does not exist
        if response.status_code == 400 or "error" in response.json():
            return False
        return True
    except:
        return False


# Fetch 5 random movies on first load
if "random_movies" not in st.session_state:
    try:
        response = requests.get(f"{API_BASE_URL}/recommend?user_id=1&movie_title=The Matrix&num_recommendations=5")
        st.session_state.random_movies = response.json().get("recommendations", [])
    except:
        st.session_state.random_movies = []

# Display random movies only if User ID is valid
if validate_user_id(user_id):
    st.subheader("🔀 Pick a Movie to Get Recommendations:")
    selected_movie = st.radio("Select a movie:", st.session_state.random_movies, index=0, key="selected_movie")

    # Fetch recommendations when a movie is selected
    if selected_movie:
        try:
            response = requests.get(
                f"{API_BASE_URL}/recommend?user_id={user_id}&movie_title={selected_movie}&num_recommendations=5")
            recommendations = response.json().get("recommendations", [])
        except:
            recommendations = []

        # Display Recommendations
        st.subheader("🎥 We Think You'd Like:")
        for movie in recommendations:
            if st.button(movie):
                st.session_state.history.append(movie) if "history" in st.session_state else st.session_state.update(
                    {"history": [movie]})
                st.rerun()

    # Display Watch History
    if "history" in st.session_state and st.session_state.history:
        st.subheader("📜 Movies You’ve Watched:")
        st.write(", ".join(st.session_state.history))

else:
    # Display user-friendly error message
    st.error("⚠️ Invalid User ID! Please enter a valid User ID from the dataset.")