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
    # Tests that a JSON Dictionary is created with call. 
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
    # Tests that a song that does not live in the SP library fails.
    def test_audio_features_error(self):
        errorMessage = "None"
        self.assertEqual(MusicTheory.audio_features_help("Foo Bar Bash Bops"), errorMessage)

    #####################
    ## Phase Two Tests ##
    #####################
    # TESTS PASSED ON 20th Nov, 2020


    # Tests the tempo call.
    def test_get_tempo(self):
        hardcodedTempo = "98.879"
        self.assertEqual(MusicTheory.get_tempo("Thank You For The Music"), hardcodedTempo)
    
    # Tests the key call.
    def test_get_key(self):
        hardcodedKey = "4"
        self.assertEqual(MusicTheory.get_key("Thank You For The Music"), hardcodedKey)

    # Tests the time signature call.
    def test_get_time_signature(self):
        hardcodedTS = "4"
        self.assertEqual(MusicTheory.get_time_signature("Thank You For The Music"), hardcodedTS)

    # Tests the modality call. 
    def test_get_mode(self):
        hardcodedMode = "1"
        self.assertEqual(MusicTheory.get_mode("Thank You For The Music"), hardcodedMode)

    # Tests the mood call.
    def test_get_mood(self):
        hardcodedMood = "0.479"
        self.assertEqual(MusicTheory.get_mood("Thank You For The Music"), hardcodedMood)

    # Tests the danceability call.
    def test_get_danceability(self):
        hardcodedDance = "0.527"
        self.assertEqual(MusicTheory.get_danceability("Thank You For The Music"), hardcodedDance)

    # Tests the acousticness. 
    def test_get_acousticness(self):
        hardcodedAcous = "0.932"
        self.assertEqual(MusicTheory.get_acousticness("Thank You For The Music"), hardcodedAcous) 

    # Tests the energy call.
    def test_get_energy(self):
        hardcodedEnergy = "0.134"
        self.assertEqual(MusicTheory.get_energy("Thank You For The Music"), hardcodedEnergy) 

    # Tests the instrumentalness call.
    def test_get_instrumentalness(self):
        hardcodedInstru = "0"
        self.assertEqual(MusicTheory.get_instrumentalness("Thank You For The Music"), hardcodedInstru)

    #######################
    ## Phase Three Tests ##
    #######################
    # ALL TESTS PASSED 21st of NOVEMBER 2020

    # Tests the tempo reply string.
    def test_reply_tempo(self):
        hardcodedTempo = "Thank You For The Music has a tempo of 98.879 BPM!"
        self.assertEqual(MusicTheory.reply_get_tempo("Thank You For The Music"), hardcodedTempo)

    # Tests the key reply string. 
    def test_reply_key(self):
        hardcodedKey = "Thank You For The Music has a key of E!"
        self.assertEqual(MusicTheory.reply_get_key("Thank You For The Music"), hardcodedKey)

    # Tests the time_sig reply string.
    def test_reply_time_signature(self):
        hardcodedTS = "Thank You For The Music has a time signature of 4 beats per bar!"
        self.assertEqual(MusicTheory.reply_get_time_signature("Thank You For The Music"), hardcodedTS)

    # Tests the mode reply string.
    def test_reply_mode(self):
        hardcodedMode = "Thank You For The Music is in the Major modality!"
        self.assertEqual(MusicTheory.reply_get_mode("Thank You For The Music"), hardcodedMode)

    # Tests the get mood reply string.
    def test_reply_mood(self):
        hardcodedMood = "Thank You For The Music is generally sad, depressed, or angry :("
        self.assertEqual(MusicTheory.reply_get_mood("Thank You For The Music"), hardcodedMood)

    # Tests the danceability reply string.
    def test_reply_danceability(self):
        hardcodedDance = "Thank You For The Music has medium danceability!"
        self.assertEqual(MusicTheory.reply_get_danceability("Thank You For The Music"), hardcodedDance)

    # Tests the acoustics reply string.
    def test_reply_acousticness(self):
        hardcodedAcous = "Thank You For The Music has high acoustics!"
        self.assertEqual(MusicTheory.reply_get_acousticness("Thank You For The Music"), hardcodedAcous) 

    # Tests the energy reply string. 
    def test_reply_energy(self):
        hardcodedEnergy = "Thank You For The Music has low energy!"
        self.assertEqual(MusicTheory.reply_get_energy("Thank You For The Music"), hardcodedEnergy) 

    # Tests the instrumentalness reply string. 
    def test_reply_instrumentalness(self):
        hardcodedInstru = "Thank You For The Music has low instrumentals!"
        self.assertEqual(MusicTheory.reply_get_instrumentalness("Thank You For The Music"), hardcodedInstru)
    
    # Changed test strings due to inconsistency with original plan, my mistake.
    # added extra underscore in method name and had extra spaces due to \N. 
    # forgot the ! at the end of BPM too :)
    # Tests the reply all string.
    def test_reply_all_musictheory(self):
        hardcodedDict = ("Thank You For The Music has a tempo of 98.879 BPM!\n" 
                         "Thank You For The Music has a key of E!\n" 
                         "Thank You For The Music has a time signature of 4 beats per bar!\n"
                         "Thank You For The Music is in the Major modality!\n"
                         "Thank You For The Music is generally sad, depressed, or angry :(\n"
                         "Thank You For The Music has medium danceability!\n"
                         "Thank You For The Music has high acoustics!\n"
                         "Thank You For The Music has low energy!\n"
                         "Thank You For The Music has low instrumentals!")
        self.assertEqual(MusicTheory.reply_all_music)theory("Thank You For The Music"), hardcodedDict)

    ## Key Tests: Each test here tests that each reply key branch is correct. ##

    # Original song was not in the key of C, Google Lied ;(
    def test_reply_key_C(self):
        self.assertEqual(MusicTheory.reply_get_key("Chained To The Rhythm"), "Chained To The Rhythm has a key of C!")

    # Original song was not in the key of C#, Google Lied ;(
    # Same for second song
    def test_reply_key_CS(self):
        self.assertEqual(MusicTheory.reply_get_key("Bounce Back"), "Bounce Back has a key of C#/D♭!")

    def test_reply_key_D(self):
        self.assertEqual(MusicTheory.reply_get_key("Love Story"), "Love Story has a key of D!")

    # Original song was not in the key of D#, Google Lied ;(
    # Same with second song...
    def test_reply_key_DS(self):
        self.assertEqual(MusicTheory.reply_get_key("Harajuku Girls"), "Harajuku Girls has a key of D#/E♭!")

    # Original song was not in the key of E, Google Lied ;(
    def test_reply_key_E(self):
        self.assertEqual(MusicTheory.reply_get_key("Happy Now"), "Happy Now has a key of E!")

    def test_reply_key_F(self):
        self.assertEqual(MusicTheory.reply_get_key("This Is America"), "This Is America has a key of F!")

    def test_reply_key_FS(self):
        self.assertEqual(MusicTheory.reply_get_key("Lucid Dreams"), "Lucid Dreams has a key of F#/G♭!")

    # Original song was not in the key of G, Google Lied ;(
    def test_reply_key_G(self):
        self.assertEqual(MusicTheory.reply_get_key("Still Got Time"), "Still Got Time has a key of G!")

    def test_reply_key_GS(self):
        self.assertEqual(MusicTheory.reply_get_key("Don't Cry"), "Don't Cry has a key of G#/A♭!")

    def test_reply_key_A(self):
        self.assertEqual(MusicTheory.reply_get_key("No Tears Left To Cry"), "No Tears Left To Cry has a key of A!")

    # Original song was not in the key of C#, Google Lied ;(
    def test_reply_key_AS(self):
        self.assertEqual(MusicTheory.reply_get_key("Hollaback Girl"), "Hollaback Girl has a key of A#/B♭!")

    # Forgot exclamation point at the end of test also mispelled Pijama. 
    def test_reply_key_B(self):
        self.assertEqual(MusicTheory.reply_get_key("Sin Pijama"), "Sin Pijama has a key of B!")
    
