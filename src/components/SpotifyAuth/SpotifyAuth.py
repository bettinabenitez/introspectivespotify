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

def spotify_login(user):
    pass

def spotify_logout(user):
    pass

def get_access_token(user):
    pass
