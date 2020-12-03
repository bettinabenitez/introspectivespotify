import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
scope = "user-read-recently-played, user-top-read, user-read-playback-position, user-read-playback-state, user-modify-playback-state, user-read-currently-playing, playlist-modify-public, user-read-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope, cache_path=".oAuthCache"))

    #####################
    ## Phase One Code ##
    ####################
def audio_features_help(song):
    """
    _audio_features_help will return a JSON object storing all the audio_features listed below.
    This function will interact with the Spotipy Library which interacts with the Spotify  Web API. 
    Using the search function from the Spotify Web Api which returns a JSON object, which can 
    retrieve  track_id from the returned JSON Object which will use the Spotipy Library 
    audio_features(track_id) for the rest of MusicTheory to use. When searching, if there are no
    items in the Spotify Search, aka the items list in the JSON file is empty, it return an empty list.

    Param: String song: The requested song from the user.
    
    Returns:  A JSON Dictionary object with all audio_features.
              An empty list if there are no songs. 

    TDD: No changes were made after running tests as all tests passed initally. 
    """
    # Get the JSON List of results from Spotipy Object
    results = sp.search(q= song, type="track", limit=1)
    
    # Iterate through the results specifically for tracks in items and grab
    # track ID. Call the audio_features function on the track id and return. 
    for  item in results['tracks']['items']:      
        trackID = item['id']
        if trackID != " ":
            audioFeatures = sp.audio_features(trackID)
            return audioFeatures
    return "None"

    #####################
    ## Phase Two Code ##
    ####################

def get_tempo(song):
    """
    get_tempo will return a string representing a value from 0 - 300 BPM of a specified song. 
    This function will call the  helper method audio_features_help(song) to compute a 
    JSON dictionary object to be returned all features, if the call returns "none", then end the 
    process and return "none". Otherwise, , where one can just call JSON_Object[tempo] key to retrieve
    the tempo. Then, the floating point value will be converted into a string for the Music Theory 
    reply methods and Music History methods to use. 

    Param: String song: The requested song from the user.

    Returns: A string representing the tempo (0 - 300 BPM).

    """
    # Get the audio features of a specific song, 
    # key into the tempo and return the tempo.
    audioFeatures = audio_features_help(song)
    if audioFeatures == "None":
        return audioFeatures
    for feature in audioFeatures:
        tempo = feature['tempo']
        return str(tempo)

def get_key(song):
    """
    get_key will return a string reepresenting an integer value of a key using universal pitch class 
    notation, e.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1 
    This function will call the  helper method audio_features_help(song) to compute a 
    JSON dictionary object to be returned all features, if the call returns "none", then end the 
    process and return "none". Otherwise, , where one can just call JSON_Object[tempo] key to retrieve
        the tempo. Then, the floating point value will be converted into a string for the Music Theory 
    reply methods and Music History methods to use. 

    Param: String song: The requested song from the user.

    Returns: A string representing the key ( e.g. 0 = C, 1 = C♯/D♭, 2 = D,
                and so on. If no key was detected, the value is -1).

    """
    # Get the audio features of a specific song, 
    # key into the key and return the tempo.
    audioFeatures = audio_features_help(song)
    if audioFeatures == "None":
        return audioFeatures
    for feature in audioFeatures:
        key = feature['key']
        return str(key)


def get_time_signature(song):
    """
    get_time_signature will return a string representing an integer which is the estimated overall
    time signature of a specified song. This function will call the  helper method 
    audio_features_help(song) to compute a JSON dictionary object to be returned all features, 
    if the call returns "none", then end the process and return "none". Otherwise, , 
    where one can just call JSON_Object[tempo] key to retrieve
    the tempo. Then, the floating point value will be converted into a string for the Music Theory 
    reply methods and Music History methods to use. 

    Param: String song: The requested song from the user.

    Returns: A string representing the time signature. (0-12).
    """
    # Get the audio features of a specific song, 
    # key into the time_sig and return the tempo.
    audioFeatures = audio_features_help(song)
    if audioFeatures == "None":
        return audioFeatures
    for feature in audioFeatures:
        timeSig = feature['time_signature']
        return str(timeSig)


