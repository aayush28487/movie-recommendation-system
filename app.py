import streamlit as st
import pickle
import requests


# -----------------------------------------
# Page Configuration
# -----------------------------------------

st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)


# -----------------------------------------
# Fetch Movie Poster
# -----------------------------------------

def fetch_poster(movie_id, movie_title):

    API_KEY = "691105c942b734886a4953b000a2e585"

    # Method 1: Try using movie ID
    try:

        url = f"https://api.themoviedb.org/3/movie/{movie_id}"

        params = {
            "api_key": API_KEY,
            "language": "en-US"
        }

        response = requests.get(
            url,
            params=params,
            timeout=5
        )

        if response.status_code == 200:

            data = response.json()

            poster_path = data.get("poster_path")

            if poster_path:

                return (
                    "https://image.tmdb.org/t/p/w500"
                    + poster_path
                )

    except Exception:
        pass


    # Method 2: Search movie by title
    try:

        search_url = "https://api.themoviedb.org/3/search/movie"

        params = {
            "api_key": API_KEY,
            "query": movie_title,
            "language": "en-US",
            "include_adult": False
        }

        response = requests.get(
            search_url,
            params=params,
            timeout=5
        )

        if response.status_code == 200:

            data = response.json()

            results = data.get("results", [])

            if results:

                poster_path = results[0].get("poster_path")

                if poster_path:

                    return (
                        "https://image.tmdb.org/t/p/w500"
                        + poster_path
                    )

    except Exception:
        pass


    return None


# -----------------------------------------
# Recommendation Function
# -----------------------------------------

def recommend(movie):

    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]


    recommend_movies = []

    recommended_movie_posters = []


    for i in movies_list:

        movie_id = movies.iloc[i[0]]["movie_id"]

        movie_name = movies.iloc[i[0]]["title"]

        recommend_movies.append(movie_name)

        poster = fetch_poster(
            movie_id,
            movie_name
        )

        recommended_movie_posters.append(poster)


    return recommend_movies, recommended_movie_posters


# -----------------------------------------
# Load Pickle Files
# -----------------------------------------

movies = pickle.load(
    open("movie_list.pkl", "rb")
)

similarity = pickle.load(
    open("similarity.pkl", "rb")
)


# -----------------------------------------
# Frontend
# -----------------------------------------

st.title("🎬 Movie Recommender System")

st.write(
    "Select a movie and get 5 similar movie recommendations."
)


# -----------------------------------------
# Movie Selection
# -----------------------------------------

selected_movie_name = st.selectbox(
    "Select your movie",
    movies["title"].values
)


# -----------------------------------------
# Recommend Button
# -----------------------------------------

if st.button("Recommend"):

    names, posters = recommend(
        selected_movie_name
    )


    st.subheader("Recommended Movies")


    col1, col2, col3, col4, col5 = st.columns(5)


    columns = [
        col1,
        col2,
        col3,
        col4,
        col5
    ]


    for i in range(5):

        with columns[i]:

            st.write(names[i])


            if posters[i]:

                st.image(
                    posters[i],
                    use_container_width=True
                )

            else:

                st.info(
                    "Poster unavailable"
                )