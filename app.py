import streamlit as st
import pickle
import pandas as pd
import requests
import time
time.sleep(0.2)
import os
import urllib.request
import gdown

URL = f"https://drive.google.com/file/d/1Kp7dErH6R8MESEJJf6Xnc0j6CX_PfvzJ/view?usp=sharing"

if not os.path.exists("similarity.pkl"):
    gdown.download(URL, "similarity.pkl", quiet=False)

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)



def fetch_poster(movie_id):
    try:
        response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=1bd9f2f151e6a1cf5f6a506fbec69181&language=en-US'.format(movie_id), timeout=5)
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
    except requests.exceptions.RequestException as e:
        print(f'Error fetching poster for movie ID{movie_id}:{e}')
        return "https://via.placeholder.com/500x750?text=No+Image"
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters=[]
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

movies_dict=pickle.load(open('movie_dict.pkl', 'rb'))
movies=pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name=st.selectbox(
    'Type or select a movie from the dropdown',movies['title'].values
)

if st.button('Show Recommendations'):
    names, posters=recommend(selected_movie_name)

    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
