import pickle
import pandas as pd
import requests
import streamlit as st

st.title("Movie Recommender App")

# Load the movies dictionary and similarity matrix
movie_dict = pickle.load(open('movie_list.pkl', 'rb'))
similarity_dict = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pd.DataFrame(similarity_dict)
# print('movies')
# print(movies)
# print('similarity')
# print(similarity)
api_key='925dd7f6e9ee484dfb69bdb3a7329df3'
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=925dd7f6e9ee484dfb69bdb3a7329df3&language=en-US'.format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

option = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title']  # Assuming the DataFrame has a 'title' column
)
st.write(f'You selected Movie: {option}')

# Function to search for the movie index
def search_movie_index(title):
    return movies[movies['title'] == title].index[0]

index = []
recommended_movies = []
# Function to get recommended movies
def recommended(title):
    index_m = search_movie_index(title)
    sorted_list = sorted(list(enumerate(similarity.iloc[index_m])), reverse=True, key=lambda x: x[1])
    # st.write(sorted_list)
    recommended_movies.clear()
    index.clear()
    for i in sorted_list[1:6]:
        index.append(movies['id'].iloc[i[0]])
        recommended_movies.append(movies['title'].iloc[i[0]])
    print(index)
    return recommended_movies

# Recommendation button
if st.button('Show Recommendation'):
    st.title('Recommended Movies')
    recommended(option)
    # Create five columns
    cols = st.columns(5)

    # Iterate over the columns and populate them with movie titles and posters
    for col, movie in zip(cols, recommended_movies):
        with col:
            st.text(movie)
    for col, idx in zip(cols, index):
        with col:
            st.image(fetch_poster(idx))