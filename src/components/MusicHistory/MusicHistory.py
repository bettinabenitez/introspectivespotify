import sys
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

sys.path.append('../')
import MusicTheory.MusicTheory 

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
    """Returns theory data on a user's top songs over a given time range 
    :param genre_dictionary: keys = genre name, values = a list of ints representing the ranking of artist
    :type genre_dictionary: dictionary 

    :param limit: indicate how many artists to compute, defaults to 5. Minimum of 1, maximum of 10. 
    :type limit: int 

    :rtype: list
    :return: a queue of top genres sorted from most listened to genre to least listened to 
    """
    top_genre_queue = []
    genre_dictionary = sorted(genre_dictionary, key=lambda k: len(genre_dictionary[k]), reverse=True)
    count = 0
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
    # We will loop through the values (lists) in our output dictionary.
    # For values of tempo, mode, danceability, acousticness, energy, and instrumentalness,
    # we will find the average of the list and reset the list to a list containing only the average value.
    # For values of key and time_signature, then we will reset the list as a list
    # containing the element with the most occurrences (the mode). If there are ties, then the new list will include all the tied elements.
    # Returns a dictionary

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
    # TO DO: Calls getAccessToken(discord username) from Spotify Auth class 

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
    
    return (compute_genre_helper(top_genres_dict, limit))

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
    # check is limit is out of bounds 
    if limit > 10:
        limit = 10

    ## TO DO 
    # calls getAccessToken(discord username) from Spotify Auth class 
    # uses accessToken and Spotipy object and get user's top artists songs in JSON (uses limit parameter)
    
    # Make Spotify API call 
    results = sp.current_user_top_tracks(time_range=time_range, limit=limit)

    # loop through JSON to get the track names and track IDs 
    top_songs_dict = {}
    for song in results['items']:
        # store in dict. key = id, value = name 
        # top_songs_dict[song['id']]  = song['name']
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
    # check is limit is out of bounds 
    if limit > 10:
        limit = 10

    ## TO DO 
    # calls getAccessToken(discord username) from Spotify Auth class 
    # uses accessToken and Spotipy object and get user's top artists in JSON

    # Make Spotify API call 
    results = sp.current_user_top_artists(time_range=time_range, limit=limit)

    # loop through JSON to get the artists' names
    top_artists_queue = []
    for artist in results['items']:
        top_artists_queue.append(artist['name'])

    return top_artists_queue

def compute_top_songs_theory(top_songs):
    """Returns theory data on a user's top songs over a given time range 
    :param top_songIDs: a dictionary that stores a user's top songs (passed in from compute_top_songs())
    :type top_songIDs: dictionary 
    # TO DO fix param 

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
        song = str(song[0]) + str(song[1])
        theory_dictionary["tempo"].append(int(get_tempo(song)))
        theory_dictionary["key"].append(int(get_key(song)))
        theory_dictionary["mode"].append(int(get_mode(song)))
        theory_dictionary["mood"].append(int(get_mood(song)))
        theory_dictionary["danceability"].append(int(get_danceability(song)))
        theory_dictionary["acousticness"].append(int(get_acousticness(song)))
        theory_dictionary["energy"].append(int(get_energy(song)))
        theory_dictionary["instrumentalness"].append(int(get_instrumentalness(song)))
    print(theory_dictionary)
    #return compute_top_songs_theory_helper(theory_dictionary)
#print(compute_top_songs_theory())


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
    if limit < 0:
        return "Please try a limit greater than 0! :)"

    try:
        top_genres_queue = compute_genre(time_range, limit)
        if limit == 1:
            return "Your top genre is " + top_genres_queue[0] + ". Happy listening!"
        else: 
            output = "Your top genres are"
            for index, genre in enumerate(top_genres_queue):
                output += " (" + str(index + 1) + ") " + genre 
            return output + ". Happy listening!"
    except:
        print("An exception occurred. Something went wrong. :( uh oh")
    
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
    if limit < 0:
        return "Please try a limit greater than 0! :)"

    try:
        top_songs_dict = compute_top_songs(time_range, limit)
        if limit == 1:
            song_details = list(top_songs_dict.values())[0] 
            return "Your top song is " + str(song_details[0]) + " by " + str(song_details[1]) + ". Nice bops!"
        else: 
            output = "Your top songs are"
            for index, song_details in enumerate(top_songs_dict.values()):
                output += " (" + str(index + 1) + ") " + song_details[0] + " by " + song_details[1]
            return output + ". Nice bops!"
    except:
        print("An exception occurred. Something went wrong. :( uh oh")

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
    if limit < 0:
        return "Please try a limit greater than 0! :)"

    try:
        top_artists_queue = compute_top_artists(time_range, limit)
        if limit == 1:
            return "Your top artist is " + top_artists_queue[0] + ". You have great taste!"
        else: 
            output = "Your top artists are"
            for index, artist in enumerate(top_artists_queue):
                output += " (" + str(index + 1) + ") " + artist
            return output + ". You have great taste!"
    except:
        print("An exception occurred. Something went wrong. :( uh oh")

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
    top_songs = list(compute_top_songs(time_range, limit).values())
    print(compute_top_songs_theory(top_songs))
    # Add try and except block
    # calls compute_top_songs and passes the output to compute_top_songs_theory 
    # stores the output of compute_top_songs_theory in a dictionary
    # loop through the dictionary and format a string ("Your top songs have an average tempo of ...,  your most common key(s) is/are … "). Inside the loop, there should an if/else to check if the length of the length of the value is greater than 1 (there was a tie). If there a tie is found, the string should use the “are” word instead of “is.” The noun should also be plural instead of singular. 
    # Return string 

print(reply_top_songs_theory("medium_term", 6))
