import os
import spotipy
import sys
import json
import pandas as pd
import seaborn as sns
import cv2
import matplotlib.pyplot as plt
import numpy as np
from glob import glob
import textwrap
import base64
from PIL import ImageFont, ImageDraw, Image

from spotipy.oauth2 import SpotifyOAuth
from spotipy import SpotifyException
from dotenv import load_dotenv

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
        Output: Playlist name, Playlist Owner, Tempo, Danceability, and Mood in a features dictionary
    """
    # Create default lists for storing values
    tempo = []
    dance = []
    mood = []
    # Grab the API result into a dictionary
    try:
        results = sp.playlist(playlist_url)
    except SpotifyException:
        return None
    num_tracks = len(results['tracks']['items'])

    # Append the tempo, danceability, mood
    # to a results list, add playlist name, 
    # Spotify username and ID.
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
        Output: A PNG figure representing a playlist specific polar graph.
    """
    # Spotipy call to grab playlist data
    try:
        results = sp.playlist(playlist_url)
    except SpotifyException:
        return None 
    num_tracks = len(results['tracks']['items'])
    features = {}
    # For every item in the plalyist, grab the track name, features, 
    # and add the results to a features dictionary.
    for item in results['tracks']['items']:
        song_name = item['track']['name']
        song_features = get_all_music_theory(song_name)
        if song_features == 'None':
            continue
        for key, value in song_features.items():
            # value/num_tracks is the contribution from one song to the entire average
            features[key] = features.get(key, 0.0) + (value/num_tracks)

    return (results['name'], features)


def personality_graphs(playlist_url, filename):
    """
        Create a polar graph using the playlist url that graphs 
        danceability, energy, instrumentalness, acousticness, valence, and tempo
        with a random color generator. 
        Input: playlist_url A url that links to a Spotify playlist.
               filename: A string representing "cover_playlistID" for formatting.
        Output: Playlist name, features dictionary
    """
    graph_features = ['danceability', 'energy', 'instrumentalness', 'acousticness', 'valence', 'tempo']

    rtnTuple = personality_graphs_helper(playlist_url)
    if rtnTuple == None:
        return None

    name, average_feats = rtnTuple
    
    # scale the tempo to be between 0 and 1
    average_feats['tempo'] /= 200
    if average_feats['tempo'] > 1.0: average_feats['tempo'] = 1.0 
    
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
    
    # set title of playlist REMOVE IF USING TEMPLATE 
    ax.set_title('{} {}'.format('Personality of', name), y=1.08)

    ax.plot(angs, vals, color=clr, linewidth=1)
    ax.fill(angs, vals, color=clr, alpha=0.6)

    # Fix axis to go in the right order and start at 12 o'clock.
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)

    # Draw axis lines for each angle.
    ax.set_thetagrids(np.degrees(angs[:-1]), graph_features)
    ax.set_rgrids([0, 0.2, 0.4, 0.6, 0.8,1])
    
    # If we want to remove the background of the image, uncomment this: 
        # # removing white background
        # ax.patch.set_alpha(0.0)
        # fig.patch.set_alpha(0.0)
        # # remove axis lines 
        # ax.axis('off')

    fig.savefig(fname=filename)
    return "Here's the personality of your playlist!"



def cover_graph(playlist_url, discord_user, filename):
    """
        Retrieve the mood and tempo of a user specified Spotify Playlist and 
        creates a Seaborn graph in a color specific to mood with the 
        playlist name and Spotify author overlayed ontop, returns 
        a boolean check to ensure the user who called the command 
        is the same author of the Playlist. 
        Input: playlist_url: A url that links to a Spotify playlist
               discord_user: A unique ID that is specific to the Discord command caller.
               filename: A string representing "cover_playlistID" for formatting.
        Output: A boolean check that ensures the user who called the command 
                is the same as the playlist author. Will trigger an addtional function 
                to upload the new graphic, otherwise will just create a png image. 
    """
    returnTPL = cover_graphs_helper(playlist_url)

    if returnTPL == None:
        return None
    
    name, user, user_id, tempo, dance, mood = returnTPL
    
    # Divide tempo by 200 to scale values down. If not, give default val of 1.0.
    tempo_mean = np.mean(tempo)
    tempo = list(map(lambda x: x/tempo_mean, tempo))
    mood_mean = np.mean(mood)

    # determine color based on playlist's average mood
    color_start = 0.0
    color = (127, 84, 141)
    if mood_mean <= .25:
        # sad
        color_start = 2.0
        color = (166, 142, 99)
    elif mood_mean <= .5:
        color_start = 1.67
        color = (137, 153, 88)
    elif mood_mean <= .75:
        color_start = .33
        color = (118, 130, 161)

    sns.set_theme(style="white")
    
    fig, ax = plt.subplots(figsize=(10, 10))

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
    
    fig.savefig(fname=filename, bbox_inches='tight')  
    write_title(name, user, color, filename)

    # returns True if current user owns the Spotify playlist
    return get_spotify_id(discord_user) == user_id

def write_title(name, user, color, filename):
    # read Image
    img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
    
    # setup text
    font_size = 1
    font_thickness = 2
    font_path = "./fonts/Teko-Light.ttf"
    TEXT_GAP = 40

    # PIL vars
    font = ImageFont.truetype(font_path, 32)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)

    # get boundary of text and coords based on bounds
    wrapped_text = textwrap.wrap(name, width=35)
    for i, line in enumerate(wrapped_text):

        # get position for text (top center)
        textsize = font.getsize(line)
        y = TEXT_GAP + (i * TEXT_GAP)
        x = int((img.shape[1] - textsize[0]) / 2)

        # add text
        draw.text((x,y), line, font=font, fill=color)
    
    # add by line at bottom of image
    by_line = "curated by " + user
    textsize = font.getsize(by_line)
    x = int((img.shape[1] - textsize[0]) / 2)
    draw.text((x,img.shape[0]-(2*TEXT_GAP)), by_line, font=font, fill=color)

    # save the file
    img = np.array(img_pil)
    cv2.imwrite(filename, img)



def upload_cover(url, user, filename):
    """
        Calls the Spotify API to upload our generated playlist to a specific 
        playlist url. Converts the generated playlist cover to a bit 64 image
        for the API call. 
        Input: url: A url that links to a Spotify playlist
               user: A unique ID that is specific to the Discord command caller.
               filename: A string representing "cover_playlistID" for formatting.
        Output: A string confirming an image was successfully uploaded for the InputClass
                to output to the user. 
    """
    # set sp object with user's auth token
    auth_token = get_access_token(user)
    if auth_token is None:
        return "You have not logged in!"
    sp.set_auth(auth_token)
    
    # convert file to base64
    with open(filename, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read())

    try:
        sp.playlist_upload_cover_image(url, b64_string)
    except SpotifyException:
        return "An unexpected error occurred :("
    
    return "Playlist cover successfully uploaded! 🎶🖼"
 # HI WE SHOULD ERROR CATCH HERE
