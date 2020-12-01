import unittest 
import MusicHistory

class MusicHistoryTest(unittest.TestCase):
    #########################
    #### BLACK BOX TESTS ####
    #########################
    """ testing compute genre """
    #need to update data frequently 
    def test_compute_genre_short(self):
        genre_data = ['pop', 'post-teen pop', 'dance pop', 'pop dance']
        self.assertEqual(MusicHistory.compute_genre("short_term", 5), genre_data)
    def test_compute_genre_medium(self):
        genre_data = ['pop', 'post-teen pop', 'dance pop', 'electropop', 'alternative r&b']
        self.assertEqual(MusicHistory.compute_genre("medium_term", 5), genre_data)
    def test_compute_genre_long(self):
        genre_data  = ['pop', 'post-teen pop', 'dance pop', 'electropop', 'pop dance']
        self.assertEqual(MusicHistory.compute_genre("long_term", 5), genre_data)
    def test_compute_genre_few(self):
        genre_data = ['pop']
        self.assertEqual(MusicHistory.compute_genre("medium_term", 1), genre_data)
    def test_compute_genre_many(self):
        genre_data = ['pop', 'post-teen pop', 'dance pop', 'electropop', 'alternative r&b', 'pop rap', 'r&b', 'pop dance', 'indonesian r&b', 'bedroom soul']
        self.assertEqual(MusicHistory.compute_genre("medium_term", 10), genre_data)

    """ testing compute top songs """
    # need to update data frequently 
    def test_compute_top_song_short(self):
        song_data = {'2cYALQZNXmuFGp2ecgpKMa': ['cellophane', 'FKA twigs'], '6Im9k8u9iIzKMrmV7BWtlF': ['34+35', 'Ariana Grande'], '0WdR2AyLW1Drd3OUdwezM0': ['everytime', 'Ariana Grande'], '49UDOG8DoBajXTJSTqfRMg': ['Kyoto', 'Phoebe Bridgers'], '15ahYSiHAIMxAnujlXVtta': ['Super Far', 'LANY']}
        self.assertEqual(MusicHistory.compute_top_songs("short_term", 5),song_data)
    def test_compute_top_song_medium(self):
        song_data = {'1ApN1loxlt0rzRFc8iETw7': ['Bad Friend', 'Rina Sawayama'], '2cYALQZNXmuFGp2ecgpKMa': ['cellophane', 'FKA twigs'], '5E30LdtzQTGqRvNd7l6kG5': ['Daddy Issues', 'The Neighbourhood'], '3eGsNpXzcb1BDkfSJI54NY': ['Strawberry Blond', 'Mitski'], '3HZuxQ80VWOsBWws8XQdFB': ['F2020', 'Avenue Beat']}
        self.assertEqual(MusicHistory.compute_top_songs("medium_term", 5), song_data)
    def test_compute_top_song_long(self):
        song_data = {'5bgwqaRSS3M8WHWruHgSL5': ['8TEEN', 'Khalid'], '1KHGSJPHiHkG2FEGFy8fLc': ['Pompeii', 'Jasmine Thompson'], '6ZevjRLgEEXYagcPRE1cxY': ['Capsize', 'Grace Grundy'], '1TEL6MlSSVLSdhOSddidlJ': ['needy', 'Ariana Grande'], '3dP0pLbg9OfVwssDjp9aT0': ['Satisfied', 'Renée Elise Goldsberry']}
        self.assertEqual(MusicHistory.compute_top_songs("long_term", 5), song_data)
    def test_compute_top_song_few(self):
        song_data = {'1ApN1loxlt0rzRFc8iETw7': ['Bad Friend', 'Rina Sawayama'] }
        self.assertEqual(MusicHistory.compute_top_songs("medium_term", 1), song_data)
    def test_compute_top_song_many(self):
        song_data = {'1ApN1loxlt0rzRFc8iETw7': ['Bad Friend', 'Rina Sawayama'], '2cYALQZNXmuFGp2ecgpKMa': ['cellophane', 'FKA twigs'], '5E30LdtzQTGqRvNd7l6kG5': ['Daddy Issues', 'The Neighbourhood'], '3eGsNpXzcb1BDkfSJI54NY': ['Strawberry Blond', 'Mitski'], '3HZuxQ80VWOsBWws8XQdFB': ['F2020', 'Avenue Beat'], '5oruuYKxGXcS0Cm1hpRLup': ['Cancelled.', 'Kiana Ledé'], '6LxcPUqx6noURdA5qc4BAT': ['Motion Sickness', 'Phoebe Bridgers'], '6Im9k8u9iIzKMrmV7BWtlF': ['34+35', 'Ariana Grande'], '0WdR2AyLW1Drd3OUdwezM0': ['everytime', 'Ariana Grande'], '6TrdeNEgbKuBqIToRfdWMY': ['Everybody Business', 'Kehlani']}
        self.assertEqual(MusicHistory.compute_top_songs("medium_term", 10), song_data)
    
    """ testing compute top artists  """
    # need to update data frequently 
    def test_compute_top_artist_short(self):
        artist_data = ['Ariana Grande', 'Taylor Swift']
        self.assertEqual(MusicHistory.compute_top_artists("short_term", 5),artist_data)
    def test_compute_top_artist_medium(self):
        artist_data = ['Ariana Grande', 'Taylor Swift', 'Kehlani', 'Lauv', 'NIKI']
        self.assertEqual(MusicHistory.compute_top_artists("medium_term", 5), artist_data)
    def test_compute_top_artist_long(self):
        artist_data = ["Taylor Swift", "Ariana Grande", "Shawn Mendes", "Ed Sheeran", "Avril Lavigne"]
        self.assertEqual(MusicHistory.compute_top_artists("long_term", 5), artist_data)
    def test_compute_top_artist_few(self):
        artist_data = ['Ariana Grande', 'Taylor Swift']
        self.assertEqual(MusicHistory.compute_top_artists("medium_term", 2), artist_data)
    def test_compute_top_artist_many(self):
        artist_data = ['Ariana Grande', 'Taylor Swift', 'Kehlani', 'Lauv', 'NIKI', 'UMI', 'Jeremy Zucker', 'Phoebe Bridgers', 'SZA', 'Kiana Ledé']
        self.assertEqual(MusicHistory.compute_top_artists("medium_term", 10), artist_data)
    
    """ testing compute top song theory  """
    def test_compute_top_song_theory_short(self):
        song_theory_data = {'tempo': 118.41, 'time_signature': 4.0, 'key': ['2', '0', '10', '11', '1'], 'mode': ['1'], 'mood': 0.47, 'danceability': 0.66, 'acousticness': 0.29, 'energy': 0.54, 'instrumentalness': 0.06}
        short_songs = [['cellophane', 'FKA twigs'], ['34+35', 'Ariana Grande'], ['everytime', 'Ariana Grande'], ['Kyoto', 'Phoebe Bridgers'], ['Super Far', 'LANY']]
        self.assertEqual(MusicHistory.compute_top_songs_theory(short_songs),song_theory_data)
    def test_compute_top_song_theory_medium(self):
        song_theory_data = {'tempo': 89.87, 'time_signature': 4.0, 'key': ['2'], 'mode': ['1'], 'mood': 0.47, 'danceability': 0.6, 'acousticness': 0.52, 'energy': 0.53, 'instrumentalness': 0.03}
        med_songs = [['Bad Friend', 'Rina Sawayama'], ['cellophane', 'FKA twigs'], ['Daddy Issues', 'The Neighbourhood'], ['Strawberry Blond', 'Mitski'], ['F2020', 'Avenue Beat']]
        self.assertEqual(MusicHistory.compute_top_songs_theory(med_songs), song_theory_data)
    def test_compute_top_song_theory_long(self):
        song_theory_data = {'tempo': 123.76, 'time_signature': 4.0, 'key': ['1', '9', '3', '7', '5'], 'mode': ['1'], 'mood': 0.41, 'danceability': 0.63, 'acousticness': 0.63, 'energy': 0.38, 'instrumentalness': 0.0}
        long_songs = [['8TEEN', 'Khalid'], ['Pompeii', 'Jasmine Thompson'], ['Capsize', 'Grace Grundy'], ['needy', 'Ariana Grande'], ['Satisfied', 'Renée Elise Goldsberry']]
        self.assertEqual(MusicHistory.compute_top_songs_theory(long_songs), song_theory_data)
    def test_compute_top_song_theory_few(self):
        song_theory_data = {'tempo': 95.03, 'time_signature': 4.0, 'key': ['3'], 'mode': ['1'], 'mood': 0.46, 'danceability': 0.6, 'acousticness': 0.21, 'energy': 0.72, 'instrumentalness': 0.0}
        few_songs = [['Bad Friend', 'Rina Sawayama']]
        self.assertEqual(MusicHistory.compute_top_songs_theory(few_songs), song_theory_data)
    def test_compute_top_song_theory_many(self):
        song_theory_data = {'tempo': 105.54, 'time_signature': 3.9, 'key': ['2'], 'mode': ['1'], 'mood': 0.5, 'danceability': 0.61, 'acousticness': 0.48, 'energy': 0.56, 'instrumentalness': 0.02}
        many_songs = [['Bad Friend', 'Rina Sawayama'], ['cellophane', 'FKA twigs'], ['Daddy Issues', 'The Neighbourhood'], ['Strawberry Blond', 'Mitski'], ['F2020', 'Avenue Beat'], ['Cancelled.', 'Kiana Ledé'], ['Motion Sickness', 'Phoebe Bridgers'], ['34+35', 'Ariana Grande'], ['everytime', 'Ariana Grande'], ['Everybody Business', 'Kehlani']]
        self.assertEqual(MusicHistory.compute_top_songs_theory(many_songs), song_theory_data)

    # TO DO add reply methods to black box testing
    
    #########################
    #### WHITE BOX TESTS ####
    #########################
    
    """ testing compute genre helper method"""
    def test_compute_genre_helper_empty(self):
        genre_dictionary = {}
        limit = 4
        top_genres = []
        self.assertEqual(MusicHistory.compute_genre_helper(genre_dictionary, limit), top_genres)
    def test_compute_genre_helper_tie(self):
        genre_dictionary = {"pop": [1, 3], "r&b": [2,5], "indie": [2,4]}
        limit = 3
        top_genres = ["pop", "indie", "r&b"]
        self.assertEqual(MusicHistory.compute_genre_helper(genre_dictionary, limit), top_genres)
    def test_compute_genre_helper_no_tie(self):
        genre_dictionary = {"pop": [1], "r&b": [1,4], "indie": [1, 2, 3]}
        limit = 3
        top_genres = ["indie", "r&b", "pop"]
        self.assertEqual(MusicHistory.compute_genre_helper(genre_dictionary, limit), top_genres)
    def test_compute_genre_helper_small_limit(self):
        genre_dictionary = {"pop": [1], "r&b": [1,4], "indie": [1, 2, 3]}
        limit = 1
        top_genres = ["indie"]
        self.assertEqual(MusicHistory.compute_genre_helper(genre_dictionary, limit), top_genres)
    def test_compute_genre_helper_small_limit(self):
        genre_dictionary = {"pop": [1], "r&b": [1,4], "indie": [1, 2, 3]}
        limit = 6
        top_genres = ["indie", "r&b", "pop"]
        self.assertEqual(MusicHistory.compute_genre_helper(genre_dictionary, limit), top_genres)

    """ testing compute top song theory helper """
    def test_compute_theory_helper_key_tie(self):
        theory_dict = {'tempo': [95.025, 106.973, 85.012, 77.332],
                       'time_signature': [4, 4, 3, 4],
                       'key': ['3', '2', '2', '3'],
                       'mode': ['1', '1', '1', '0'],
                       'mood':[0.462, 0.228, 0.337, 0.943],
                       'danceability': [0.598, 0.563, 0.588, 0.553],
                       'acousticness': [0.215, 0.872, 0.0678, 0.839],
                       'energy': [0.72, 0.283, 0.521, 0.545],
                       'instrumentalness': [2.95e-06, 0.000143, 0.149, 0.0]}
        excepted_output_dict = {'tempo': 91.09,
                       'time_signature': 3.75,
                       'key': ['3', '2'],
                       'mode': ['1'],
                       'mood': 0.49,
                       'danceability': 0.58,
                       'acousticness': 0.50,
                       'energy': 0.52,
                       'instrumentalness': 0.04}
        self.assertEqual(MusicHistory.compute_top_songs_theory_helper(theory_dict), excepted_output_dict)
    def test_compute_theory_helper_mode_tie(self):
        theory_dict = {'tempo': [95.025, 106.973, 85.012, 77.332],
                       'time_signature': [4, 4, 3, 4],
                       'key': ['3', '2', '4', '3'],
                       'mode': ['1', '1', '0', '0'],
                       'mood':[0.462, 0.228, 0.337, 0.943],
                       'danceability': [0.598, 0.563, 0.588, 0.553],
                       'acousticness': [0.215, 0.872, 0.0678, 0.839],
                       'energy': [0.72, 0.283, 0.521, 0.545],
                       'instrumentalness': [2.95e-06, 0.000143, 0.149, 0.0]}
        excepted_output_dict = {'tempo': 91.09,
                       'time_signature': 3.75,
                       'key': ['3'],
                       'mode': ['1', '0'],
                       'mood': 0.49,
                       'danceability': 0.58,
                       'acousticness': 0.50,
                       'energy': 0.52,
                       'instrumentalness': 0.04}
        self.assertEqual(MusicHistory.compute_top_songs_theory_helper(theory_dict), excepted_output_dict)
    def test_compute_theory_helper_both_tie(self):
        theory_dict = {'tempo': [95.025, 106.973, 85.012, 77.332],
                       'time_signature': [4, 4, 3, 4],
                       'key': ['3', '2', '1', '4'],
                       'mode': ['1', '1', '0', '0'],
                       'mood':[0.462, 0.228, 0.337, 0.943],
                       'danceability': [0.598, 0.563, 0.588, 0.553],
                       'acousticness': [0.215, 0.872, 0.0678, 0.839],
                       'energy': [0.72, 0.283, 0.521, 0.545],
                       'instrumentalness': [2.95e-06, 0.000143, 0.149, 0.0]}
        excepted_output_dict = {'tempo': 91.09,
                       'time_signature': 3.75,
                       'key': ['3', '2', '1', '4'],
                       'mode': ['1', '0'],
                       'mood': 0.49,
                       'danceability': 0.58,
                       'acousticness': 0.50,
                       'energy': 0.52,
                       'instrumentalness': 0.04}
        self.assertEqual(MusicHistory.compute_top_songs_theory_helper(theory_dict), excepted_output_dict)
    def test_compute_theory_helper_no_tie(self):
        theory_dict = {'tempo': [95.025, 106.973, 85.012, 77.332],
                       'time_signature': [4, 4, 3, 4],
                       'key': ['1', '1', '1', '4'],
                       'mode': ['1', '0', '0', '0'],
                       'mood':[0.462, 0.228, 0.337, 0.943],
                       'danceability': [0.598, 0.563, 0.588, 0.553],
                       'acousticness': [0.215, 0.872, 0.0678, 0.839],
                       'energy': [0.72, 0.283, 0.521, 0.545],
                       'instrumentalness': [2.95e-06, 0.000143, 0.149, 0.0]}
        excepted_output_dict = {'tempo': 91.09,
                       'time_signature': 3.75,
                       'key': ['1'],
                       'mode': ['0'],
                       'mood': 0.49,
                       'danceability': 0.58,
                       'acousticness': 0.50,
                       'energy': 0.52,
                       'instrumentalness': 0.04}
        self.assertEqual(MusicHistory.compute_top_songs_theory_helper(theory_dict), excepted_output_dict)
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MusicHistoryTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
