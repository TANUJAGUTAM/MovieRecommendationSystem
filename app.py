import streamlit as st
import pickle
import pandas as pd
import requests
def fetch_poster(movie_id):
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
            movie_id)
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance_scores = similarity[index]  # get similarity scores for the selected movie
    distances = sorted(list(enumerate(distance_scores)), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

    return recommended_movie_names, recommended_movie_posters
st.title('Movie Recommendation System')
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
# ✅ Auto-download similarity.pkl from Google Drive if not found
import os
import pickle
import requests

# ✅ Check and download if similarity.pkl is missing
def download_similarity():
    url = "https://drive.google.com/uc?export=download&id=1P1LgNw01wntsvCbW20gh1GG0V1czL5In"
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open("similarity.pkl", "wb") as f:
            f.write(response.content)
        return True
    except Exception as e:
        print("Error downloading similarity.pkl:", e)
        return False

# 📦 Ensure the file exists before loading
if not os.path.exists("similarity.pkl"):
    success = download_similarity()
    if not success:
        st.error("Failed to download similarity.pkl. Please try again later.")

# ✅ Load the file after confirming it's present
if os.path.exists("similarity.pkl"):
    similarity = pickle.load(open("similarity.pkl", "rb"))
else:
    similarity = None


movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

import streamlit as st

if st.button('Recommend movies'):
    if similarity is None:
        st.error("Similarity data not available.")
    else:
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

        # Create columns dynamically based on the number of recommended movies
        cols = st.columns(len(recommended_movie_names))

        for i, col in enumerate(cols):
            if i < len(recommended_movie_names):  # Ensure we don't access out-of-range elements
                with col:
                    st.text(recommended_movie_names[i])
                    st.image(recommended_movie_posters[i])

