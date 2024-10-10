# Refer: https://docs.streamlit.io/develop/api-reference
import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch poster for a particular movie
def fetch_poster(movie_id):
    
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=315afe2aab27834565fda3fa1d8a50a8&language=en-US')

    # converting the response into json
    data = response.json()

    # This is for checking the API is working fine or not.
    # st.text(data)
    # st.text('https://api.themoviedb.org/3/movie/{movie_id}?api_key=315afe2aab27834565fda3fa1d8a50a8&language=en-US')

    # get this info by seeing the results of API
    # for complete path, search in browser 'tmdb image path' and copy it
    return "http://image.tmdb.org/t/p/w500" + data['poster_path']    

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1]) [1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)

        # For fetching a poster for a particular movie_id from the API of TMDB website
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters


# Set the title for Front Web Page
st.title('Movie Recommender System')

# make the movies list
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# make the similarity matrix
similarity = pickle.load(open('similarity.pkl', 'rb'))


# now I want to make a select box and need to show the movies_list in it
selected_movie_name = st.selectbox(
    "Which Movie would you like to watch?",
    movies['title'].values
)

# apply a button
if st.button("Show Recommendation"):
    names,posters = recommend(selected_movie_name)

    # For displaying the Movie_poster:
    col1, col2, col3, col4, col5 = st.columns(5)
 
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
