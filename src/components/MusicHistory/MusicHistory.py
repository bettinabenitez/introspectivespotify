import sys
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from statistics import multimode

sys.path.append('../')
from MusicTheory.MusicTheory import get_tempo
from MusicTheory.MusicTheory import get_key
from MusicTheory.MusicTheory import get_instrumentalness
from MusicTheory.MusicTheory import get_danceability
from MusicTheory.MusicTheory import get_mode
from MusicTheory.MusicTheory import get_time_signature
from MusicTheory.MusicTheory import get_energy
from MusicTheory.MusicTheory import get_acousticness
from MusicTheory.MusicTheory import get_mood

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

        
######################################
##### COMPUTATION HELPER METHODS #####
######################################
def compute_genre_helper(genre_dictionary, limit):
    """Returns a user's top genres given a dictionary containing potential top genres and their corresponding rankings
    :param genre_dictionary: keys = genre name, values = a list of ints representing the ranking of artist
    :type genre_dictionary: dictionary 

    :param limit: indicate how many artists to compute, defaults to 5. Minimum of 1, maximum of 10. 
    :type limit: int 

    :rtype: list
    :return: a queue of top genres sorted from most listened to genre to least listened to 
    """
    # check if limit is out of bounds
    if limit > 10:
        limit = 10

    top_genre_queue = []

    # sort the genre_dictionary based on the number of artists each genre is associated with
    genre_dictionary = sorted(genre_dictionary, key=lambda k: len(genre_dictionary[k]), reverse=True)
    
    count = 0
    # add genre to top_genre_queue until limit is reached
    for genre in genre_dictionary:
        if count < limit:
            top_genre_queue.append(genre)
            count += 1
        else:
            break
    
    return top_genre_queue

def compute_top_songs_theory_helper(theory_dictionary):
    """Returns theory data on a user's top songs over a given time range 
    :param theory_dictionary: 
    :type theory_dictionary: dictionary 

    :rtype: dictionary
    :return: a sorted dictionary with both the song IDs (key) and song names (value)
    """
    for feature in theory_dictionary:
        if feature == "key" or feature == "mode":
            # find the multimode (all "tied" elements are added into a list)
            theory_dictionary[feature] = multimode(theory_dictionary[feature])
        else:
            # find the mean
            theory_dictionary[feature] = round(sum(theory_dictionary[feature]) / len(theory_dictionary[feature]), 2)
    return theory_dictionary

###############################
##### COMPUTATION METHODS #####
###############################
def compute_genre(time_range, limit):
    """Returns a user's top genre(s) over a given time range 
    :param time_range: when in the user's Spotify history to analyze. (long, medium, or short) defaults to medium 
    :type time_range: string 

    :param limit: indicate how many genres to compute, defaults to 3. Minimum of 1, maximum of 5. 
    :type limit: int 

    :param discord_user: Discord user's username that we want to analyze
    :type discord_user: string 

    :rtype: list
    :return: a queue in the order of most listened to genre to least listened to
    """
    # Make Spotify API call to get user's top artists
    results = sp.current_user_top_artists(time_range=time_range, limit=20)

    # key = genre name, value = "rankings" of the artist(s) associated with the genre 
    top_genres_dict = {}
    for index, artist in enumerate(results['items']):
        for genre in artist['genres']: 
            if top_genres_dict.get(genre) == None: 
                top_genres_dict[genre] = [index]
            else:
                top_genres_dict[genre].append(index)

    # take care of edge case - all top artists have no genre 
    if top_genre_dict == {}:
        return []
    else:
        return compute_genre_helper(top_genres_dict, limit)

def compute_top_songs(time_range, limit):
    """Returns a user's top songs(s) over a given time range 
    :param time_range: when in the user's Spotify history to analyze. (long, medium, or short) defaults to medium 
    :type time_range: string 

    :param limit: indicate how many songs to compute, defaults to 5. Minimum of 1, maximum of 10. 
    :type limit: int 

    :param discord_user: Discord username of the person that we want to analyze
    :type discord_user: string 

    :rtype: dictionary 
    :return: dictionary with both the IDs and name 
    """
    # Make Spotify API call 
    results = sp.current_user_top_tracks(time_range=time_range, limit=limit)

    # loop through JSON to get the track names and track IDs 
    top_songs_dict = {}
    for song in results['items']:
        # store in dict. key = id, value = name 
        top_songs_dict[song['id']]  = [song['name'], song['artists'][0]['name']]

    return top_songs_dict