def get_mode(song):
    """
    get_mode will return a string representing an integer of either 0 or 1 to represent the modality
    of the song. Major is represented by 1 and minor is represented by 0.  This function will call the 
    helper method audio_features_help(song) to compute a JSON dictionary object to be 
    returned all features, if the call returns "none", then end the process and return "none". 
    Otherwise, , where one can just call JSON_Object[mode] to retrieve the mode. Then, the 
    floating point value will be converted into a string (representing major or minor) for the 
    Music Theory reply methods and Music History methods to use.

    Param: String song: The requested song from the user.

    Returns: A string representing the mode (1 for Major, 0 for Minor).
    """
    # Get the audio features of a specific song, 
    # key into the mode and return the tempo.
    audioFeatures = audio_features_help(song)
    if audioFeatures == "None":
        return audioFeatures
    for feature in audioFeatures:
        mode = feature['mode']
        return str(mode)


def get_mood(song):
    """
    get_mood will return a string representing the valence of a specified track using a float. 
    Valence is a measure from 0.0 to 1.0, where a high valence is a happy track, while a low valence 
    is a sad track. Anything below 0.5 would be classified as “sad, depressed, angry” while anything 
    above and including 0.5 would be classified as “happy, cheerful, euphoric”. This function will 
    call the helper method audio_features_help(song) to compute a JSON dictionary object to 
    be returned all features, if the call returns "none", then end the process and return "none". 
    Otherwise, , where one can just call JSON_Object[valence] to retrieve the mood.. The, the 
    floating point value will be converted into a string or the Music Theory reply 
    methods and Music History methods to use. 

    Param: String song: The requested song from the user.

    Returns: A string representing the valence from (0.0-1.0)

    TDD: Accidentally had 'mood' as the key when it should be 'valence'
    """
    # Get the audio features of a specific song, 
    # key into the valence and return the tempo.
    audioFeatures = audio_features_help(song)
    if audioFeatures == "None":
        return audioFeatures
    for feature in audioFeatures:
        mood = feature['valence']
        return str(mood)


def get_danceability(song):
    """
    get_ danceability will return a string representing a float value from 0 - 1.0 for 
    danceability for a specified song. Where a value of 0.0 is not danceable while 1.0 
    is very danceable.  This function will call the helper method audio_features_help(song)
    to compute a JSON dictionary object to be returned all features, if the call returns 
    "none", then end the process and return "none". Otherwise, , where one can just call 
    JSON_Object[danceability] to retrieve the danceability.  Then, the floating point 
    value will be converted into a string for the Music Theory reply methods and Music
    History methods to use. 

    Param: String song: The requested song from the user.

    Returns: A string representing the danceability from (0.0 -1.0).

    TDD: Accidentally had 'valance" as the key for the feature dict.
    """
    # Get the audio features of a specific song, 
    # key into the danceability and return the tempo.
    audioFeatures = audio_features_help(song)
    if audioFeatures == "None":
        return audioFeatures
    for feature in audioFeatures:
        dance = feature["danceability"]
        return str(dance)

def get_acousticness(song):
    """
    get_acousticness will return a string representing a float value from 0 - 1.0 for 
    the acoustics of a specified song. Where 0.0 has no acoustics and 1.0 represents 
    high confidence that the track is acoustic. T This function will call the  helper method 
    audio_features_help(song) to compute a JSON dictionary object to be returned all 
    features, if the call returns "none", then end the process and return "none". 
    Otherwise, , where one can just call JSON_Object[acousticness] to retrieve the 
    acousticness. Then, the floating point value will be converted into a string  for 
    the Music Theory reply methods and Music History methods to use. 

    Param: String song: The requested song from the user.

    Returns: A string representing the acoustics from (0.0 - 1.0).

    """
    # Get the audio features of a specific song, 
    # key into the acousticness and return the tempo.
    audioFeatures = audio_features_help(song)
    if audioFeatures == "None":
        return audioFeatures
    for feature in audioFeatures:
        acous = feature['acousticness']
        return str(acous)


