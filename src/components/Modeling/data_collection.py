import os
import spotipy
import sys
import csv

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
scope = "user-read-recently-played, user-top-read, user-read-playback-position, user-read-playback-state, user-modify-playback-state, user-read-currently-playing, playlist-modify-public, playlist-modify-private, user-read-private, ugc-image-upload"
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
