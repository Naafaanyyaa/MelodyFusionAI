import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import warnings

warnings.filterwarnings('ignore')

song_library = pd.read_csv('../Data/song_library.csv', na_filter=False)

song_library.drop(['id_artists'], axis=1, inplace=True)

song_vectorizer = CountVectorizer()

song_vectorizer.fit(song_library['genres'])

def song_recommender(first_song_id, second_song_id):
    try:
        num_cols = ['release_year', 'duration_s', 'popularity', 'danceability', 'energy', 'key', 'loudness',
                    'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

        text_vec1 = song_vectorizer.transform(song_library[song_library['id'] == str(first_song_id)]['genres']).toarray()
        text_vec2 = song_vectorizer.transform(song_library[song_library['id'] == str(second_song_id)]['genres']).toarray()

        num_vec1 = song_library[song_library['id'] == str(first_song_id)][num_cols].to_numpy()
        num_vec2 = song_library[song_library['id'] == str(second_song_id)][num_cols].to_numpy()

        sim_scores = []

        for index, row in song_library.iterrows():
            name = row['id']

            text_vec_other = song_vectorizer.transform(song_library[song_library['id'] == name]['genres']).toarray()

            num_vec_other = song_library[song_library['id'] == name][num_cols].to_numpy()

            text_sim1 = cosine_similarity(text_vec1, text_vec_other)[0][0]
            text_sim2 = cosine_similarity(text_vec2, text_vec_other)[0][0]

            num_sim1 = cosine_similarity(num_vec1, num_vec_other)[0][0]
            num_sim2 = cosine_similarity(num_vec2, num_vec_other)[0][0]

            sim = (text_sim1 + num_sim1 + text_sim2 + num_sim2) / 4
            sim_scores.append(sim)

        song_library['similarity'] = sim_scores

        song_library.sort_values(by=['similarity', 'popularity', 'release_year'], ascending=[False, False, False],
                                 inplace=True)

        recommended_songs = song_library[['id']][2:7]

        return recommended_songs
    except:
        error_msg = '{} or {} not found in songs library.'.format(first_song_id, second_song_id)
        return error_msg
