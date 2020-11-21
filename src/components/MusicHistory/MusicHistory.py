#from MusicTheory.py import get_all_musictheory
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
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

###############################
##### COMPUTATION METHODS #####
###############################
def compute_genre(self, time_range, limit, discord_user):
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
    genre_dict = {}

    # Create a genre_dictionary to store the potential top genres 
    # Check that if limit is less than or equal to 5. Else, set limit equal to 5.
    # Calls getAccessToken(discord username) from Spotify Auth class 
    # uses accessToken and Spotipy object and get user's top 20 artists in JSON 
    # parses through JSON to get the genres of the top 20 artists and stores in a dictionary (key = string representing genre name, value = int representing the “ranking” of the artist the genre is associated with)
    # Calls and returns compute_genre_helper method with genre_dictionary and limit as the parameter 

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
    # create a theory dictionary which will have the following keys. Each key will have a list as its value. 
        # Tempo
        # Time_signature
        # Key
        # Mode
        # Danceability
        # Acousticness
        # Energy
        # instrumentalness
    # loop through top_songIDs dictionary’s keys and calls get_all_music_theory method from the MusicTheory Class on each song ID. Get_all_music_theory returns a dictionary that we will parse through and append data into the values of our theory dictionary. 
    # Call and return compute_top_songs_theory_helper with theory dictionary as a parameter 


######################################
##### COMPUTATION HELPER METHODS #####
######################################
def compute_genre_helper(self, genre_dictionary, limit):
    """Returns theory data on a user's top songs over a given time range 
    :param genre_dictionary: 
    :type genre_dictionary: dictionary 

    :param limit: indicate how many artists to compute, defaults to 5. Minimum of 1, maximum of 10. 
    :type limit: int 

    :rtype: list
    :return: a queue of top genres sorted from most listened to genre to least listened to 
    """
    # output_genres = {}
    # count = 0
    # for key in genre_dictionary:


    # Create a queue that will store top genres
    # Loops through the keys of genres_dictionary and pushes the top genre (based on order of highest occurrence or mode) into queue. Continues to loop until the queue reaches the length limit. 
    # ties are broken based what genre is associated with the artist(s) that is listened to more
    # Returns a queue


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


#########################
##### REPLY METHODS #####
#########################
def reply_genre(self, time_range, limit, discord_user):
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
    # Add try and except block
    # calls compute_genre 
    # stores the output of compute_genre in a queue
    # loop through the queue and format a string ("Your top genres are ___")
    # Return string 
    
def reply_top_songs(self, time_range, limit, discord_user):
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
    # Add try and except block
    # calls compute_top_songs using the same parameters
    # stores the output of compute_top_songs in a dictionary
    # loop through the values of the dictionary and format a string ("Your top songs are ... ")
    # Return string 

def reply_top_artists(self, time_range, limit, discord_user):
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
    # Add try and except block
    # calls compute_top_arists using the same parameters 
    # stores the output of compute_top_artists in a queue
    # loop through the queue and format a string ("Your top artists are ... ")
    # Return string 

def reply_top_songs_theory(self, top_songIDs, discord_user):
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
    # Add try and except block
    # calls compute_top_songs and passes the output to compute_top_songs_theory 
    # stores the output of compute_top_songs_theory in a dictionary
    # loop through the dictionary and format a string ("Your top songs have an average tempo of ...,  your most common key(s) is/are … "). Inside the loop, there should an if/else to check if the length of the length of the value is greater than 1 (there was a tie). If there a tie is found, the string should use the “are” word instead of “is.” The noun should also be plural instead of singular. 
    # Return string 
