import unittest 
import MusicHistory

class MusicHistoryTest(unittest.TestCase):
    #########################
    #### BLACK BOX TESTS ####
    #########################
    """ testing compute genre """
    # need to update data frequently 
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
        genre_data = ['pop', 'post-teen pop', 'dance pop', 'electropop', 'alternative r&b', 'pop dance', 'r&b', 'art pop', 'pop rap', 'indie r&b']
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
        artist_data = ["Ariana Grande", "Taylor Swift"]
        self.assertEqual(MusicHistory.compute_top_artists("short_term", 5),artist_data)
    def test_compute_top_artist_medium(self):
        artist_data = ["Taylor Swift", "Ariana Grande", "Kehlani", "Rina Sawayama", "Lauv"]
        self.assertEqual(MusicHistory.compute_top_artists("medium_term", 5), artist_data)
    def test_compute_top_artist_long(self):
        artist_data = ["Taylor Swift", "Ariana Grande", "Shawn Mendes", "Ed Sheeran", "Avril Lavigne"]
        self.assertEqual(MusicHistory.compute_top_artists("long_term", 5), artist_data)
    def test_compute_top_artist_few(self):
        artist_data = ["Taylor Swift", "Ariana Grande"]
        self.assertEqual(MusicHistory.compute_top_artists("medium_term", 2), artist_data)
    def test_compute_top_artist_many(self):
        artist_data = ["Taylor Swift", "Ariana Grande", "Kehlani", "Rina Sawayama", "Lauv", "NIKI", "Frank Ocean", "Jeremy Zucker", "UMI", "Phoebe Bridgers"]
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

    #########################
    #### WHITE BOX TESTS ####
    #########################

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MusicHistoryTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