def get_energy(song):
    """
    get_energy will return a string representing a float value from 0 - 1.0 of specific 
    energy for the song.  Where 0.0 represents low energy and 1.0 represents max energy. 
    This function will call the  helper method audio_features_help(song) to 
    compute a JSON dictionary object to be returned all features, if the call returns "none", 
    then end the process and return "none". Otherwise,  where one can just call JSON_Object[energy] 
    to retrieve the energy. Then, the floating point value will be converted into a string 
    for the Music Theory reply methods and Music History methods to use.

    Param: String song: The requested song from the user.

    Returns: A string representing the energy from (0.0-1.0)

    """
    # Get the audio features of a specific song, 
    # key into the energy and return the tempo.
    audioFeatures = audio_features_help(song)
    if audioFeatures == "None":
        return audioFeatures
    for feature in audioFeatures:
        energy = feature['energy']
        return str(energy)


def get_instrumentalness(song):
    """
    get_instrumentalness will return a string representing the number of no vocals (Oohs and Aahs) 
    in a specific track from 0.0 to 1.0. If a track has 1.0 value, there is more than likely 
    no vocal content, while tracks closer to 0.0 have high vocal content.  This function will 
    call the  helper method audio_features_help(song) to compute a JSON dictionary object 
    to be returned all features, if the call returns "none", then end the process and return "none". 
    Otherwise, , where one can just call JSON_Object[tempo] to retrieve the instrumentals. 
    Then, the floating point value will be converted into a string for the Music Theory reply 
    methods and Music History methods to use. 

    Param: String song: The requested song from the user.

    Returns: A string representing the Instrumental-ness from (0.0 - 1.0)

    """
    # Get the audio features of a specific song, 
    # key into the instrumentalness and return the tempo.
    audioFeatures = audio_features_help(song)
    if audioFeatures == "None":
        return audioFeatures
    for feature in audioFeatures:
        instrumental = feature['instrumentalness']
        return str(instrumental)

    ######################
    ## Phase Three Code ##
    ######################
    
def reply_get_tempo(song):
    """
    reply_get_tempo will call the get_tempo(song) class which either returns a string or "none", 
    if "none" then return "Sorry! This song does not exist." representing the tempo from 0 - 300 BPM. 
    This method will concatenate a response for the input class which is easy for a bot reply. 
    The string will include the Song name and the correct tempo.

    Param: String song: The requested song from the user.

    Returns: A string that has the value for tempo and formatted English sentences for the input class.

    TDD: Forgot BPM at the end of the reply string.
    """
    # Get the tempo and return as string.
    tempo = get_tempo(song)
    if tempo == "None":
        return "Sorry! This song does not exist."
    else: 
        return song + " has a tempo of" + " " + tempo + " BPM!"

def reply_get_key(song):
    """
    reply_get_key will call the get_key(song) class which either returns a string or "none", if "none" 
    then return "Sorry! This song does not exist." representing the key ( e.g. 0 = C, 1 = C♯/D♭, 2 = D, 
    and so on. If no key was detected, the value is -1). Inside this method, I will convert the numeric 
    value to the musical representation of a key. Such that, if get_key(song) returned 0, then my string
    will reply back with “C”. This method will concatenate a response for the input class which is easy 
    for a bot reply. The string will include the Song name and the correct key. 

    Param: String song: The requested song from the user.

    Returns: A string that has the value for key and formatted English sentences for the input class.  

    TDD: I read online that if statement branches are less efficient than dictionaries, so I changed it!

    """
    # Get the key and convert to correct string format. 
    key = get_key(song)
    key_dict = {"0": "C",
                "1": "C#/D♭",
                "2": "D",
                "3": "D#/E♭",
                "4": "E",
                "5": "F",
                "6": "F#/G♭",
                "7": "G",
                "8": "G#/A♭",
                "9": "A",
                "10": "A#/B♭",
                "11": "B",
                "-1": "Sorry! This song does not exist."}
    return song + " has a key of " + key_dict[key] + "!"

def reply_get_time_signature(song):
    """
    reply_get_time_signature will call the get_time_signature(song) class which either returns a string or "none", 
    if "none" then return "Sorry! This song does not exist." representing the time signature. This method will 
    concatenate a response for the input class which is easy for a bot reply. The string will include the Song 
    name and the correct time signature value.

    Param: String song: The requested song from the user.

    Returns: A string that has the value for the time signature and formatted English sentences for the input class.

    TDD: Forgot to change variable name to "timeSig" from tempo.
    """
    # Get the time sig and convert. 
    timeSig = get_time_signature(song)
    if timeSig == "None":
        return "Sorry! This song does not exist."
    else: 
        return song + " has a time signature of" + " " + timeSig + " beats per bar!"

