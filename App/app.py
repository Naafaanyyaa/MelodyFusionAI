# Required libraries
# To read and handle data files
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)

# For creating vectors from text and determining similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Supress warnings
import warnings

warnings.filterwarnings('ignore')


# Song recommender
# Read song library data file
song_library = pd.read_csv('D:/Artem/Artem/4_course/Diploma/OurProj/App/song_library.csv', na_filter=False)

# Drop "id_artists" field from DataFrame
song_library.drop(['id_artists'], axis=1, inplace=True)

# Create CountVectorizer object to transform text into vector
song_vectorizer = CountVectorizer()

# Fit the vectorizer on "genres" field of song_library DataFrame
song_vectorizer.fit(song_library['genres'])


# Function to recommend more songs based on given song name
def song_recommender(first_song_id, second_song_id):
    try:
        # Numeric columns (audio features) in song_library DataFrame
        num_cols = ['release_year', 'duration_s', 'popularity', 'danceability', 'energy', 'key', 'loudness',
                    'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

        # Create vector from "genres" field (text data) for given songs
        text_vec1 = song_vectorizer.transform(song_library[song_library['id'] == str(first_song_id)]['genres']).toarray()
        text_vec2 = song_vectorizer.transform(song_library[song_library['id'] == str(second_song_id)]['genres']).toarray()

        # Create vector from numerical columns for given songs
        num_vec1 = song_library[song_library['id'] == str(first_song_id)][num_cols].to_numpy()
        num_vec2 = song_library[song_library['id'] == str(second_song_id)][num_cols].to_numpy()

        # Initialise empty list to store similarity scores
        sim_scores = []

        # For every song/track in song library, determine cosine similarity with given songs
        for index, row in song_library.iterrows():
            name = row['id']

            # Create vector from "genres" field for other songs
            text_vec_other = song_vectorizer.transform(song_library[song_library['id'] == name]['genres']).toarray()

            # Create vector from numerical columns for other songs
            num_vec_other = song_library[song_library['id'] == name][num_cols].to_numpy()

            # Calculate cosine similarity using text vectors
            text_sim1 = cosine_similarity(text_vec1, text_vec_other)[0][0]
            text_sim2 = cosine_similarity(text_vec2, text_vec_other)[0][0]

            # Calculate cosine similarity using numerical vectors
            num_sim1 = cosine_similarity(num_vec1, num_vec_other)[0][0]
            num_sim2 = cosine_similarity(num_vec2, num_vec_other)[0][0]

            # Take average of both similarity scores and add to list of similarity scores
            sim = (text_sim1 + num_sim1 + text_sim2 + num_sim2) / 4
            sim_scores.append(sim)

        # Add new column containing similarity scores to song_library DataFrame
        song_library['similarity'] = sim_scores

        # Sort DataFrame based on "similarity" column
        song_library.sort_values(by=['similarity', 'popularity', 'release_year'], ascending=[False, False, False],
                                 inplace=True)

        # Create DataFrame "recommended_songs" containing 5 songs that are most similar to the given songs
        recommended_songs = song_library[['id']][2:7]

        return recommended_songs
    except:
        # If given song is not found in song library then return error message
        error_msg = '{} or {} not found in songs library.'.format(first_song_id, second_song_id)
        return error_msg
