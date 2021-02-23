from __future__ import print_function    # (at top of module)
import os
import spotipy
import time
import sys
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go
from collections import OrderedDict
from math import log
#import calmap

from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from statistics import multimode

from MusicAnalytics.MusicTheory import get_tempo
from MusicAnalytics.MusicTheory import get_key
from MusicAnalytics.MusicTheory import get_instrumentalness
from MusicAnalytics.MusicTheory import get_danceability
from MusicAnalytics.MusicTheory import get_mode
from MusicAnalytics.MusicTheory import get_time_signature
from MusicAnalytics.MusicTheory import get_energy
from MusicAnalytics.MusicTheory import get_acousticness
from MusicAnalytics.MusicTheory import get_mood
from MusicAnalytics.MusicTheory import reply_all_music_theory
from MusicAnalytics.MusicTheory import audio_features_help

sys.path.append('../')
from SpotifyAuth.SpotifyAuth import get_access_token

load_dotenv()

# CREATE SPOTIPY OBJECT
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
scope = "user-read-recently-played, user-top-read, user-read-playback-position, user-read-playback-state, user-modify-playback-state, user-read-currently-playing, playlist-modify-public, user-read-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET,
                            redirect_uri=REDIRECT_URI,
                            scope=scope, cache_path=".oAuthCache"))


def playlist_features(playlist_url):
    """
        Retrieve all of the audio features for a 
        user-specified playlist.
        Input: playlist_url A url that links to a Spotify
               playlist.
    """
    results = sp.playlist(playlist_url)
    features = {}
    for item in results['tracks']['items']: 
        song_features = audio_features_help(item)[0]
        for key in song_features.keys():
            features[key] = features.get(key, 0.0) + song_features[key]

    print(features)
    return "None"
