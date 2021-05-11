import os
import spotipy
import sys
import csv
import discord
import pandas as pd
import numpy as np
from sklearn import ensemble  # for random forests

from spotipy.oauth2 import SpotifyOAuth
from spotipy import SpotifyException
from dotenv import load_dotenv

from MusicAnalytics.MusicTheory import get_all_music_theory

sys.path.append('../')
load_dotenv()

# CREATE SPOTIPY OBJECT
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
scope = "user-read-recently-played, user-top-read, user-read-playback-position, user-read-playback-state, user-modify-playback-state, user-read-currently-playing, playlist-modify-public, playlist-modify-private, user-read-private, playlist-read-private, playlist-read-collaborative, ugc-image-upload"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET,
                            redirect_uri=REDIRECT_URI,
                            scope=scope, cache_path=".oAuthCache"))

def song_add(url, classification):
    """
    Takes in a playlist url and gets the audio features of the songs in the album

    Inputs:
     - url: a url to a spotify playlist
     - classification: name of the classification the songs are part of
    """
    try:
        results = sp.playlist(url)
    except SpotifyException:
        return "Unsuccessful Add"

    fieldnames = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                       'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'class']
    # For every item in the plalyist, grab the track name, features, 
    # and add the results to a features dictionary.
    with open(r'bending_songs.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        for item in results['tracks']['items']:
            fields = {}
            song_name = item['track']['name']
            music_theory_results = get_all_music_theory(song_name)
            if music_theory_results == 'None':
                print(f"Song {song_name} was not added.")
                continue
            song_features, _ = music_theory_results
            if len(song_features) != 11:
                print(f"{song_name} did not have 11 Audio Features!")

            for key, value in song_features.items():
                if not value:
                    fields[key] = None
                else:
                    if value == 0:
                        fields[key] = 0.0
                    else: 
                        fields[key] = value

            fields['class'] = classification

            writer.writerow(fields)

    return f"Successfully added the {classification} playlist."


def playlist_stats_helper(playlist_url):
    """
        retrieve the average audio features and name of a user-specified playlist
        Input: playlist_url A url that links to a Spotify
               playlist.
        Output: a tuple containing the name of the playlist and a dict of features.
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


def bending_helper(features):
    """
        match the dictionary of average audio features to an ATLA element
        using ML predictor
        Input: a dictionary of audio features
        Output: A string containing the element
    """
    # DATA CLEANING
    filename = 'bending_songs.csv'
    df = pd.read_csv(filename, header=0)
    df_filled = df.fillna(0)
    COLUMNS = df_filled.columns    
    COL_INDEX = {}
    for i, name in enumerate(COLUMNS):
        COL_INDEX[name] = i
    
    ELEMENT = ['Fire', 'Water', 'Earth', 'Air']
    ELEMENT_INDEX = {k: v for v, k in enumerate(ELEMENT)}

    def convert_species(element):
        """ return the species index (a unique integer/category) """
        return ELEMENT_INDEX[element]
    
    df_filled['class'] = df_filled['class'].apply(convert_species)
    A = df_filled.values 
    A = A.astype('float64') 

    # DATA DEFINITIONS
    X_all = A[:,0:11] 
    y_all = A[:,11]

    # PREDICTIVE MODEL
    rforest_model_final = ensemble.RandomForestClassifier(max_depth=9, n_estimators=100)

    rforest_model_final.fit(X_all, y_all)              # yay!  trained!
    our_features = np.asarray([features])                 # extra brackets needed
    predicted_element = rforest_model_final.predict(our_features)
    
    predicted_element = int(round(predicted_element[0]))  # unpack one element
    name = ELEMENT[predicted_element]

    return f"{name}"

async def which_bending(playlist_url, ctx):
    """
        Match the playlist to a bending type by running its average
        audio features through our model. Sends the user a discord embeded
        message with their result.
        Input: playlist_url A url that links to a Spotify playlist. ctx a
               context object used to send the message 
        Output: A confirmation message
    """

    rtnTuple = playlist_stats_helper(playlist_url)
    if rtnTuple == None:
        return None

    name, average_feats = rtnTuple

    # Run average_feats of playlist through predictor
    element = bending_helper(average_feats)

    # get image of ATLA element
    image = element + ".jpg"
    
    # create an embed with all the informaiton
    image_file = discord.File(image)
    title_message = "You element is " + element
    reply = f"Based on your playlist {name}, you're a/an {element} bender! \n" \
            "Nice."
    embed = discord.Embed(title=title_message, description=reply, color= 0x2ecc71) 
    # Set up the image URL thumbnail
    embed.set_thumbnail(url="attachment://" + image)
    await ctx.send(file=image_file, embed=embed)
    return "Here's the personality of your playlist!"