def reply_get_mode(song):
    """
    reply_get_mode will call the get_mode(song) class which returns a  string representing the mode 
    (1 for Major, 0 for Minor). Inside this method, I will convert the numeric representation of mode 
    to the musical representation (either major or minor). This method will concatenate a response for 
    the input class which is easy for a bot reply. The string will include the Song name and the correct mode. 

    Param: String song: The requested song from the user.

    Returns: A string that has the value for the mode and formatted English sentences for the input class.

    """
    # Get the mode and convert, and reply. 
    mode = get_mode(song)
    if mode == "None":
        return "Sorry! This song does not exist."
    elif mode == "1": 
        return song + " is in the Major modality!"
    else:
        return song + " is in the Minor modality!"

def reply_get_mood(song):
    """
    reply_get_mood will call the get_mood(song) class which either returns a string or "none", if "none" 
    then return "Sorry! This song does not exist." representing the valence as numeric representation.
    I will create conditionals which check if anything below 0.5 would be classified as “sad, depressed, angry” 
    while anything above and including 0.5 would be classified as “happy, cheerful, euphoric”. 
    This method will concatenate a response for the input class which is easy for a bot reply. 
    The string will include the Song name and the correct mood of either “sad, depressed, angry” or 
    “happy, cheerful euphoric”. 

    Param: String song: The requested song from the user.

    Returns: A string that has the value for the mood and formatted English sentences for the input class.

    """
    # Change into a float to compare values, set correct string for
    # specific value.
    mood = get_mood(song)
    if mood == "None":
        return "Sorry! This song does not exist."
    elif float(mood) >= 0.0 and float(mood) < 0.5: 
        return song + " is generally sad, depressed, or angry :("
    else:
        return song + " is generally happy, cheerful, euphoric :)"

def reply_get_danceability(song):
    """
    reply_get_danceability will call the get_danceability(song) class which either returns a string or "none",
    if "none" then return "Sorry! This song does not exist." representing the danceability from 0.0 to 1.0. 
    Inside this method, I will convert the values to a more musical representation. Anything from 0.0 - 0.4 
    would be “Low”, 0.4 -0.6 would be “Medium” and 0.6-1.0 would be “High”.  This method will concatenate a 
    response for the input class which is easy for a bot reply. The string will include the Song name and 
    the correct danceability. 

    Param: String song: The requested song from the user.

    Returns: A string that has the value for the danceability and formatted English sentences for the input class.
    """
    # Change into a float to compare values, set correct string for
    # specific value.
    dance = get_danceability(song)
    if dance == "None":
        return "Sorry! This song does not exist."
    elif float(dance) >= 0.0 and float(dance) < 0.4: 
        return song + " has low danceability!"
    elif float(dance) >= 0.4 and float(dance) < 0.6: 
        return song + " has medium danceability!"
    else:
        return song + " has high danceability!"

def reply_get_acousticness(song):
    """
    reply_get_acousticness will call the get_acousticness(song) class which returns a  string representing the 
    acoustics from 0.0 to 1.0 Inside this method, I will convert the values to a more musical representation. 
    Anything from 0.0 - 0.4 would be “Low”, 0.4 -0.6 would be “Medium” and 0.6-1.0 would be “High”. 
    This method will concatenate a response for the input class which is easy for a bot reply. 
    The string will include the Song name and the correct acoustics. 

    Param: String song: The requested song from the user.

    Returns: A string that has the value for the acoustics and formatted English sentences for the input class.

    """
    # Change into a float to compare values, set correct string for
    # specific value.
    acoustics = get_acousticness(song)
    if acoustics == "None":
        return "Sorry! This song does not exist."
    elif float(acoustics) >= 0.0 and float(acoustics) < 0.4: 
        return song + " has low acoustics!"
    elif float(acoustics) >= 0.4 and float(acoustics) < 0.6: 
        return song + " has medium acoustics!"
    else:
        return song + " has high acoustics!"

