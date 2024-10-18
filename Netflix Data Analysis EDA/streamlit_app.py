import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Load the dataset
@st.cache_data
def load_data():
    data = pd.read_csv('netflix_data.csv')  
    return data

# Main function for the Streamlit app
def main():
    st.title("Netflix Content Analysis")

    # Load the data
    netflix_data = load_data()

    # Data Overview
    if st.checkbox("Show Data Overview"):
        st.write(netflix_data.head())

    # Content Availability by Country
    st.subheader("Content Availability by Country")
    country_counts = netflix_data['country'].value_counts().head(10)
    st.bar_chart(country_counts)

    # TV Shows vs Movies
    st.subheader("TV Shows vs Movies Over the Years")
    tv_movie_trend = netflix_data.groupby(['release_year', 'type']).size().unstack().fillna(0)
    st.bar_chart(tv_movie_trend)

    # Genre Distribution
    st.subheader("Genre Distribution in Top Countries")
    genre_counts = netflix_data['listed_in'].str.split(', ')
    genre_counts = genre_counts.explode().value_counts().head(10)
    st.bar_chart(genre_counts)

    # Optimal Launch Period for TV Shows
    # Clean and parse the date_added column
    netflix_data['date_added'] = pd.to_datetime(netflix_data['date_added'].str.strip(), errors='coerce')

    # Check for NaT values
    if netflix_data['date_added'].isnull().any():
        problematic_dates = netflix_data[netflix_data['date_added'].isnull()]['date_added']
        st.warning("Some dates could not be parsed and have been set to NaT.")
        st.write("The following problematic dates could not be parsed:")
        st.write(problematic_dates)  # Show problematic rows

    netflix_data['month_added'] = netflix_data['date_added'].dt.month_name()
    tv_shows_per_month = netflix_data[netflix_data['type'] == 'TV Show']['month_added'].value_counts()
    tv_shows_per_month = tv_shows_per_month.reindex(['January', 'February', 'March', 'April', 'May', 'June',
                                                      'July', 'August', 'September', 'October', 'November', 'December'])
    st.bar_chart(tv_shows_per_month)

    # Director and Actor Analysis
    st.subheader("Top Directors and Actors")
    top_directors = netflix_data['director'].value_counts().head(10)
    top_actors = netflix_data['cast'].apply(lambda x: x.split(',')[0] if isinstance(x, str) else 'Unknown').value_counts().head(10)
    
    # Plotting directors
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    top_directors.plot(kind='bar', ax=ax[0], color='salmon')
    ax[0].set_title('Top 10 Directors')
    ax[0].set_xlabel('Director')
    ax[0].set_ylabel('Number of Titles')
    
    # Plotting actors
    top_actors.plot(kind='bar', ax=ax[1], color='lightgreen')
    ax[1].set_title('Top 10 Actors')
    ax[1].set_xlabel('Actor')
    ax[1].set_ylabel('Number of Titles')
    
    st.pyplot(fig)

if __name__ == "__main__":
    main()
