import unittest 
import MusicTheory

class MusicTheoryTest(unittest.TestCase):
    #####################
    ## Phase One Tests ##
    ####################
    # These tests are testing the blackbox and whitebox functionality 
    # of the inner method, audio_features_help in which every method
    # depends on. It checks to make sure that a correct JSON object 
    # is created and an error message is returned if there is no 
    # song in the library. 

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
        errorMessage = "None"
        self.assertEqual(MusicTheory.audio_features_help("Foo Bar Bash Bops"), errorMessage)

    #####################
    ## Phase Two Tests ##
    #####################
    def test_get_tempo(self):
        hardcodedTempo = "98.879"
        self.assertEqual(MusicTheory.get_tempo("Thank You For The Music", hardcodedTempo)) 
    
    def test_get_key(self):
        hardcodedKey = "4"
        self.assertEqual(MusicTheory.get_key("Thank You For The Music", hardcodedKey))

    def test_get_time_signature(self):
        hardcodedTS = "4"
        self.assertEqual(MusicTheory.get_time_signature("Thank You For The Music", hardcodedTS))

    def test_get_mode(self):
        hardcodedMode = "1"
        self.assertEqual(MusicTheory.get_mode("Thank You For The Music", hardcodedMode))  

    def test_get_mood(self):
        hardcodedMood = "0.479"
        self.assertEqual(MusicTheory.get_mood("Thank You For The Music", hardcodedMood)) 

    def test_get_danceability(self):
        hardcodedDance = "0.527"
        self.assertEqual(MusicTheory.get_danceability("Thank You For The Music", hardcodedDance)) 

    def test_get_acousticness(self):
        hardcodedAcous = "0.932"
        self.assertEqual(MusicTheory.get_acousticness("Thank You For The Music", hardcodedAcous)) 

    def test_get_energy(self):
        hardcodedEnergy = "0.134"
        self.assertEqual(MusicTheory.get_energy("Thank You For The Music", hardcodedEnergy)) 

    def test_get_instrumentalness(self):
        hardcodedInstru = "0"
        self.assertEqual(MusicTheory.get_instrumentalness("Thank You For The Music", hardcodedInstru))
    
    def test_get_all_musictheory(self):
        hardcodedDict = [{
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
        self.assertEqual(MusicTheory.get_all_music_theory("Thank You For The Music"), hardCodedDict)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MusicTheoryTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