def reply_get_energy(song):
    """
    reply_get_energy will call the get_energy(song) class which either returns a string or "none", if "none" then 
    return "Sorry! This song does not exist." representing the energy from 0.0-1.0. Inside this method, 
    I will convert the values to a more musical representation. Anything from 0.0 - 0.4 would be “Low”, 
    0.4 -0.6 would be “Medium” and 0.6-1.0 would be “High”. This method will concatenate a response for 
    the input class which is easy for a bot reply. The string will include the Song name and the correct energy.

    Param: String song: The requested song from the user.

    Returns: A string that has the value for the energy and formatted English sentences for the input class. 
    """
    # Change into a float to compare values, set correct string for
    # specific value.
    energy = get_energy(song)
    if energy == "None":
        return "Sorry! This song does not exist."
    elif float(energy) >= 0.0 and float(energy) < 0.4: 
        return song + " has low energy!"
    elif float(energy) >= 0.4 and float(energy) < 0.6: 
        return song + " has medium energy!"
    else:
        return song + " has high energy!"

def reply_get_instrumentalness(song):
    """
    reply_get_instrumentalness will call the get_instrumentalness(song) class which either returns a string or "none",
    if "none" then return "Sorry! This song does not exist." representing the Instrumentalness from 0.0-1.0. 
    Inside this method, I will convert the values to a more musical representation. Anything from 0.0 - 0.4 
    would be “Low”, 0.4 -0.6 would be “Medium” and 0.6-1.0 would be “High”. This method will concatenate a 
    response for the input class which is easy for a bot reply. The string will include the Song name and 
    the correct instrumentalness. 

    Param: String song: The requested song from the user.

    Returns: A string that has the value for the instrumentalness and formatted English sentences for the input class.
    
    TDD: Accidentally did not change the variable from energy to instrumentals
    """
    # Change into a float to compare values, set correct string for
    # specific value.
    instrumentals = get_instrumentalness(song)
    if instrumentals == "None":
        return "Sorry! This song does not exist."
    elif float(instrumentals) >= 0.0 and float(instrumentals) < 0.4: 
        return song + " has low instrumentals!"
    elif float(instrumentals) >= 0.4 and float(instrumentals) < 0.6: 
        return song + " has medium instrumentals!"
    else:
        return song + " has high instrumentals!"

def reply_all_music_theory(song):
    """
     reply_all_music_theory will call the helper which holds a 
     JSON object representing all of the audio_features from the Spotipy library. 
     Using a for: each loop to parse through the object, the method will create a 
     reply containing all of the audio_features to return back to the calling input class. 

    Param: String song: The requested song from the user.   

    Returns: A string that has the value for the instrumentalness and formatted English sentences for the input class.

    TDD: I had deleted the get_all_musictheory(song) method due to it being not needed and forgotten to change 
        the method here to call audio_features_help instead!
    """
    # Grab the total theory for a song, call each getter 
    # and format the string properly. 
    allTheory = audio_features_help(song)
    if allTheory == "None":
        return "Sorry! This song does not exist."
    else: 
        return (reply_get_tempo(song) + "\n" + reply_get_key(song) + "\n" + reply_get_time_signature(song) + "\n" +
        reply_get_mode(song) + "\n" + reply_get_mood(song) + "\n" + reply_get_danceability(song) + "\n" + reply_get_acousticness(song) + "\n" +
        reply_get_energy(song) + "\n" + reply_get_instrumentalness(song))
    
    ######################
    ## Phase Four Code  ##
    ######################