# Mode Tests: Tests each branch of the reply method executes. 
    def test_get_mode_0(self):
        self.assertEqual(MusicTheory.reply_get_mode("LIKE I WOULD"), "LIKE I WOULD is in the Minor modality!")
    
    def test_get_mode_1(self):
        self.assertEqual(MusicTheory.reply_get_mode("Someone Like You"), "Someone Like You is in the Major modality!")

# Mood Tests:  Tests each branch of the reply method executes. 
    def test_get_mood_H(self):
        self.assertEqual(MusicTheory.reply_get_mood("Cut To The Feeling"), "Cut To The Feeling is generally happy, cheerful, euphoric :)")

    def test_get_mood_L(self):
        self.assertEqual(MusicTheory.reply_get_mood("If I Could Fly"), "If I Could Fly is generally sad, depressed, or angry :(")

# Danceability Tests: Tests each branch of the reply method executes. 
# All of these tests had the wrong information- I was looking at the wrong audio_feature! Oops.
    def test_get_dance_M(self):
        self.assertEqual(MusicTheory.reply_get_danceability("Dusk Till Dawn"), "Dusk Till Dawn has low danceability!")

    def test_get_dance_L(self):
        self.assertEqual(MusicTheory.reply_get_danceability("Mamma Mia"), "Mamma Mia has high danceability!")

    def test_get_dance_H(self):
        self.assertEqual(MusicTheory.reply_get_danceability("Honey, Honey"), "Honey, Honey has medium danceability!")

