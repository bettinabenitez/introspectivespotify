import random
import time
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
load_dotenv()


"""
Public Instance Variables
"""

"""
Private Instance Variables
"""
current_song = ""
current_pos = ""
users = []
total_number_songs = 0

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
scope = "user-read-currently-playing, "
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope, cache_path=".oAuthCache"))

current_song = ""
current_position = ""


def getCurrentSong(self):
    """
    Accessor method that gets the current song playing by the listening party. 
    Call setCurrentSong() to get the most updated song that the users are listening to


    Returns:
        string: Name of the current song being played in the listening party

    """

    setCurrentSong = setCurrentSong()

    return current_song


def setCurrentSong(self):
    """
    Mutator method that sets the current song playing by the listening party. 
    When called, the function uses the Spotipy object to find the current song of the users in the listening party and set's the current song and current position of that song to the private instance variables: current_song and current_position
    This can be done by checking the first user’s current song and song position since everyone on the list should have the same song and position.



    """
    results = sp.current_user_playing_track()

    trackID = results['items']['id']
    if trackID != "":
        current_song = trackID
        
    


def getQueue(self):
    """
    Acessor method that gets songs added in the listening party’s queue with the current song as the first item of the list. 
    This is done by selecting the songs from the list on the song database that are currently on the list of being played.

    
    Returns:
        list: track songs of songs currently on the listening party’s queue
    """

def displayQueue(self):
    """
    Displays songs added in the listening party’s queue with the current song as the first item of the list. 
    This is done by calling the getQueue function then using discord API to send a message on the discord channel.

    """



def join(self, user):
    """
    Adds user to the listening party.
    This is done by calling getAccessToken(discord username) from Spotify Auth class, where discord username is taken from the user argurment of this function,
    and user is then added to the database of list of users that are part of the listening party.
    This function will then use the setCurrentSong function and use current_song and current_position to play that track and position for the new user in order to synchronise the users with the rest of the party.

    Args:
        user (int): discord userid

    """



def leave(self, user):
    """
    Removes users from the listening party:
    This is done by using the spotipy object to pause the song on the user's spotify account.
    The user is then removed from the database of list of users on the listening party

    Args:
        user (int): discord userid

    """



def play(self):
    """
    Plays the playback for all users in the listening party.
    This is done by using the spotipy object to play the song on the user's playback.
    Note: If the song on the user is currently playing, this function will not run. 

    """


def pause(self):
    """
    Pauses the playback for all users in the listening party.
    This is done by using the spotipy object to pause the song on the user's playback.
    Note: If the song on the user is currently paused, this function will not run.

    """


def skip(self, user):
    """
    Skips the playback for all users in the listening party.
    This is done by selecting the song on the queue from the database that is next on the queue being played
    then using the spotify object to play that song for all the users

    """


def rewind(self, user):
    """
    Rewinds the playback for all users in the listening party.
    This is done by selecting the song on the queue from the database prior to song currently being played 
    then using the spotipy object to play that song for all the users

    """

def shuffle(self, user):
    """
    Shuffles the playback for all users in the listening party.
    This is done on the database by selecting all the songs that still need to be played and shuffling the order that it is to be played
    Use the Fisher-Yates algorithm to shuffle songs on the playlist, which uses the random function from the random library to randomize the selection of songs.
    Call queueManagement() method to ensure that the queue is correct
    Get the position number of the first song after the current song
    Create a random list of position numbers starting from the position retrieved and the number of songs (use rand() function from random library).
    Call queueManagement() method to rearrange the queue to the new shuffled playlist.
    If there are no songs on in the queue at all, then nothing is run

    """


def add(self, song):
    """
    Adds a song to the playback for all users in the listening party.
    This is done by using the Spotipy object to search for the song.
    Parameters needed:
        Q: q=song%20 (any spaces must be separated by %20)
        Type: type=track
        Limit: limit=1 
    The response of the search is in JSON, and will return the songs that correspond with the song searched
    Therefore this method will parse through the JSON and retrieve the track id
    Increment total_number_songs variable by 1
    Then add the trackid, song name, and position in the queue (total number of songs), and status (2) to the database.
    The song variable will also be saved under the discord direct quote column.

    Args:
        song (string): name of the song

    """

    results = sp.search(q= song, type="track", limit=1)

    # Iterate through the results specifically for tracks in items and grab

    for item in results['tracks']['items']:      
        trackID = item['id']
        #add track id to queue
        




def remove(self, song):
    """
    removes a song to the playback for all users in the listening party.
    This is done by selecting the song from the database either from direct quote or song name and deleting it from the database. 
    Decrement all the positions of the songs after the deleted song by 1
    Decrement the total_number_songs variable by 1
    Note: By removing a song the song will not be added if a playlist is created
    If there are no songs on in the queue at all, then nothing is run

    Args:
        song (string): name of the song

    """


def createPlaylist(self, user):
    """
    Creates a playlist with all the songs played during the listening party. 
    This is done by: 
    Calling the getAccessToken(discord username) method from the OAuth class in order to allow access to each users’ Spotify accounts
    Using the Spotipy object to create a playlist on the user's account.
    The songs will be taken from the songs saved on the databases 
    If there are any duplicates in the song database, those must be removed before making the playlist. 
    Have a local variable that will store a list of the songs needed to add to the playlist without duplicates
    Name of the playlist will be “Introspective Spotify Listening Party”
    Add songs to the newly created playlist
    If there are no songs on in the queue at all, then nothing is run


    Args:
        user (int): discord userid

    Returns:
        string: link to the created playlist

    """

def listeningParty():
    """
    Runs whenever the user list is not empty\
    Set listeningParty to true
    While the queue is not empty, run the commands below:
    Gets the total time length of getCurrentSong() using Spotipy object to find duration_ms of the song from the JSON data given when song searched using Spotify Web API search endpoint then store the integer to local variable
    Use time.sleep() until the current_position = total time length of song (local variable)
    Run skip() command
    Sets listeningParty variable to false once the function is over (no users no songs in queue)

    """
    pass

def queueManagement():
    """
    Manages the songs stored on the database and checks whether the queue is correct 
    Goes through the song database per song
    Checks if the all the songs with a position on queue that is less than the position of the current song has status of 0, if not set that status to 0.
    When it gets to the current song on the database, check if the status is 1, if not change the status to 1. 
    Check if all songs after the current song have the status 2

    """
    pass

    