def compare_theory(song, song_compare):
    """
    This method will use the helper function, audio_features_help to compare for similarities with another song, song_compare. 
    By using the help method, I will create two calls to the helper function for both song and song_compare and store them in 
    different variables within the method. Then, by looping through both objects, I will look for values that are either equal 
    or +/- 0.1  off from their initial floating values. If the values are similar, I will store that into a list with all the 
    correlating audio_features between the songs for the reply_compare_theory(self, song, song_compare) to use. If there are no 
    audio features that are similar, I will return an empty list for the reply method to use as well. 

    Param: String song: One of the requested songs from the user. 
    Param: String song_comapre: The other song to compare with Param song. 

    Returns: A list with all audio_features that are similar between song and song_compare. 

    TDD: I realized that mode will always have a difference that puts it in similarities, despite 
         if it is different, so I added it as it's own branch of comparision too. 
    """
    # Get the audio features of the specific song, grab the dictionary.
    similaritiesList = []
    songA_features = audio_features_help(song)[0]
    songB_features = audio_features_help(song_compare)[0]

    if songA_features == "None" or songB_features == "None":
        return similaritiesList
    # Iterate through each key in both dicts, if one of the keys are something I'm not looking for, continue. 
    # Otherwise, compare values if they are +/- 0.1. For some, compare +/- 1. 
    # append to list and return.
    for (featureA,valueA), (featureB,valueB) in zip(songA_features.items(), songB_features.items()):
        if (featureA == "loudness" or featureA == "speechiness" or featureA == "liveness" or featureA == "type"
        or featureA == "id" or featureA == "uri" or featureA == "track_href" or featureA == "analysis_url" or
        featureA == "duration_ms"):
            continue
        else:
            # If feature is tempo, only offest by one.
            if featureA == "tempo":
                if valueA - 1 <= valueB <= valueA + 1:
                    similaritiesList.append(featureA)
            # If the feature is mode, make sure they are equal.
            elif featureA == "mode":
                if valueA == valueB:
                    similaritiesList.append(featureA)
            # If the feature is instru. , make sure its offset by 0.01
            elif featureA == "instrumentalness":
                if valueA - 0.01 <= valueB <= valueA + 0.01:
                    similaritiesList.append(featureA)
            # Normal Offeset.
            elif valueA - 0.1 <= valueB <= valueA + 0.1:
                    similaritiesList.append(featureA)  
    return similaritiesList

def reply_compare_theory(song, song_compare):
    """
    reply_compare_theory(song, song_compare) will call compare_theory(song, song_compare) to compute the similarities between two 
    songs and store it into a new list which holds the similar audio_features. If the returned list is empty, that means that there 
    were no computed similarities and the method will return a string containing  “Sorry! There were no similarities between these 
    songs.”. If the returned list has values, then it will return a string which contains all of the similar audio features and the 
    two songs as well for easy readability. 

    Param: String song: One of the requested songs from the user. 
    Param: String song_comapre: The other song to compare with Param song. 

    Returns: A string that either reads “Sorry! There were no similarities between these songs.” if the returned list from 
             compare_theory(song, song_compare) was empty or a string that contains all the similar audio_features between 
             two songs for the InputClass to use.
    
    TDD: I did have some extra spaces due to my string concatention issue to which I fixed. I also did not realize that 
         time signature will usually AWLAYS match, so I changed my testing songs to ensure I get 2 100% different songs. 
    """
    # Check if the returned list is empty, as no similartiies. 
    # Otherwise, iterate through list and append to return string. 
    similaritiesList = compare_theory(song,song_compare)
    similaritiesString = song + " and " + song_compare + " are similar in: \n"
    if similaritiesList == []:
        return "Sorry! There were no similarties between these songs."
    else:
        for feature in similaritiesList:
            if feature == "valence":
                similaritiesString += "mood\n"
            elif feature == "time_signature":
                similaritiesString += "time signature\n" 
            else:
                similaritiesString +=  feature + "\n"
    return similaritiesString

    ######################
    ## Phase Five Code  ##
    ######################