# Acoustics Tests: Tests each branch of the reply method executes. 
    def test_get_acoust_H(self):
        self.assertEqual(MusicTheory.reply_get_acousticness("Night Changes"), "Night Changes has high acoustics!")

    def test_get_acoust_L(self):
        self.assertEqual(MusicTheory.reply_get_acousticness("Sunflower"), "Sunflower has medium acoustics!!")

    def test_get_acoust_L(self):
        self.assertEqual(MusicTheory.reply_get_acousticness("Honey, Honey"), "Honey, Honey has low acoustics!")

# Energy Tests: Tests each branch of the reply method executes.
    def test_get_energy_H(self):
        self.assertEqual(MusicTheory.reply_get_energy("Nice To Meet Ya"), "Nice To Meet Ya has high energy!")

    def test_get_energy_L(self):
        self.assertEqual(MusicTheory.reply_get_energy("Goodnight N Go"), "Goodnight N Go has medium energy!!")
    
    # Picked the incorrect song. 
    def test_get_energy_L(self):
        self.assertEqual(MusicTheory.reply_get_energy("Intermission:Flower"), "Intermission:Flower has low energy!")

# Instrumental Tests: Tests each branch of the reply method executes. 
    def test_get_instrumental_H(self):
        self.assertEqual(MusicTheory.reply_get_instrumentalness("King Kunta"), "King Kunta has low instrumentals!")

    # Had the wrong song harcoded!
    def test_get_instrumental_M(self):
        self.assertEqual(MusicTheory.reply_get_instrumentalness("I'm Closing My Eye"), "I'm Closing My Eye has medium instrumentals!")
    # Had the wrong song harcoded!
    def test_get_instrumental_L(self):
        self.assertEqual(MusicTheory.reply_get_instrumentalness("Swan Lake"), "Swan Lake has high instrumentals!")

    #######################
    ## Phase Four Tests  ##
    #######################
    # ALL TESTS PASSED 22nd OF NOVEMBER 2020
    # I got rid of my second whitebox test for compare_theory as my first blackbox test technically checks the successful branch.
    # With testing, I realized I had formatted the way the similar methods are shown in the wrong way so I 
    # fixed that up. I also had spelling mistakes and some spacing errors. 

    # Tests the functionality of compare_theory with a hardcoded reply and a successful running branch. 
    def test_compare_theory_functionality(self):
        self.assertEqual(MusicTheory.reply_compare_theory("POV", "POV"),("POV and POV are similar in: \n"
        "danceability\n"
        "energy\n"
        "key\n"
        "mode\n"
        "acousticness\n"
        "instrumentalness\n"
        "mood\n"
        "tempo\n"
        "time signature\n"))

    # Tests the error branch with an incorrect songs that have no similarities. 
    def test_compare_theory_nomatch(self):
        self.assertEqual(MusicTheory.reply_compare_theory("Far More Blue", "THAT BITCH"),("Sorry! There were no similarties between these songs."))

    #######################
    ## Phase Five Tests  ##
    #######################
    # I found it way too hard to get a playlist and sort through a playlist due to my own miscomception of what a GET SEED SUGGESTION 
    # did, so therefore I changed it back to two songs and compare + find songs thru that. 

    # Forgot to make the method called be reply_suggest_theory! Name two tests the same thing too, also had parenthesis issues.
    # Added a newline cmnd after the 1. 1980s Horror film as I decided to have newlines at the end of each line. Also for my POV POV test
    # I still had the "Computed" line at the end....oops.
    # On 25th November, I changed my key method to a dictionary and noticed music_one failed due to 
    # a new hardcoded suggestion. So I changed how my test works as Spotify Suggest is never 100% the same EVER.
    
    # TESTS PASSED 24th of November 2020 :) 
    
    # Tests a functionality that these two songs will ALWAYS produce this song for ensuring format is correct.
    # also tests succesful branch.
    def test_suggest_music_one(self):
        headerString = "I computed these songs that are similar to FROOT and Summertime Sadness: \n"
        self.assertTrue(headerString in MusicTheory.reply_suggest_theory("FROOT", "Summertime Sadness"))

    # Tests two songs that have no similarities will produce no suggestions, also tests failure branch.
    def test_suggest_music_two(self):
        self.assertEqual(MusicTheory.reply_suggest_theory("Foo Bar Bash Song", "Sheila Ki Jiwani"), "Sorry! There are no suggested songs based on theory from these songs!")

    # Tests that a song cannot suggest itself, also tests the failure branch. 
    def test_suggest_music_three(self):
        self.assertEqual(MusicTheory.reply_suggest_theory("POV", "POV"),("Sorry! There are no suggested songs based on theory from these songs!"))

    # Tests two songs not in the Spotify Library fails.
    def test_suggest_music_four(self):
        self.assertEqual(MusicTheory.reply_suggest_theory("Foo Bar Bash Song", "I am in Art Class"), "Sorry! There are no suggested songs based on theory from these songs!")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MusicTheoryTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
