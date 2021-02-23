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
from MusicAnalytics.MusicTheory import get_all_music_theory

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


def average_playlist_features(playlist_url):
    """
        Retrieve the average audio features of a user-specified playlist.
        Input: playlist_url A url that links to a Spotify
               playlist.
    """
    results = sp.playlist(playlist_url)
    num_tracks = len(results['tracks']['items'])
    features = {}
    for item in results['tracks']['items']:
        song_name = item['track']['name']
        song_features = get_all_music_theory(song_name)
        if song_features == 'None':
            continue
        for key, value in song_features.items():
            # value/num_tracks is the contribution from one song to the entire average
            features[key] = features.get(key, 0.0) + (value/num_tracks)

    return features


def personality_graphs(playlist_url):
    graph_features = ['danceability', 'energy', 'speechiness', 'acousticness', 'valence', 'tempo']

    average_feats = average_playlist_features(playlist_url)
    
    # scale the tempo to be between 0 and 1
    average_feats['tempo'] = average_feats['tempo'] / 200
    if average_feats['tempo'] > 1.0: average_feats['tempo'] = 1.0 

    # adjust speechiness and acoustiness


    # Number of variables we're plotting.
    num_vars = len(graph_features)

    # Split the circle into even parts and save the angles
    # so we know where to put each axis.
    angs = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    

    vals = []
    for feat, val in average_feats.items():
        if feat in graph_features:
            vals.append(val)

    # loop it
    angs += angs[:1] 
    vals += vals[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # get random color
    clr = [np.random.choice(range(256))/255.0 for i in range(3)]

    ax.plot(angs, vals, color=clr, linewidth=1)
    ax.fill(angs, vals, color=clr, alpha=0.6)

    # Fix axis to go in the right order and start at 12 o'clock.
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    
    # Draw axis lines for each angle and label.
    ax.set_thetagrids(np.degrees(angs[:-1]), graph_features)
    
    ax.set_rgrids([0, 0.2, 0.4, 0.6, 0.8,1])
    ax.set_title("swag", y=1.08)
    fig.savefig(fname='plot.png')