def compute_top_artists(time_range, limit):
    """Returns a user's top artists(s) over a given time range 
    :param time_range: when in the user's Spotify history to analyze. (long, medium, or short) defaults to medium 
    :type time_range: string 

    :param limit: indicate how many artists to compute, defaults to 5. Minimum of 1, maximum of 10. 
    :type limit: int 

    :param discord_user: Discord username of the person that we want to analyze
    :type discord_user: string 

    :rtype: list
    :return: dictionary with both the IDs and name 
    """
    # Make Spotify API call 
    results = sp.current_user_top_artists(time_range=time_range, limit=limit)

    # loop through JSON to get the artists' names
    top_artists_queue = []
    for artist in results['items']:
        top_artists_queue.append(artist['name'])

    return top_artists_queue

def compute_top_songs_theory(top_songs):
    """Returns theory data on a user's top songs over a given time range 
    :param top_song: a dictionary that stores a user's top songs 
    :type top_song: dictionary 

    :rtype: dictionary
    :return: a sorted dictionary with both the song IDs (key) and song names (value)
    """
    theory_dictionary = {"tempo": [],
                        "time_signature": [],
                        "key": [],
                        "mode": [],
                        "mood": [],
                        "danceability": [],
                        "acousticness": [],
                        "energy": [],
                        "instrumentalness": []}

    for song in top_songs:
        song = song[0] + " " + song[1] # song name + artist name 
        theory_dictionary["tempo"].append(float(get_tempo(song)))
        theory_dictionary["time_signature"].append(int(get_time_signature(song)))
        theory_dictionary["key"].append(get_key(song))
        theory_dictionary["mode"].append(get_mode(song))
        theory_dictionary["mood"].append(float(get_mood(song)))
        theory_dictionary["danceability"].append(float(get_danceability(song)))
        theory_dictionary["acousticness"].append(float(get_acousticness(song)))
        theory_dictionary["energy"].append(float(get_energy(song)))
        theory_dictionary["instrumentalness"].append(float(get_instrumentalness(song)))
    return compute_top_songs_theory_helper(theory_dictionary)

#########################
##### REPLY METHODS #####
#########################
def reply_top_genres(time_range, limit):
    """Returns a string with a user's top genres that the Discord Bot will reply to the chat 
    :param time_range: when in the user's Spotify history to analyze. (long, medium, or short) defaults to medium 
    :type time_range: string 

    :param limit: indicate how many genres to compute, defaults to 3. Minimum of 1, maximum of 5. 
    :type limit: int 

    :param discord_user: Discord user's username that we want to analyze
    :type discord_user: string 

    :rtype: string
    :return: a string that describes what a user's top genres are
    """
    try:
        # TO DO: call set_auth from Spotify Auth component 

        top_genres_queue = compute_genre(time_range, limit)

        # take care of edge case - all top artists have no genre 
        if top_genres_queue == []:
            return "Sorry, no top genres were found! Spotify is still gathering info about your top artists. Try again another time."

        if limit == 1:
            return "Your top genre is " + top_genres_queue[0] + ". Happy listening!"
        else: 
            output = "Your top genres are"
            for index, genre in enumerate(top_genres_queue):
                output += " (" + str(index + 1) + ") " + genre 
            return output + ". Happy listening!"
    except:
        return "An exception occurred. Something went wrong. :( uh oh"
    
