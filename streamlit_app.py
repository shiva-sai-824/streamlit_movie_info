import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from datetime import datetime
import os


# Initialize session state variables
if 'loginres' not in st.session_state:
    st.session_state.loginres = None
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'movie_lists' not in st.session_state:
    st.session_state.movie_lists = {}  # Store movie lists with privacy settings
if 'current_list' not in st.session_state:
    st.session_state.current_list = None


# Load user credentials from a file
user_credentials = {}
if os.path.isfile("user_credentials.txt"):
    with open("user_credentials.txt", "r") as f:
        for line in f:
            username, password = line.strip().split(":")
            user_credentials[username] = password


def handle_login(username, password):
    if username in user_credentials and user_credentials[username] == password:
        st.session_state.loginres = {"user": username}
        st.session_state.logged_in = True
        st.success("Logged in successfully")

        # Load or initialize user's favorite movies
        if username in st.session_state.movie_lists:
            st.session_state.current_list = st.session_state.movie_lists[username]
        else:
            st.session_state.current_list = {
                "movies": [], "privacy": "Private", "user": username}
    else:
        st.error(
            "Incorrect username or password. Please sign up if you haven't already.")


def handle_logout():
    st.session_state.loginres = None
    st.session_state.logged_in = False
    st.info("Logged out successfully")


def signup():
    st.title("Signup")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Signup"):
        if username not in user_credentials:
            user_credentials[username] = password
            with open("user_credentials.txt", "a") as f:
                f.write(f"{username}:{password}\n")
            handle_login(username, password)
        else:
            st.warning(
                "Username already exists. Please choose a different one.")


def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in user_credentials:
            if user_credentials[username] == password:
                handle_login(username, password)
            else:
                st.error("Incorrect password. Please try again.")
        else:
            st.error("Username not found. Please sign up if you haven't already.")


# Navbar component


def navbar():
    st.sidebar.header(f"Welcome, {st.session_state.loginres['user']}!")
    st.sidebar.button("Logout", on_click=handle_logout)


