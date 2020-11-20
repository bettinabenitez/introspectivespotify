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


def __audio_features_help(song):
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
    """
    results = sp.search(q= song, type="track", limit=1)
    
    for  item in results['tracks']['items']:      
        trackID = item['id']
        if trackID != " ":
            audioFeatures = sp.audio_features(trackID)
            return audioFeatures
    return "Sorry! That track does not exist"

test = __audio_features_help("Thank you for the music")
print(test)

test1 = __audio_features_help("Foo bar Bash Songs")
print(test1)