import unittest 

class TestStringMethods(unittest.TestCase):

    def audio_features_json(self)
            hardCodedAF = {
                            "danceability": 0.527,
                            "energy": 0.134,
                            "key": 4,
                            "loudness": -11.264,
                            "mode": 1,
                            "speechiness": 0.0348,
                            "acousticness": 0.932,
                            "instrumentalness": 0,
                            "liveness": 0.103,
                            "valence": 0.479,
                            "tempo": 98.879,
                            "type": "audio_features",
                            "id": "64yJ0tpcSveze3KJAdZGKe",
                            "uri": "spotify:track:64yJ0tpcSveze3KJAdZGKe",
                            "track_href": "https://api.spotify.com/v1/tracks/64yJ0tpcSveze3KJAdZGKe",
                            "analysis_url": "https://api.spotify.com/v1/audio-analysis/64yJ0tpcSveze3KJAdZGKe",
                            "duration_ms": 224107,
                            "time_signature": 4
                            }
        self.assertEqual(MusicTheory.__audio_features_help("Thank You For The Music"), hardCodedAF)

    def audio_features_error(self):
        # Q! , so if there is nothing in here, it'll just have an 
        # empty list. So how do I instead tell this inner private method 
        # to just talk right back to the input class and say hey there is 
        # nothing here and print this error instead of going back to my getter
        # then back to the reply and back to Input !!! 
        errorMessage = "Sorry! That track does not exist"
        self.assertFalse(MusicTheory.__audio_features_help("Foo Bar Bash Bops"), errorMessage)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
    unittest.TextTestRunner(verbosity=2).run(suite)
