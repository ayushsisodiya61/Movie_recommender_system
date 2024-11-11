import streamlit as st
import pickle
import requests


st.set_page_config(layout="wide")

def fetch_poster(movie_id):
    response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=40dc7ffc47d01d7f1ecd70486e31bd28&language=en-US'.format(movie_id))
    data=  response.json()
    return  "https://image.tmdb.org/t/p/w500/" + data['poster_path']



def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    similarity_matrix= pickle.load(open('similarity_matrix.pkl','rb'))
    distances = similarity_matrix[movie_index]
    similar_mov_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies= list()
    recommended_movie_posters= list()

    for i in similar_mov_list:
        movie_id= movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch posters from Api
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movie_posters

movies= pickle.load(open('movies.pkl', 'rb'))
movies_list= movies['title'].values
st.title('Movie Recommendation System')
selected_movie_name= st.selectbox('Enter the name of a Movie',movies_list)
if st.button('Recommend'):
    recommended_movie_names,posters= recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(posters[4])