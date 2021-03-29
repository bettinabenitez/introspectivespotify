from __future__ import print_function    # (at top of module)
import os
import spotipy
import time
import sys
import json
import pandas as pd
import seaborn as sns
import cv2
import matplotlib.pyplot as plt
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go
from collections import OrderedDict
from math import log
from glob import glob
import textwrap
import base64
from PIL import ImageFont, ImageDraw, Image
from datetime import timedelta
import calendar
import statistics

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
from SpotifyAuth.SpotifyAuth import get_spotify_id

load_dotenv()

# CREATE SPOTIPY OBJECT
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
scope = "user-read-recently-played, user-top-read, user-read-playback-position, user-read-playback-state, user-modify-playback-state, user-read-currently-playing, playlist-modify-public, playlist-modify-private, user-read-private, ugc-image-upload"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET,
                            redirect_uri=REDIRECT_URI,
                            scope=scope, cache_path=".oAuthCache"))

def cover_graphs_helper(playlist_url):
    """
        Retrieve a list of tempos, list of danceability and name of a user-specified playlist
        Input: playlist_url A url that links to a Spotify
               playlist.
        Output: Playlist name, features dictionary
    """

    tempo = []
    dance = []
    mood = []
    
    results = sp.playlist(playlist_url)
    num_tracks = len(results['tracks']['items'])

    for item in results['tracks']['items']:
        song_name = item['track']['name']
        song_features = get_all_music_theory(song_name)
        if song_features == 'None':
            continue
        tempo.append(song_features['tempo'])
        dance.append(song_features['danceability'])
        mood.append(song_features['valence'])

    return (results['name'], results['owner']['display_name'], results['owner']['id'], tempo, dance, mood)