def reply_top_songs(time_range, limit):
    """Returns a string with a user's top songs that the Discord Bot will reply to the chat 
    :param time_range: when in the user's Spotify history to analyze. (long, medium, or short) defaults to medium 
    :type time_range: string 

    :param limit: indicate how many songs to compute, defaults to 5. Minimum of 1, maximum of 10. 
    :type limit: int 

    :param discord_user: Discord username of the person that we want to analyze
    :type discord_user: string 

    :rtype: string
    :return: a string that describes what a user's top songs are
    """
    try:
        # TO DO: call set_auth from Spotify Auth component 

        top_songs_dict = compute_top_songs(time_range, limit)
        if limit == 1:
            song_details = list(top_songs_dict.values())[0] 
            return "Your top song is " + str(song_details[0]) + " by " + str(song_details[1]) + ". Nice bop!"
        else: 
            output = "Your top songs are"
            for index, song_details in enumerate(top_songs_dict.values()):
                output += " (" + str(index + 1) + ") " + song_details[0] + " by " + song_details[1]
            return output + ". Nice bops!"
    except:
        return "An exception occurred. Something went wrong. :( uh oh"

def reply_top_artists(time_range, limit):
    """Returns a string with a user's top artists that the Discord Bot will reply to the chat 
    :param time_range: when in the user's Spotify history to analyze. (long, medium, or short) defaults to medium 
    :type time_range: string 

    :param limit: indicate how many artists to compute, defaults to 5. Minimum of 1, maximum of 10. 
    :type limit: int 

    :param discord_user: Discord username of the person that we want to analyze
    :type discord_user: string 
    
    :rtype: string
    :return: a string that describes what a user's top artists are
    """
    try:
        # TO DO: call set_auth from Spotify Auth component 

        top_artists_queue = compute_top_artists(time_range, limit)
        if limit == 1:
            return "Your top artist is " + top_artists_queue[0] + ". You have great taste!"
        else: 
            output = "Your top artists are"
            for index, artist in enumerate(top_artists_queue):
                output += " (" + str(index + 1) + ") " + artist
            return output + ". You have great taste!"
    except:
        return "An exception occurred. Something went wrong. :( uh oh"

def reply_top_songs_theory(time_range, limit):
    """Returns a string with a user's theory data on their top songs over a given time range that
    the Discord Bot will reply to the chat 
    :param time_range: when in the user's Spotify history to analyze. (long, medium, or short) defaults to medium 
    :type time_range: string 

    :param discord_user: Discord username of the person that we want to analyze
    :type discord_user: string 

    :param top_songIDs: a dictionary that stores a user's top songs 
    :type top_songIDs: dictionary 

    :param discord_user: Discord username of the person that we want to analyze

    :rtype: string
    :return: a string that describes what a user's theory data on top songs
    """
    output = "Your top song"
    if limit == 1:
        output += "has the following music theory features:"
    else:
        output += "s have the following music theory features:"

    try:
        # TO DO: call set_auth from Spotify Auth component 

        top_songs = list(compute_top_songs(time_range, limit).values())
        theory_dictionary = (compute_top_songs_theory(top_songs))
        for feature in theory_dictionary:
            if feature == "key":
                key_dict = {"0": "C",
                            "1": "C#/D♭",
                            "2": "D",
                            "3": "D#/E♭",
                            "4": "E",
                            "5": "F",
                            "6": "F#/G♭",
                            "7": "G",
                            "8": "G#/A♭",
                            "9": "A",
                            "10": "A#/B♭",
                            "11": "B"}
                if len(theory_dictionary[feature]) == 1:
                    output += "\n• modal key of " + key_dict[theory_dictionary[feature][0]] + "."
                else: 
                    top_keys = ""
                    for key in theory_dictionary[feature]:
                        top_keys += key_dict[key] + ", "
                    output += "\n• modal keys of " + top_keys[:-2] + "."
            elif feature == "mode":
                mode_dict = {"1": "major", "0": "minor"}
                if len(theory_dictionary[feature]) == 1:
                    output += "\n• modal modality of " + mode_dict[(theory_dictionary[feature][0])] + "."
                else: 
                    output += "\n• modal modalities of major and minor."
            else:
                output += "\n• mean " + str(feature) + " of " + str(theory_dictionary[feature]) + "."
        return output
    except:
        return "An exception occurred. Something went wrong. :( uh oh"