def movie_finder_app():
    st.title("Movie Finder App")

    # User input for movie title
    movie_title = st.text_input("Enter Movie Title", "")

    # Current Year
    current_year = datetime.now().year

    # Dataframe for storing all movie data
    movies_df = pd.DataFrame()

    # Filter options
    type_filter = st.selectbox("Filter by Type", ["movie", "series"])
    year_filter = st.slider("Filter by Release Year", min_value=1900,
                            max_value=current_year, step=1, value=(1900, current_year))
    rating_filter = st.slider("Filter by IMDb Rating", min_value=0.0,
                              max_value=10.0, step=0.1, value=(0.0, 10.0))

    # Search for the movie using the OMDB API
    if movie_title:
        omdb_api_url = "http://www.omdbapi.com/"
        # OMDb API key (you need to sign up for a free API key)
        api_key = "6449cfca"

        params = {
            "apikey": api_key,
            "t": movie_title,  # Use 't' instead of 's' for searching by movie title
            "type": type_filter,
            "y": f"{year_filter[0]}-{year_filter[1]}",
            "r": "json"
        }

        with st.spinner('Processing...'):
            response = requests.get(omdb_api_url, params=params)
            data = response.json()

            # Filter and display movie details
            if data.get("Response") == "True":
                detailed_data = data  # No need for additional request since we got detailed data directly
                detailed_data["Year"] = detailed_data["Year"].rstrip("–")

                # Apply additional filters
                if (
                    (
                        type_filter == 'movie' and
                        year_filter[0] <= int(detailed_data["Year"]) <= year_filter[1] and
                        detailed_data.get("imdbRating") != "N/A" and
                        rating_filter[0] <= float(
                            detailed_data["imdbRating"]) <= rating_filter[1]
                    ) or
                    (
                        type_filter == 'series' and
                        detailed_data.get("imdbRating") != "N/A" and
                        rating_filter[0] <= float(
                            detailed_data["imdbRating"]) <= rating_filter[1]
                    )
                ):
                    # Temporarily store movie detail in this dataframe.
                    new_row_df = pd.DataFrame({
                        'Poster': [detailed_data['Poster']],
                        'Title': [f"{detailed_data['Title']} ({detailed_data['Year']})"],
                        'Year': [detailed_data['Year']],
                        'Rated': [detailed_data.get('Rated')],
                        'Runtime': [detailed_data.get('Runtime')],
                        'Released': [detailed_data.get('Released')],
                        'Genre': [detailed_data.get('Genre')],
                        'Director': [detailed_data.get('Director')],
                        'Writer': [detailed_data.get('Writer')],
                        'Actors': [detailed_data.get('Actors')],
                        'Language': [detailed_data.get('Language')],
                        'Country': [detailed_data.get('Country')],
                        'Awards': [detailed_data.get('Awards')],
                        'Plot': [detailed_data.get('Plot')],
                        'IMDB Rating': [detailed_data.get('imdbRating')],
                        'IMDB Votes': [detailed_data.get('imdbVotes')]
                    })

                    # Add movie detail dataframe to the main dataframe containing all movies
                    movies_df = pd.concat(
                        [movies_df, new_row_df], ignore_index=True)
            else:
                st.warning("No movie found for the specified criteria.")

    # Setup tabs
    tab1, tab2 = st.tabs(["Search Results", "Ratings and Votes"])

    # Search Results: List of movie details
    with tab1:
        if len(movies_df) > 0:
            st.header("Search Results")
            for i in range(len(movies_df)):
                col1, col2 = st.columns([1, 2])
                with col1:
                    # Display movie poster
                    if movies_df['Poster'][i] != "N/A":
                        st.image(
                            movies_df['Poster'][i], caption=movies_df['Title'][i], use_column_width=True)
                    else:
                        # If there is no movie poster, use custom movie poster
                        st.image("film-solid.png")

                with col2:
                    # Display movie details
                    st.subheader(movies_df['Title'][i])

                    col1, col2, col3 = st.columns(3)
                    col1.write(f"IMDb Rating: {movies_df['IMDB Rating'][i]}")
                    col2.write(f"Rated: {movies_df['Rated'][i]}")
                    col3.write(f"Runtime: {movies_df['Runtime'][i]}")

                    st.write(f"Released: {movies_df['Released'][i]}")
                    st.write(f"Genre: {movies_df['Genre'][i]}")
                    st.write(f"Director: {movies_df['Director'][i]}")
                    st.write(f"Writer: {movies_df['Writer'][i]}")
                    st.write(f"Actors: {movies_df['Actors'][i]}")
                    st.write(f"Plot: {movies_df['Plot'][i]}")
                    st.write(f"Language: {movies_df['Language'][i]}")
                    st.write(f"Country: {movies_df['Country'][i]}")
                    st.write(f"Awards: {movies_df['Awards'][i]}")

                    with st.form(key=f"form_{i}"):
                        list_name = st.text_input(
                            "Enter List Name", key=f"list_name_{i}")
                        list_privacy = st.selectbox(
                            "Privacy", ["Private", "Public"], key=f"privacy_{i}")
                        submit_button = st.form_submit_button(label="Add")
                        if submit_button:
                            if list_name:
                                if list_name not in st.session_state.movie_lists:
                                    st.session_state.movie_lists[list_name] = {
                                        "movies": [],
                                        "privacy": list_privacy,
                                        "user": st.session_state.loginres['user']
                                    }
                                st.session_state.movie_lists[list_name]["movies"].append(
                                    movies_df.iloc[i].to_dict())
                                st.success(f"Added to {list_name}")
                            else:
                                st.error("List name cannot be empty")

                st.divider()

    # Plots of Ratings and Votes
    with tab2:
        if len(movies_df) > 0:
            fig, ax = plt.subplots()
            ax.bar(movies_df['Title'], movies_df['IMDB Rating'])
            ax.set_title("IMDB Ratings")
            st.pyplot(fig)

            fig, ax = plt.subplots()
            ax.bar(movies_df['Title'], movies_df['IMDB Votes'])
            ax.set_title("IMDB Votes")
            st.pyplot(fig)


def home_page():
    st.title("My Movie Lists")

    user_lists = {name: data for name, data in st.session_state.movie_lists.items(
    ) if data["user"] == st.session_state.loginres['user']}

    if len(user_lists) == 0:
        st.write("No movie lists found. Create one from the Movie Finder page.")
    else:
        for list_name, list_data in user_lists.items():
            st.subheader(list_name)
            st.write(f"Privacy: {list_data['privacy']}")
            for movie in list_data["movies"]:
                st.write(f"- {movie['Title']} ({movie['Year']})")


def app():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to", ["Signup", "Login", "Home", "Movie Finder"])

    if page == "Signup":
        signup()
    elif st.session_state.logged_in:
        navbar()
        if page == "Home":
            home_page()
        elif page == "Movie Finder":
            movie_finder_app()
    else:
        # Check if the user has signed up before
        if 'loginres' in st.session_state and st.session_state.loginres is not None:
            handle_login(st.session_state.loginres["user"])
        else:
            login()

    # Update the user's favorite movies when they add to their list
    if st.session_state.logged_in and st.session_state.current_list:
        st.session_state.movie_lists[st.session_state.current_list["user"]
                                     ] = st.session_state.current_list


if __name__ == "__main__":
    app()
