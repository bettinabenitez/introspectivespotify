import sys
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

sys.path.append('../')
from MusicTheory.MusicTheory import get_all_music_theory

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

def compute_top_songs_theory_helper(self, theory_dictionary):
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
        top_songs_dict[song['id']]  = song['name'] 

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

def compute_top_songs_theory(self, top_songIDs, discord_user):
    """Returns theory data on a user's top songs over a given time range 
    :param time_range: when in the user's Spotify history to analyze. (long, medium, or short) defaults to medium 
    :type time_range: string 

    :param top_songIDs: a dictionary that stores a user's top songs (passed in from compute_top_songs())
    :type top_songIDs: dictionary 

    :param discord_user: Discord username of the person that we want to analyze
    :type discord_user: string 

    :rtype: dictionary
    :return: a sorted dictionary with both the song IDs (key) and song names (value)
    """
    theory_dictionary = {"tempo": [],
                        "time_signature": [],
                        "key": [],
                        "mode": [],
                        "danceability": [],
                        "acousticness": [],
                        "energy": [],
                        "instrumentalness": []}
    for song in top_songIDs:
        song_theory = get_all_music_theory(song)
    # loop through top_songIDs dictionary’s keys and calls get_all_music_theory method from the MusicTheory Class on each song ID. Get_all_music_theory returns a dictionary that we will parse through and append data into the values of our theory dictionary. 
    # Call and return compute_top_songs_theory_helper with theory dictionary as a parameter 


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
            print(top_songs_dict)
            return "Your top song is " + list(top_songs_dict.values())[0] + ". Nice bops!"
        else: 
            output = "Your top songs are"
            for index, song in enumerate(top_songs_dict.values()):
                output += " (" + str(index + 1) + ") " + song 
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
    :type discord_user: string 

    :rtype: string
    :return: a string that describes what a user's theory data on top songs
    """
    # song_ids = compute_top_songs(time_range, limit).keys()
    # print(song_ids)
    song_ID = '1ApN1loxlt0rzRFc8iETw7'
    get_all_music_theory(song_ID)
    # Add try and except block
    # calls compute_top_songs and passes the output to compute_top_songs_theory 
    # stores the output of compute_top_songs_theory in a dictionary
    # loop through the dictionary and format a string ("Your top songs have an average tempo of ...,  your most common key(s) is/are … "). Inside the loop, there should an if/else to check if the length of the length of the value is greater than 1 (there was a tie). If there a tie is found, the string should use the “are” word instead of “is.” The noun should also be plural instead of singular. 
    # Return string 
print()
