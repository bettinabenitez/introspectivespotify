#from MusicTheory.py import get_all_musictheory
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# TO DO create spotipy object here 

###############################
##### COMPUTATION METHODS #####
###############################
async def compute_genre(self, time_range, limit, discord_user):
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
    # Create a genre_dictionary to store the potential top genres 
    # Check that if limit is less than or equal to 5. Else, set limit equal to 5.
    # Calls getAccessToken(discord username) from Spotify Auth class 
    # uses accessToken and Spotipy object and get user's top 20 artists in JSON 
    # parses through JSON to get the genres of the top 20 artists and stores in a dictionary (key = string representing genre name, value = int representing the “ranking” of the artist the genre is associated with)
    # Calls and returns compute_genre_helper method with genre_dictionary and limit as the parameter 

async def compute_top_songs(self, time_range, limit, discord_user):
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
    # Parameters are the same as compute_top_genres
    # limit: an int that refers to the number of top songs the user wants to get with a minimum of 1 and a maximum of 10. If omitted, will default to the top  5 songs. If the limit given exceeds 10, limit will be set to 10.   
    # Description
    # Check that if limit is less than or equal to 10. Else, set limit equal to 10.
    # creates a dictionary that will store the names and IDs of the top songs. Keys will be IDs (string) and values will be song name (string). 
    # calls getAccessToken(discord username) from Spotify Auth class 
    # uses accessToken and Spotipy object and get user's top artists songs in JSON (uses limit parameter)
    # parses through JSON to get the top song’s name and ID. Adds top song’s name and ID to the dictionary
    # return the dictionary 
 

async def compute_top_artists(self, time_range, limit, discord_user):
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
    # Check that if limit is less than or equal to 10. Else, set limit equal to 10.
    # creates a queue that will store the top artists 
    # calls getAccessToken(discord username) from Spotify Auth class 
    # uses accessToken and Spotipy object and get user's top artists in JSON
    # parses through JSON to get the top artist’s name (string). Pushes top artist’s name into the queue. 
    # return the queue 

async def compute_top_songs_theory(self, top_songIDs, discord_user):
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
async def compute_genre_helper(self, genre_dictionary, limit):
    """Returns theory data on a user's top songs over a given time range 
    :param genre_dictionary: 
    :type genre_dictionary: dictionary 

    :param limit: indicate how many artists to compute, defaults to 5. Minimum of 1, maximum of 10. 
    :type limit: int 

    :rtype: list
    :return: a queue of top genres sorted from most listened to genre to least listened to 
    """
    # Create a queue that will store top genres
    # Loops through the keys of genres_dictionary and pushes the top genre (based on order of highest occurrence or mode) into queue. Continues to loop until the queue reaches the length limit. 
    # ties are broken based what genre is associated with the artist(s) that is listened to more
    # Returns a queue


async def compute_top_songs_theory_helper(self, theory_dictionary):
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
async def reply_genre(self, time_range, limit, discord_user):
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
    
async def reply_top_songs(self, time_range, limit, discord_user):
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

async def reply_top_artists(self, time_range, limit, discord_user):
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

async def reply_top_songs_theory(self, top_songIDs, discord_user):
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