def suggest_theory(song_a, song_b):
    """
    This method will call for song_a and song_b spotify search for the specific artist ID, where it will grab the top genres for both 
    artist_a and artist_b. Then, for song_a and song_b it will call the audio_features_help and grab the track ID for song_b. It will
    compare the audio features of valence, danceability, tempo, and energy to fill in the filters of max and min for the different features
    in the Spotify GET suggestions based on seeds. There, I will search for at most 5 songs based on similar artist from artist_a, similar 
    track from song_b and the two top genres from both artist_a and artist_b. If there are songs, it will return the track ids in a list. If
    there are no songs, or the search failed, it will return an empty list. 
    
    Param: String song_a: One of the requested songs from the user. 
    Param: String song_b: The other song to compare with Param song. 
    
    Returns: A list with up to 5 track_ids if there are matches OR an empty list if things fail or there are no suggestions.
    """
    # Grab the search results for each song, set the artists to "none" at the moment. 
    # Grab the artist_id for both songs, if search fails, return empty list. 
    # Otherwise, grab the audio_features and track_id and genres for each song
    songAResults = sp.search(q= song_a, type="track", limit=1)
    songBResults = sp.search(q= song_b, type="track", limit=1)
    artist_a = "None"
    artist_b = "None"
    track_list = []

    for song in songAResults['tracks']['items']:
        if song != " ":
            artist_a = song['artists'][0]['id']
    for song in songBResults['tracks']['items']:
        if song != " ":   
            artist_b = song['artists'][0]['id']
    # If no artist exists for the specific song.
    if artist_a == "None" or artist_b == "None":
        return track_list 
    else:
        # Get the audio features, track id, and genre list.
        songAFeatures = audio_features_help(song_a)[0]
        songBFeatures = audio_features_help(song_b)[0]
        track_id_A = songAFeatures["id"]
        track_id_B = songBFeatures["id"]

        genre_a = sp.artist(artist_a)['genres']
        genre_b = sp.artist(artist_b)['genres']
        # Check if the genre list is empty. Some artists don't have genres 
        # and cause a fail if they do not. Do not run search if both
        # artists do not have a genre.
        if (genre_b == [] and genre_a == []):
            return []
        elif genre_a == []:
            combined_genres = genre_b[0]
        elif genre_b == []:
            combined_genres = genre_a[0]
        else:
            combined_genres = genre_a[0] + " "  + genre_b[0]

        # Find the max and min for each audio_feature for the search. 
        max_valence = max(float(get_mood(song_a)), float(get_mood(song_b)))
        min_valence = min(float(get_mood(song_a)), float(get_mood(song_b)))
        max_energy = max(float(get_energy(song_a)), float(get_energy(song_b)))
        min_energy = min(float(get_energy(song_a)), float(get_energy(song_b)))
        max_tempo = max(float(get_tempo(song_a)), float((get_tempo(song_b))))
        min_tempo = min(float(get_tempo(song_a)), float((get_tempo(song_b))))
        max_dance = max(float(get_danceability(song_a)), float(get_danceability(song_b)))
        min_dance = min(float(get_danceability(song_a)), float(get_danceability(song_b)))

        # Spotify search call for GET_RECOMENDATIONS_BY_SEED 
        recomendations = sp.recommendations(seed_artists = [artist_a, artist_b], seed_genres = [combined_genres],
        seed_tracks = [track_id_A, track_id_B], limit = 5, country = 'US',
        min_valence = min_valence,
        max_valence = max_valence,
        min_energy = min_energy,
        max_energy = max_energy,
        min_tempo = min_tempo,
        max_tempo = max_tempo,
        min_danceability = min_dance,
        max_danceability = max_dance)

        # Iterate through the results, store the new song tracks and artists_ids into a list.
        # if the suggested song is the same as the requested song, remove it. 
        for item in recomendations['tracks']:
            artist_id = item['artists'][0]['id']
            track_id = item['id']
            if track_id == track_id_A or track_id == track_id_B:
                continue
            else:
                track_list.append([artist_id, track_id])
        if len(recomendations) == 0: 
            return []
        else:
            return track_list
        
def reply_suggest_theory(song_a, song_b):
    """
    This method will call suggest_theory(song_a, song_b) to grab a list with similar track_ids (up to 5). If there is an empty list
    return the ending string that lets the user know there are no similartiies. If there are, it will go through each track_id and 
    get the artist name and format a reply to list each song and it's artist for the user to read easily and for the input class.

    Param: String song_a: One of the requested songs from the user. 
    Param: String song_b: The other song to compare with Param song. 

    Returns: A string that either reads “Sorry! There were no suggestions between these songs.” if the returned list from 
             suggest_theory(song_a, song_b) was empty or a string that contains all the similar songs between 
             two songs for the InputClass to use.
    """
    # Grab the track_list of suggested songs, set up the return string. 
    # For each element in the track_list, enumerate it and grab the track name 
    # and track artist for the return string. If the track list is empty, 
    # return the no suggestions string. 
    track_list = suggest_theory(song_a, song_b)
    reply_string = ("I computed these songs that are similar to " + song_a + " and " + song_b + ": \n")

    if track_list == []:
        return "Sorry! There are no suggested songs based on theory from these songs!"
    else:
        for idx, item in enumerate(track_list):
            rep = (str(idx + 1) + ". " + sp.track(item[1])['name'] + " by " + sp.artist(item[0])['name'] + "\n")
            reply_string += rep

    return reply_string
