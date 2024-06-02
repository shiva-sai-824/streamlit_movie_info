
# Movie Information Streamlit App

Welcome to the Movie Information Streamlit App! This app allows you to search for movies, view their details, and even create your own movie lists.

## Features

- **Signup and Login:** Users can sign up for a new account or log in with existing credentials to access personalized features.
- **Movie Finder:** Search for movies by title, filter by type (movie or series), release year, and IMDb rating. The app retrieves movie details from the OMDb API and displays relevant information such as poster, title, year, rating, plot, director, and more.
- **Add to Lists:** Users can add their favorite movies to personalized lists, specifying the list name and privacy settings (private or public).
- **View Lists:** Users can view their own movie lists on the "Home" page, organized by list name and privacy settings.

## Usage

1. **Signup/Login:** 
    - If you are a new user, click on the "Signup" option and provide a username and password.
    - If you already have an account, click on the "Login" option and enter your credentials.

2. **Movie Finder:**
    - Enter the title of the movie you want to search for in the text input field.
    - Optionally, apply filters for type, release year, and IMDb rating using the dropdown menus and sliders.
    - Click on the "Search" button to retrieve movie details.

3. **Add to Lists:**
    - After searching for a movie, you can add it to your personalized lists by entering a list name and selecting the privacy settings (private or public).
    - Click on the "Add" button to add the movie to the selected list.

4. **View Lists:**
    - Navigate to the "Home" page to view your personalized movie lists.
    - Lists are organized by name and display the privacy settings.
    - Each movie in the list shows the title and year.

## Installation

To run this app locally, follow these steps:

1. Clone this repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Run the app using the command `streamlit run streamlit_app.py`.

## Technologies Used

- Streamlit: Frontend framework for building interactive web apps with Python.
- Plotly Express: Visualization library for creating interactive plots and charts.
- Pandas: Data manipulation and analysis library for working with tabular data.
- Requests: HTTP library for making API requests.
- datetime: Module for manipulating dates and times in Python.

## Credits

- **OMDb API:** The Open Movie Database API is used to retrieve movie details.

## Author

- [Shiva Sai K]

---
