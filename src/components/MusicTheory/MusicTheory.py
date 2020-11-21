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
    results = sp.search(q= song, type="track", limit=1)
    
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
    audioFeatures = audio_features_help(song)
    if audioFeatures == "None":
        return audioFeatures
    for feature in audioFeatures:
        dance = feature["danceability"]
        return str(dance)

#print(get_danceability("Thank you for the music"))

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
    audioFeatures = audio_features_help(song)
    if audioFeatures == "None":
        return audioFeatures
    for feature in audioFeatures:
        instrumental = feature['instrumentalness']
        return str(instrumental)
        
def reply_get_tempo(song):
    """
    reply_get_tempo will call the get_tempo(song) class which either returns a string or "none", 
    if "none" then return "Sorry! This song does not exist." representing the tempo from 0 - 300 BPM. 
    This method will concatenate a response for the input class which is easy for a bot reply. 
    The string will include the Song name and the correct tempo.

    Param: String song: The requested song from the user.

    Returns: A string that has the value for tempo and formatted English sentences for the input class.
    """

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

    """

def reply_get_time_signature(song):
    """
    reply_get_time_signature will call the get_time_signature(song) class which either returns a string or "none", 
    if "none" then return "Sorry! This song does not exist." representing the time signature. This method will 
    concatenate a response for the input class which is easy for a bot reply. The string will include the Song 
    name and the correct time signature value.

    Param: String song: The requested song from the user.

    Returns: A string that has the value for the time signature and formatted English sentences for the input class.
    """

def reply_get_mode(song):
    """
    reply_get_mode will call the get_mode(song) class which returns a  string representing the mode 
    (1 for Major, 0 for Minor). Inside this method, I will convert the numeric representation of mode 
    to the musical representation (either major or minor). This method will concatenate a response for 
    the input class which is easy for a bot reply. The string will include the Song name and the correct mode. 

    Param: String song: The requested song from the user.

    Returns: A string that has the value for the mode and formatted English sentences for the input class.

    """

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
    """