def personality_graphs_helper(playlist_url):
    """
        Retrieve the average audio features and name of a user-specified playlist
        Input: playlist_url A url that links to a Spotify
               playlist.
        Output: Playlist name, features dictionary
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

    return (results['name'], features)


def personality_graphs(playlist_url):
    """
        
    """
    graph_features = ['danceability', 'energy', 'instrumentalness', 'acousticness', 'valence', 'tempo']

    name, average_feats = personality_graphs_helper(playlist_url)
    
    # scale the tempo to be between 0 and 1
    average_feats['tempo'] /= 200
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
    
    ax.set_title('{} {}'.format('Personality of', name), y=1.08)
    ax.plot(angs, vals, color=clr, linewidth=1)
    ax.fill(angs, vals, color=clr, alpha=0.6)

    # Fix axis to go in the right order and start at 12 o'clock.
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    # Draw axis lines for each angle and label.
    ax.set_thetagrids(np.degrees(angs[:-1]), graph_features)
    # ax.set_rgrids([0, 0.2, 0.4, 0.6, 0.8,1])
    # removing white background
    # ax.patch.set_alpha(0.0)
    # fig.patch.set_alpha(0.0)
    # remove axis lines 
    # ax.axis('off')

    fig.savefig(fname='plot.png')



def cover_graph(playlist_url, discord_user, filename):
    """
        
    """
    name, user, user_id, tempo, dance, mood = cover_graphs_helper(playlist_url)
    # Divide tempo by 200 to scale values down. If not, give default val of 1.0.
    tempo_mean = np.mean(tempo)
    tempo = list(map(lambda x: x/tempo_mean, tempo))
    
    mood_mean = np.mean(mood)
    color_start = 0.0
    color = (127, 84, 141)
    if mood_mean <= .25:
        color_start = 2.0
        color = (166, 142, 99)
    elif mood_mean <= .5:
        color_start = 1.67
        color = (137, 153, 88)
    elif mood_mean <= .75:
        color_start = .33
        color = (118, 130, 161)

    sns.set_theme(style="white")
    
    # fig, ax = plt.subplots(figsize=(4, 4))
    fig, ax = plt.subplots(figsize=(10, 10))
    # Rotate the starting point around the cubehelix hue circle
    # for ax, s in zip(axis.flat, np.linspace(0, 3, 10)):

    # Create a cubehelix colormap to use with kdeplot
    cmap = sns.cubehelix_palette(start=color_start, light=1, as_cmap=True)
    sns.kdeplot(
        x=tempo, y=dance,
        cmap=cmap, fill=True,
        clip=(-6, 6), cut=10,
        thresh=0, levels=10,
        ax=ax,
    )
    ax.set_axis_off()
    ax.margins(x=0, y=-0.25)
    
    #title_format = name + " ".format(3, 5)
    # ax.set_title('{}'.format(name), y=1.08)
    # ax.text(1, .7, name, ha='center', wrap=True, fontsize=20)
    # ax.text(1, .7, title_format, ha='center', wrap=True, fontsize=20)
    
    # ax.set(xlim=(-3.5, 3.5), ylim=(-3.5, 3.5))
    #fig.subplots_adjust(0, 0, 1, 1, .08, .08)

    fig.savefig(fname=filename, bbox_inches='tight')  
    write_title(name, user, color, filename)

    return get_spotify_id(discord_user) == user_id

def write_title(name, user, color, filename):
    #Read Image
    img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    # setup text
    # font = cv2.FONT_HERSHEY_SIMPLEX
    font_size = 1
    font_thickness = 2
    font_path = "./fonts/Teko-Light.ttf"
    
    TEXT_GAP = 40

    # PIL vars
    font = ImageFont.truetype(font_path, 32)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)

    # get boundary aof text nd coords based on bounds
    wrapped_text = textwrap.wrap(name, width=35)
    # wrapped_text = textwrap.wrap(name + " by " + user, width=35)
    for i, line in enumerate(wrapped_text):
        # textsize = cv2.getTextSize(line, font, font_size, font_thickness)[0]
        textsize = font.getsize(line)
        y = TEXT_GAP + (i * TEXT_GAP)
        x = int((img.shape[1] - textsize[0]) / 2)

        # add tet centered on image and rewrite image
        # cv2.putText(img, line, (x, y), font, font_size, (0, 0, 0), font_thickness, lineType = cv2.LINE_AA)
        draw.text((x,y), line, font=font, fill=color)
    by_line = "curated by " + user
    textsize = font.getsize(by_line)
    x = int((img.shape[1] - textsize[0]) / 2)
    draw.text((x,img.shape[0]-(2*TEXT_GAP)), by_line, font=font, fill=color)

    img = np.array(img_pil)
    cv2.imwrite(filename, img)



def upload_cover(url, user, filename):

    auth_token = get_access_token(user)
    if auth_token is None:
        return "You have not logged in!"
    sp.set_auth(auth_token)

    with open(filename, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())

    sp.playlist_upload_cover_image(url, b64_string)

    return "Playlist cover successfully uploaded! 🎶🖼"

def timeline_graphs():
    streaming_history = read_history()
    streaming_history["date"] = streaming_history["endTime"].dt.floor('d')

    by_date = streaming_history.groupby("date")[["trackName"]].count()
    by_date = by_date.sort_index()

    by_date["weekday"] = by_date.index.weekday
    by_date["week"] = by_date.index.week

    week = 0
    prev_week = by_date.iloc[0]["week"]
    continuous_week = np.zeros(len(by_date)).astype(int)
    sunday_dates = []
    for i, (_, row) in enumerate(by_date.iterrows()):
        if row["week"] != prev_week:
            week += 1
            prev_week = row["week"]
        continuous_week[i] = week
    by_date["continuous_week"] = continuous_week 
    by_date.head()

    songs = np.full((7, continuous_week.max()+1), np.nan)

    for index, row in by_date.iterrows():
        songs[row["weekday"]][row["continuous_week"]] = row["trackName"]

    fig = plt.figure(figsize=(20,5))
    ax = plt.subplot()
    mask = np.isnan(songs)
    sns.heatmap(songs, ax = ax)

    min_date = streaming_history["endTime"].min()
    first_monday = min_date - timedelta(min_date.weekday())
    mons = [first_monday + timedelta(weeks=wk) for wk in range(continuous_week.max())]
    x_labels = [calendar.month_abbr[mons[0].month]]
    x_labels.extend([
        calendar.month_abbr[mons[i].month] if mons[i-1].month != mons[i].month else "" 
        for i in range(1, len(mons))])
    x_labels.append('')
    y_labels = ["Mon", "", "Wed", "", "Fri", "", "Sun"]

    fig = plt.figure(figsize=(20,5))
    ax = plt.subplot()

    ax.set_title("My year on Spotify", fontsize=20,pad=40)
    ax.xaxis.tick_top()
    ax.tick_params(axis='both', which='both',length=0)
    ax.set_facecolor("#ebedf0") 
    fig.patch.set_facecolor('white')
    sns.heatmap(songs, linewidths=2, linecolor='white', square=True,
            mask=np.isnan(songs), cmap="Greens",
            vmin=0, vmax=100, cbar=False, ax=ax)

    ax.set_yticklabels(y_labels, rotation=0)
    ax.set_xticklabels(x_labels, ha="left")


    fig.savefig(fname='timeplot.png')

def read_history():
    history = []
    for i in range(6):
        with open("./src/components/Visualization/StreamingHistory" + str(i) + ".json", "r", encoding="utf8") as readable:
            history.extend(json.load(readable))
    
    history = pd.DataFrame(history)
    history["endTime"] = pd.to_datetime(history["endTime"])
    return history

