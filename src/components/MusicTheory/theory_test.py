import unittest 
import MusicTheory

class MusicTheoryTest(unittest.TestCase):
    #####################
    ## Phase One Tests ##
    ####################

    # Changed the hardCodedAF object after coding due to my own
    # forgetfullness of the brackets surrounding the object!
    # TESTS PASSED ON 20th Nov, 2020
    def test_audio_features_json(self):
        hardCodedAF = [{
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
        }]
        self.assertEqual(MusicTheory.audio_features_help("Thank You For The Music"), hardCodedAF)

    # Changed the type of assert as I wrote the wrong one! Otherwise all my tests passed.
    # TESTS PASSED ON 20th Nov, 2020
    def test_audio_features_error(self):
        errorMessage = "Sorry! That track does not exist"
        self.assertEqual(MusicTheory.audio_features_help("Foo Bar Bash Bops"), errorMessage)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MusicTheoryTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
