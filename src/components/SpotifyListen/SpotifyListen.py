## Introspecitive Spotify
## Spotify Listen
##
##
##
##


import spotipy
import psycopg2
import random
import time

"""
Public Instance Variables
"""

"""
Private Instance Variables
"""
#sp = spotipy.Spotify()?sp = spotipy.Spotify(auth_manager=auth_manager)auth_manager = SpotifyClientCredentials()
#current_song
#current_position


async def getCurrentSong(self):
    """
    Accessor method that gets the current song playing by the listening party. 
    Returns the current song instance variable

    Returns:
        string: Name of the current song being played in the listening party

    """

async def setCurrentSong(self):
    """
    Mutator method that sets the current song playing by the listening party. 
    When called, the function uses the spotipy object to find the current song of the users in the listening party and 
    set's the current song and current position of that song to the private instance variables: current_song and current_position


    """


async def getQueue(self):
    """
    Acessor method that gets songs added in the listening party’s queue with the current song as the first item of the list. 
    This is done by selecting the songs from the list on the song database that are currently on the list of being played.

    
    Returns:
        list: track songs of songs currently on the listening party’s queue
    """

async def displayQueue(self):
    """
    Displays songs added in the listening party’s queue with the current song as the first item of the list. 
    This is done by calling the getQueue function then using discord API to send a message on the discord channel.

    """



async def join(self, user):
    """
    Adds user to the listening party.
    This is done by calling getAccessToken(discord username) from Spotify Auth class, where discord username is taken from the user argurment of this function,
    and user is then added to the database of list of users that are part of the listening party.
    This function will then use the setCurrentSong function and use current_song and current_position to play that track and position for the new user in order to synchronise the users with the rest of the party.

    Args:
        user (int): discord userid

    """



async def leave(self, user):
    """
    Removes users from the listening party:
    This is done by using the spotipy object to pause the song on the user's spotify account.
    The user is then removed from the database of list of users on the listening party

    Args:
        user (int): discord userid

    """



async def play(self):
    """
    Plays the playback for all users in the listening party.
    This is done by using the spotipy object to play the song on the user's playback.
    Note: If the song on the user is currently playing, this function will not run. 

    """


async def pause(self):
    """
    Pauses the playback for all users in the listening party.
    This is done by using the spotipy object to pause the song on the user's playback.
    Note: If the song on the user is currently paused, this function will not run.

    """


async def skip(self, user):
    """
    Skips the playback for all users in the listening party.
    This is done by selecting the song on the queue from the database that is next on the queue being played
    then using the spotify object to play that song for all the users

    """


async def rewind(self, user):
    """
    Rewinds the playback for all users in the listening party.
    This is done by selecting the song on the queue from the database prior to song currently being played 
    then using the spotipy object to play that song for all the users

    """

async def shuffle(self, user):
    """
    Shuffles the playback for all users in the listening party.
    This is done on the database by selecting all the songs that still need to be played
    and shuffling the order that it is to be played

    """


async def add(self, song):
    """
    Adds a song to the playback for all users in the listening party.
    This is done by using the spotipy object to get the track id of the song 
    then adding the trackid, name, and position in queue to the database.

    Args:
        song (string): name of the song

    """


async def remove(self, song):
    """
    removes a song to the playback for all users in the listening party.
    This is done by selecting the songs from the database and deleting it from the list queue. 
    Note: By removing a song the song will not be added if a playlist is created

    Args:
        song (string): name of the song

    """


async def createPlaylist(self, user):
    """
    Creates a playlist with the all the songs played during the listening party. 
    This is done by: 
    Using the spotipy object to create a playlist on the user's account.
    The songs will be taken from the songs saved on the databases 

    Args:
        user (int): discord userid

    Returns:
        string: link to the created playlist

    """

async def listeningParty():
