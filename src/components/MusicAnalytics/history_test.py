import unittest 
import MusicHistory

class MusicHistoryTest(unittest.TestCase):
    #########################
    #### BLACK BOX TESTS ####
    #########################
    """ TESTING COMPUTE GENRE 
    check that the outputted genre(s) are equal to the expected hard-coded data from
    my own Spotify account using the Spotify Web API.

    NOTE: genre_data (hard coded) needs to be updated as I listen to more music 
    """
    def test_compute_genre_short(self):
        genre_data = ['pop', 'post-teen pop', 'dance pop', 'pop dance', 'alternative r&b']

        # compute genre with "short_term" parameter 
        self.assertEqual(MusicHistory.compute_genre("short_term", 5), genre_data)
    
    def test_compute_genre_medium(self):
        genre_data = ['pop', 'post-teen pop', 'dance pop', 'electropop', 'alternative r&b']
        
        # compute genre call with "medium_term" parameter 
        self.assertEqual(MusicHistory.compute_genre("medium_term", 5), genre_data)
    
    def test_compute_genre_long(self):
        genre_data  = ['pop', 'post-teen pop', 'dance pop', 'electropop', 'pop dance']
        
        # compute genre call with "long_term" parameter 
        self.assertEqual(MusicHistory.compute_genre("long_term", 5), genre_data)
    
    def test_compute_genre_few(self):
        genre_data = ['pop']
        
        # compute genre call a low limit
        self.assertEqual(MusicHistory.compute_genre("medium_term", 1), genre_data)
    
    def test_compute_genre_many(self):
        genre_data = ['pop', 'post-teen pop', 'dance pop', 'electropop', 'alternative r&b', 'pop rap', 'r&b', 'pop dance', 'indonesian r&b', 'bedroom soul']
        
        # compute genre call with a high limit 
        self.assertEqual(MusicHistory.compute_genre("medium_term", 10), genre_data)

    
    """ TESTING COMPUTE TOP SONGS 
    check that the outputted song(s) are equal to the expected hard-coded data from
    my own Spotify account using the Spotify Web API.

    NOTE: song_data (hard coded) needs to be updated as I listen to more music 
    """
    def test_compute_top_song_short(self):
        song_data = {'2cYALQZNXmuFGp2ecgpKMa': ['cellophane', 'FKA twigs'],
                    '6Im9k8u9iIzKMrmV7BWtlF': ['34+35', 'Ariana Grande'],
                    '0WdR2AyLW1Drd3OUdwezM0': ['everytime', 'Ariana Grande'],
                    '49UDOG8DoBajXTJSTqfRMg': ['Kyoto', 'Phoebe Bridgers'],
                    '2mtLGVN6xZm93wDG9nvviS': ['Wrong Places (from Songland)','H.E.R.']}

        # compute top song call with "short_term" parameter
        # check that outputted dict has correct keys
        self.assertEqual(MusicHistory.compute_top_songs("short_term", 5),song_data)
        
        # check that values are in the correct order 
        self.assertEqual(list(MusicHistory.compute_top_songs("short_term", 5).values()), list(song_data.values()))

    def test_compute_top_song_medium(self):
        song_data = {'1ApN1loxlt0rzRFc8iETw7': ['Bad Friend', 'Rina Sawayama'],
                    '2cYALQZNXmuFGp2ecgpKMa': ['cellophane', 'FKA twigs'],
                    '5E30LdtzQTGqRvNd7l6kG5': ['Daddy Issues', 'The Neighbourhood'],
                    '3eGsNpXzcb1BDkfSJI54NY': ['Strawberry Blond', 'Mitski'],
                    '3HZuxQ80VWOsBWws8XQdFB': ['F2020', 'Avenue Beat']}
        
        # compute top song call with "medium_term" parameter 
        # check that outputted dict has correct keys
        self.assertEqual(MusicHistory.compute_top_songs("medium_term", 5), song_data)

        # check that values are in the correct order 
        self.assertEqual(list(MusicHistory.compute_top_songs("medium_term", 5).values()), list(song_data.values()))

    def test_compute_top_song_long(self):
        song_data = {'5bgwqaRSS3M8WHWruHgSL5': ['8TEEN', 'Khalid'],
                    '1KHGSJPHiHkG2FEGFy8fLc': ['Pompeii', 'Jasmine Thompson'],
                    '6ZevjRLgEEXYagcPRE1cxY': ['Capsize', 'Grace Grundy'],
                    '1TEL6MlSSVLSdhOSddidlJ': ['needy', 'Ariana Grande'],
                    '3dP0pLbg9OfVwssDjp9aT0': ['Satisfied', 'Renée Elise Goldsberry']}
        
        # compute top song call with "long_term" parameter 
        self.assertEqual(MusicHistory.compute_top_songs("long_term", 5), song_data)

        # check that values are in the correct order 
        self.assertEqual(list(MusicHistory.compute_top_songs("long_term", 5).values()), list(song_data.values()))

    def test_compute_top_song_few(self):
        song_data = {'1ApN1loxlt0rzRFc8iETw7': ['Bad Friend', 'Rina Sawayama'] }
        
        # compute top song call with a low limit
        # check that outputted dict has correct keys
        self.assertEqual(MusicHistory.compute_top_songs("medium_term", 1), song_data)

        # check that values is correct 
        self.assertEqual(list(MusicHistory.compute_top_songs("medium_term", 1).values()), list(song_data.values()))

    
    def test_compute_top_song_many(self):
        song_data = {'1ApN1loxlt0rzRFc8iETw7': ['Bad Friend', 'Rina Sawayama'],
                    '2cYALQZNXmuFGp2ecgpKMa': ['cellophane', 'FKA twigs'],
                    '5E30LdtzQTGqRvNd7l6kG5': ['Daddy Issues', 'The Neighbourhood'],
                    '3eGsNpXzcb1BDkfSJI54NY': ['Strawberry Blond', 'Mitski'],
                    '3HZuxQ80VWOsBWws8XQdFB': ['F2020', 'Avenue Beat'],
                    '5oruuYKxGXcS0Cm1hpRLup': ['Cancelled.', 'Kiana Ledé'],
                    '6LxcPUqx6noURdA5qc4BAT': ['Motion Sickness', 'Phoebe Bridgers'],
                    '6Im9k8u9iIzKMrmV7BWtlF': ['34+35', 'Ariana Grande'],
                    '0WdR2AyLW1Drd3OUdwezM0': ['everytime', 'Ariana Grande'],
                    '6TrdeNEgbKuBqIToRfdWMY': ['Everybody Business', 'Kehlani']}
        
        # compute top song call with a high limit
        # check that outputted dict has correct keys
        self.assertEqual(MusicHistory.compute_top_songs("medium_term", 10), song_data)

        # check that values are in correct order
        self.assertEqual(list(MusicHistory.compute_top_songs("medium_term", 10).values()), list(song_data.values()))


    """ TESTING COMPUTE TOP ARTISTS
    check that the outputted artists(s) are equal to the expected hard-coded data from
    my own Spotify account using the Spotify Web API.

    NOTE: artist_data (hard coded) needs to be updated as I listen to more music
    """
    def test_compute_top_artist_short(self):
        artist_data = ['Ariana Grande', 'Taylor Swift', 'UMI']
        
        # compute top artist call with "short_term" parameter 
        self.assertEqual(MusicHistory.compute_top_artists("short_term", 5),artist_data)
    
    def test_compute_top_artist_medium(self):
        artist_data = ['Ariana Grande', 'Taylor Swift', 'Kehlani', 'Lauv', 'NIKI']
        
        # compute top artist call with "medium_term" parameter 
        self.assertEqual(MusicHistory.compute_top_artists("medium_term", 5), artist_data)
    
    def test_compute_top_artist_long(self):
        artist_data = ["Taylor Swift", "Ariana Grande", "Shawn Mendes", "Ed Sheeran", "Avril Lavigne"]
        
        # compute top artist call with "long_term" parameter 
        self.assertEqual(MusicHistory.compute_top_artists("long_term", 5), artist_data)
    
    def test_compute_top_artist_few(self):
        artist_data = ['Ariana Grande', 'Taylor Swift']
        
        # compute top artist call with low limit parameter 
        self.assertEqual(MusicHistory.compute_top_artists("medium_term", 2), artist_data)
    
    def test_compute_top_artist_many(self):
        artist_data = ['Ariana Grande', 'Taylor Swift', 'Kehlani', 'Lauv', 'NIKI', 'UMI', 'Jeremy Zucker', 'Phoebe Bridgers', 'SZA', 'Kiana Ledé']
        
        # compute top artist call with high limit
        self.assertEqual(MusicHistory.compute_top_artists("medium_term", 10), artist_data)
    

    """ TESTING COMPUTE TOP SONGS THEORY 
    check that the outputted theory dictionary is equal to the expected hard-coded data
    from the Spotify Web API

    NOTE: data is not dependent on user and does not require updating 
    """
    def test_compute_top_song_theory_short(self):
        song_theory_data = {'tempo': 118.41, 'time_signature': 4.0, 'key': ['2', '0', '10', '11', '1'], 'mode': ['1'], 'mood': 0.47, 'danceability': 0.66, 'acousticness': 0.29, 'energy': 0.54, 'instrumentalness': 0.06}
        
        # compute top song theory call with a sample list of "short_term" songs
        short_songs = [['cellophane', 'FKA twigs'], ['34+35', 'Ariana Grande'], ['everytime', 'Ariana Grande'], ['Kyoto', 'Phoebe Bridgers'], ['Super Far', 'LANY']]
        self.assertEqual(MusicHistory.compute_top_songs_theory(short_songs),song_theory_data)
    
    def test_compute_top_song_theory_medium(self):
        song_theory_data = {'tempo': 89.87, 'time_signature': 4.0, 'key': ['2'], 'mode': ['1'], 'mood': 0.47, 'danceability': 0.6, 'acousticness': 0.52, 'energy': 0.53, 'instrumentalness': 0.03}
        
        # compute top song theory call with a sample list of "medium_term" songs
        med_songs = [['Bad Friend', 'Rina Sawayama'], ['cellophane', 'FKA twigs'], ['Daddy Issues', 'The Neighbourhood'], ['Strawberry Blond', 'Mitski'], ['F2020', 'Avenue Beat']]
        self.assertEqual(MusicHistory.compute_top_songs_theory(med_songs), song_theory_data)
    
    def test_compute_top_song_theory_long(self):
        song_theory_data = {'tempo': 123.76, 'time_signature': 4.0, 'key': ['1', '9', '3', '7', '5'], 'mode': ['1'], 'mood': 0.41, 'danceability': 0.63, 'acousticness': 0.63, 'energy': 0.38, 'instrumentalness': 0.0}
        long_songs = [['8TEEN', 'Khalid'], ['Pompeii', 'Jasmine Thompson'], ['Capsize', 'Grace Grundy'], ['needy', 'Ariana Grande'], ['Satisfied', 'Renée Elise Goldsberry']]
        
        # compute top song theory call with a sample list of "long_term" songs
        self.assertEqual(MusicHistory.compute_top_songs_theory(long_songs), song_theory_data)
    
    def test_compute_top_song_theory_few(self):
        song_theory_data = {'tempo': 95.03, 'time_signature': 4.0, 'key': ['3'], 'mode': ['1'], 'mood': 0.46, 'danceability': 0.6, 'acousticness': 0.21, 'energy': 0.72, 'instrumentalness': 0.0}
        
        # compute top song theory call with a short sample list 
        few_songs = [['Bad Friend', 'Rina Sawayama']]
        self.assertEqual(MusicHistory.compute_top_songs_theory(few_songs), song_theory_data)
    
    def test_compute_top_song_theory_many(self):
        song_theory_data = {'tempo': 105.54, 'time_signature': 3.9, 'key': ['2'], 'mode': ['1'], 'mood': 0.5, 'danceability': 0.61, 'acousticness': 0.48, 'energy': 0.56, 'instrumentalness': 0.02}
        
        # compute top song theory call with a long sample list 
        many_songs = [['Bad Friend', 'Rina Sawayama'], ['cellophane', 'FKA twigs'], ['Daddy Issues', 'The Neighbourhood'], ['Strawberry Blond', 'Mitski'], ['F2020', 'Avenue Beat'], ['Cancelled.', 'Kiana Ledé'], ['Motion Sickness', 'Phoebe Bridgers'], ['34+35', 'Ariana Grande'], ['everytime', 'Ariana Grande'], ['Everybody Business', 'Kehlani']]
        self.assertEqual(MusicHistory.compute_top_songs_theory(many_songs), song_theory_data)

    
    """ TESTING REPLY COMPUTE GENRE METHOD
    check that the reply is equal to an expected string using data from my own Spotify
    account and the Spotify Web API 
    
    NOTE: hard-coded data changes less requently, because only calls with 
    "long-term" parameter are used. 
    """
    def test_reply_genre_1(self):
        # uses singular verb and noun 
        expected_reply = "Your top genre is pop. Happy listening!"

        # reply genre call with a limit of 1
        self.assertEqual(MusicHistory.reply_top_genres("long_term", 1), expected_reply)
    
    def test_reply_genre_more(self):
        # verbs and adj are si
        expected_reply = "Your top genres are (1) pop (2) post-teen pop (3) dance pop (4) electropop (5) pop dance (6) canadian pop. Happy listening!"
        
        # reply genre call with a limit greater than 1
        self.assertEqual(MusicHistory.reply_top_genres("long_term", 6), expected_reply)
    

    """ TESTING REPLY COMPUTE TOP SONGS METHOD
    check that the reply is equal to an expected string using data from my own Spotify
    account and the Spotify Web API 
    
    NOTE: hard-coded data changes less requently, because only calls with 
    "long-term" parameter are used.
    """
    def test_reply_song_1(self):
        # uses singular verb and noun 
        expected_reply = "Your top song is 8TEEN by Khalid. Nice bop!"
        
        # reply song call with a limit of 1
        self.assertEqual(MusicHistory.reply_top_songs("long_term", 1), expected_reply)
    
    def test_reply_song_more(self):
        # uses plural verb and noun 
        expected_reply = "Your top songs are (1) 8TEEN by Khalid (2) Pompeii by Jasmine Thompson (3) Capsize by Grace Grundy (4) needy by Ariana Grande (5) Satisfied by Renée Elise Goldsberry (6) Wait for It by Leslie Odom Jr.. Nice bops!"
        
        # reply song call with a limit greater than 1
        self.assertEqual(MusicHistory.reply_top_songs("long_term", 6), expected_reply)
    

    """ TESTING REPLY COMPUTE TOP ARTISTS METHOD
    check that the reply is equal to an expected string using data from my own Spotify
    account and the Spotify Web API 
    
    NOTE: hard-coded data changes less requently, because only calls with 
    "long-term" parameter are used.
    """
    def test_reply_artist_1(self):
        # uses singular verb and noun  
        expected_reply = "Your top artist is Taylor Swift. You have great taste!"

        # reply artist call with a limit of 1
        self.assertEqual(MusicHistory.reply_top_artists("long_term", 1), expected_reply)
    
    def test_reply_artist_more(self):
        # uses plural verb and noun
        expected_reply = "Your top artists are (1) Taylor Swift (2) Ariana Grande (3) Shawn Mendes (4) Ed Sheeran (5) Avril Lavigne (6) Lauv. You have great taste!"
        
        # reply artist call with a limit greater than 1
        self.assertEqual(MusicHistory.reply_top_artists("long_term", 6), expected_reply)
    

    """ TEST REPLY COMPUTE TOP SONG THEORY METHOD
    check that the reply is equal to an expected string using data from my own Spotify
    account and the Spotify Web API 
    
    NOTE: hard-coded data changes less requently, because only calls with 
    "long-term" parameter are used.
    """
    def test_reply_song_theory_1(self):
        # uses singular verb and noun 
        expected_reply = "Your top song has the following music theory features:\n8TEEN Khalid has a tempo of 105.03 BPM!\n8TEEN Khalid has a key of C#/D♭!\n8TEEN Khalid has a time signature of 4 beats per bar!\n8TEEN Khalid is in the Major modality!\n8TEEN Khalid is generally happy, cheerful, euphoric :)\n8TEEN Khalid has high danceability!\n8TEEN Khalid has low acoustics!\n8TEEN Khalid has medium energy!\n8TEEN Khalid has low instrumentals!"
        
        # reply artist call with a limit of 1
        self.assertEqual(MusicHistory.reply_top_songs_theory("long_term", 1), expected_reply)
    
    def test_reply_song_theory_more(self):
        # uses plural verb and noun
        expected_reply = "Your top songs have the following music theory features:\n• mean tempo of 123.76.\n• mean time_signature of 4.0.\n• modal keys of C#/D♭, A, D#/E♭, G.\n• modal modality of major.\n• mean mood of 0.39.\n• mean danceability of 0.61.\n• mean acousticness of 0.71.\n• mean energy of 0.33.\n• mean instrumentalness of 0.0."
        
        # reply artist call with a limit greater than 1
        self.assertEqual(MusicHistory.reply_top_songs_theory("long_term", 4), expected_reply)
    
    #########################
    #### WHITE BOX TESTS ####
    #########################
    """ TESTING COMPUTE GENRE HELPER METHOD
    check that compute genre helper method is returning the correct top genres in the
    right order in each of the 5 different paths 

    NOTE: data is not Spotify user dependent and does not require updating
    """
    def test_compute_genre_helper_empty(self):
        genre_dictionary = {}
        limit = 4
        top_genres = []

        # check path where there are no potential top genres 
        self.assertEqual(MusicHistory.compute_genre_helper(genre_dictionary, limit), top_genres)
    
    def test_compute_genre_helper_tie(self):
        genre_dictionary = {"pop": [1, 3], "r&b": [2,5], "indie": [2,4]}
        limit = 3
        top_genres = ["pop", "indie", "r&b"]
        
        # check path where there is a tie has to be between the ordering top genres
        self.assertEqual(MusicHistory.compute_genre_helper(genre_dictionary, limit), top_genres)
    
    def test_compute_genre_helper_no_tie(self):
        genre_dictionary = {"pop": [1], "r&b": [1,4], "indie": [1, 2, 3]}
        limit = 3
        top_genres = ["indie", "r&b", "pop"]

        # check path where there is a no tie between the ordering top genres
        self.assertEqual(MusicHistory.compute_genre_helper(genre_dictionary, limit), top_genres)
    
    def test_compute_genre_helper_small_limit(self):
        genre_dictionary = {"pop": [1], "r&b": [1,4], "indie": [1, 2, 3]}
        limit = 1
        top_genres = ["indie"]
        
        # check path where only 1 genre will be returned 
        self.assertEqual(MusicHistory.compute_genre_helper(genre_dictionary, limit), top_genres)
    
    def test_compute_genre_helper_small_limit(self):
        genre_dictionary = {"pop": [1], "r&b": [1,4], "indie": [1, 2, 3]}
        limit = 6
        top_genres = ["indie", "r&b", "pop"]
        
        # check path where limit is greater than dictionary of potential genres 
        self.assertEqual(MusicHistory.compute_genre_helper(genre_dictionary, limit), top_genres)

    
    """ TESTING COMPUTE TOP SONG THEORY HELPER
    check that compute top song theory helper method is correcting averaging data
    (mode and mean) in each of the 4 different paths 

    NOTE: data is not Spotify user dependent and does not require updating
    """
    def test_compute_theory_helper_key_tie(self):
        # there is tie between top keys
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
        # there is tie between top modes
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
        # there is a tie in top keys and top modes
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
        # there are no ties in any of the music features
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
    unittest.TextTestRunner(verbosity=2).run(suite) # verbosity 2 is the highest option 
