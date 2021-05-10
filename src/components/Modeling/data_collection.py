import os
import spotipy
import sys
import csv
import discord

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

def song_add(url, movie):
    """
    Takes in a album url and gets the audio features of the songs in the album

    Inputs:
     - Search: song (and artist) to search on spotify
     - Movie: name of the movie the song is part of
    """
    try:
        results = sp.album(url)
    except SpotifyException:
        return "Unsuccessful Add"

    fieldnames = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
                       'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'movie']
    # For every item in the plalyist, grab the track name, features, 
    # and add the results to a features dictionary.
    with open(r'movie_songs.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        for item in results['tracks']['items']:
            fields = {}
            song_name = item['name']
            song_features = get_all_music_theory(song_name)
            if results == 'None':
                print(f"Song {song_name} was not added.")
                continue

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

            fields['movie'] = movie

            writer.writerow(fields)

    return f"Successfully added the {movie} soundtrack"

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
    return

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
