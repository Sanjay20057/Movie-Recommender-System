import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=6f3bbb8c4059102285b0a027b5a0092c&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity.iloc[movie_index].values
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movie_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movie_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movie_poster

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity_files = [
    'similarity_comp1.csv.gz',
    'similarity_comp2.csv.gz',
    'similarity_comp3.csv.gz',
    'similarity_comp4.csv.gz',
    'similarity_comp5.csv.gz',
    'similarity_comp6.csv.gz',
    'similarity_comp7.csv.gz',
    'similarity_comp8.csv.gz'
]

dfs = []

for file in similarity_files:
    df = pd.read_csv(file, compression='gzip')
    dfs.append(df)

similarity = pd.concat(dfs, ignore_index=True)

st.set_page_config(page_title="Movie Recommender", layout="wide")

background_image_url = "https://images3.alphacoders.com/882/882717.jpg"

st.markdown(
    f"""
    <style>
    body {{
        background: url("{background_image_url}") no-repeat center center fixed;
        background-size: cover;
        color: white;
    }}
    .main-container {{
        background: rgba(0, 0, 0, 0.8);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 5px 20px rgba(255, 75, 75, 0.4);
    }}
    .title {{
        color: #ff4b4b;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        background-color: rgba(0, 0, 0, 0.6);
        padding: 10px;
        border-radius: 10px;
    }}
    .subheader {{
        color: #ffffff;
        text-align: center;
        font-size: 22px;
        background-color: rgba(0, 0, 0, 0.5);
        padding: 5px;
        border-radius: 10px;
    }}
    .row-container {{
        margin-bottom: 30px;  /* Adds gap between rows */
    }}
    .movie-container {{
        border: 3px solid #ff4b4b;
        border-radius: 10px;
        padding: 15px;
        background: rgba(0, 0, 0, 0.7);
        text-align: center;
        box-shadow: 0px 5px 15px rgba(255, 75, 75, 0.6);
        transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
    }}
    .movie-container:hover {{
        transform: scale(1.05);
        box-shadow: 0px 8px 25px rgba(255, 75, 75, 0.8);
    }}
    .movie-title {{
        color: white;
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 5px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="title">🎬 Movie Recommender System 🍿</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Find movies similar to your favorite ones!</p>', unsafe_allow_html=True)
st.write("---")

selected_movie_name = st.selectbox(
    "🎞️ Select a movie to get recommendations:",
    movies['title'].values
)

if st.button("🎥 Get Recommendations"):
    names, posters = recommend(selected_movie_name)

    st.write('<div class="main-container">', unsafe_allow_html=True)
    st.write("### **Recommended Movies for You:**")

    total_recommendations = len(names)
    num_columns = 5  # Number of columns per row

    for row in range(0, total_recommendations, num_columns):
        st.markdown('<div class="row-container">', unsafe_allow_html=True)
        cols = st.columns(num_columns)  # Create 5 columns
        for i in range(num_columns):
            index = row + i
            if index < total_recommendations:
                with cols[i]:
                    st.markdown(
                        f"""
                        <div class="movie-container">
                            <p class="movie-title">{names[index]}</p>
                            <img src="{posters[index]}" width="100%" style="border-radius: 10px;">
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        st.markdown('</div>', unsafe_allow_html=True)
    st.write('</div>', unsafe_allow_html=True)
