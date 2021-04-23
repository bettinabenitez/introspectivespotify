import random
import time
import os
import spotipy
import discord
from spotipy.oauth2 import SpotifyOAuth
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")


# current_song = ""
# current_pos = 0
users = []
total_number_songs = 0
listening_party = False
queue = []


scope = "user-read-recently-played, user-top-read, user-read-playback-position, user-read-playback-state, user-modify-playback-state, user-read-currently-playing, playlist-modify-public, playlist-modify-private, user-read-private, playlist-read-private, playlist-read-collaborative, ugc-image-upload"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope, cache_path=".oAuthCache"))

##### new design idea - make playlist for each listening party #####

## methods that need to change
# start listening party --- needs to make a playlist + start playing it? 
# addSong --- needs to add song to playlist (not to user's queue)
# remove song --- playlist_remove_all_occurrences_of_items or playlist_remove_specific_occurrences_of_items
# displayQueue --- call getQueue and format 
# getQueue --- call playlist_tracks from Spotipy and loop through the output to get ID, name, and artist(s) 
# shuffle ---
    # can we change order of songs in playlist? yes we can!
    # Or we can take off all the items after our current song and readd them in a diff order

## methods that can stay the same
# getCurrentSong 
# skip 
# play/pause 

## lingering questions
# do we still need to keep track of the queue in a list? or can we just let spotify handle it?
    # answer: maybe don't need to keep track. we can get the queue by getting current song + comparing to tracks in playlist


def getCurrentSong():
    """
    returns the current song the listening party is listening to 

    Accessor method that gets the current song playing by the listening party. 
    Call setCurrentSong() to get the most updated song that the users are listening to


    Returns:
        string: Name of the current song being played in the listening party

        TODO: fix comments

    """
    current_song = ""
    current_pos = 0
    
    # get info about user's current song 
    results = sp.current_user_playing_track()

    trackID = results['item']['id']

    if trackID != "": # check if there is a song playing
        current_song = trackID
        current_pos = results['progress_ms']

    # print(f"Current position: {current_pos}")
    return (current_song, current_pos)

def setCurrentSong():
    """
    Mutator method that sets the current song playing by the listening party. 
    When called, the function uses the Spotipy object to find the current song of the users in the listening party and set's the current song and current position of that song to the private instance variables: current_song and current_position
    This can be done by checking the first user’s current song and song position since everyone on the list should have the same song and position.

    """
    
        
def getQueue(spotify_id):
    """
    get queue that we have stored (not spotify user's queue)
    returns a list

    Acessor method that gets songs added in the listening party’s queue with the current song as the first item of the list. 
    This is done by selecting the songs from the list on the song database that are currently on the list of being played.

    
    Returns:
        list: track songs of songs currently on the listening party’s queue


    TODO: fix comments is this needed?
    """
    return queue

def display_queue():
    """
    show users what the queue is 
    returns a string 

    Displays songs added in the listening party’s queue with the current song as the first item of the list. 
    This is done by calling the getQueue function then using discord API to send a message on the discord channel.

    TODO: just do this lmao
    """

    songs = f"1. {queue[0][1]} by {queue[0][2]} \n"

    print(queue)
    for i in range(1, len(queue)):
        songs = songs + f"{i+1}. {queue[i][1]} by {queue[i][2]} \n"

    return "Your songs in the queue are: \n \n" + songs

    # THIS IS REFERENCE FROM ADD

    #results = sp.search(q= song, type="track", limit=1)

    # Iterate through the results specifically for tracks in items and grab

    # for item in results['tracks']['items']:      
    #     trackID = item['id']
    
    # q = q.append(trackID)
    # return song + "was added to the queue"

# def join(self, user):
#     """
#     Adds user to the listening party.
#     This is done by calling getAccessToken(discord username) from Spotify Auth class, where discord username is taken from the user argurment of this function,
#     and user is then added to the database of list of users that are part of the listening party.
#     This function will then use the setCurrentSong function and use current_song and current_position to play that track and position for the new user in order to synchronise the users with the rest of the party.

#     Args:
#         user: discord user object  

#     """
#     if not listening_party:
#         listening_party = True
#         listeningParty()

#     if users[user.id] is None:
#         users[user.id] = user
#         # make user's current song be the listening party's current song at current position
#         return user.name + " joined the listening party!"

#     return user.name + " is already in the listening party!"

# def leave(self, user):
#     """
#     Removes users from the listening party:
#     This is done by using the spotipy object to pause the song on the user's spotify account.
#     The user is then removed from the database of list of users on the listening party

#     Args:
#         user: discord user object  

#     """

#     if users[user.id] is None:
#         return user.name + " is not in the listening party!"
    
#     del users[user.id]

#     if len(users) == 0:
#         listening_party = False
#         return user.name + " has left the listening party and the listening party is over. :("

#     return user.name + " has left the listening party."

def play_party():
    """
    adds a song to the user's Spotify queue and also to our queue 
    void

    Plays the playback for all users in the listening party.
    This is done by using the spotipy object to play the song on the user's playback.
    Note: If the song on the user is currently playing, this function will not run. 

    TODO: fix comments
          add play song?
    """
    sp.start_playback()

    return " Listening Party is playing"

def pause_party():
    """
    pauses Spotify user's Spotify 
    void 

    Pauses the playback for all users in the listening party.
    This is done by using the spotipy object to pause the song on the user's playback.
    Note: If the song on the user is currently paused, this function will not run.

    TODO: fix comments

    """

    sp.pause_playback()

    return "Listening Party is paused"

def skip_party(user):
    """
    skips the current song 
    void

    Skips the playback for all users in the listening party.
    This is done by selecting the song on the queue from the database that is next on the queue being played
    then using the spotify object to play that song for all the users

    """

    sp.next_track()

    return user + " skipped to the next track"
    # call current song
    # find where current song is in the queue (searching from the end)
    # call play on next song after the current song in the queue

def rewind_party(user):
    """
    rewind to previous song on the queue
    void

    Rewinds the playback for all users in the listening party.
    This is done by selecting the song on the queue from the database prior to song currently being played 
    then using the spotipy object to play that song for all the users

    TODO: fix comments

    """
    current_song = getCurrentSong()
    #print(f"queue is:: {queue} and length is {len(queue)}")

    # we have played over 5 seconds of the current song
    # rewind to beginning
    if current_song[1] >= 5000:  # 5 seconds
        sp.start_playback(uris=["spotify:track:" + current_song[0]])
        return user + " rewinded song to beginning"

    # we are at the beginning of the song. Rewind to previous song. 
    for i in range(len(queue)-1, 0, -1):
        # look for the index of our current song in our queue 
        # print(f"current song is: {current_song} and the song id is {queue[i]}")   

        if current_song[0] == queue[i][0]:   
        #if current_song[0] == queue[i]:
            # print("here in if: " + current_song)
            # play previous song in queue 

            prev_uri = "spotify:track:" + queue[i-1][0]
            #prev_uri = "spotify:track:" + queue[i-1]
            sp.start_playback(uris=[prev_uri])
            
    return user + " rewinded song to previous song"

    # call current song
    # find where current song is in the queue (searching from the end)
    # call play on previous song before the current song in the queue

# def shuffle(self, user):
#     """
#     Shuffles the playback for all users in the listening party.
#     This is done on the database by selecting all the songs that still need to be played and shuffling the order that it is to be played
#     Use the Fisher-Yates algorithm to shuffle songs on the playlist, which uses the random function from the random library to randomize the selection of songs.
#     Call queueManagement() method to ensure that the queue is correct
#     Get the position number of the first song after the current song
#     Create a random list of position numbers starting from the position retrieved and the number of songs (use rand() function from random library).
#     Call queueManagement() method to rearrange the queue to the new shuffled playlist.
#     If there are no songs on in the queue at all, then nothing is run

#     """

def add_song(song):
    """
    add it user's queue and to our own queue 
    void 

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

        TODO: fix comments

    """
    results = sp.search(q= song, type="track", limit=1)
    print(results)
    
    # Iterate through the results specifically for tracks in items
    # grab track id, name, and artist(s)
    for item in results['tracks']['items']:   
        #print(item)   
        trackID = item['id']
        trackName = item['name']
        trackArtist = item['artists'][0]['name']
        for artist_index in range(1, len(item['artists'])):
            trackArtist = trackArtist + ", " + item['artists'][artist_index]['name']
    

    ## IDEA: we should add trackName and Track artist too! As a 3 element tuple
    queue.append((trackID, trackName, trackArtist))
    #queue.append(trackID) # Adds to queue
    sp.add_to_queue(trackID)  
    #print(queue)
    return trackName + " by " + trackArtist + " was added to the queue"

# def remove(self, song, listening_party_id):
#     """
#     remove a song from our queue (just the first time we see it)

#     removes a song to the playback for all users in the listening party.
#     This is done by selecting the song from the database either from direct quote or song name and deleting it from the database. 
#     Decrement all the positions of the songs after the deleted song by 1
#     Decrement the total_number_songs variable by 1
#     Note: By removing a song the song will not be added if a playlist is created
#     If there are no songs on in the queue at all, then nothing is run

#     Args:
#         song (string): name of the song

#     """

#     results = sp.search(q= song, type="track", limit=1)

#     # Iterate through the results specifically for tracks in items and grab

#     for item in results['tracks']['items']:      
#         trackID = item['id']
    
#     if trackID not in q:
#         return song + "not in queue"
    
#     q = q.remove(trackID)
#     return song + "was removed from queue"

def createPlaylist(playlist_name):
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

    TODO: work on this !!!
    """
    # check if playlist_name was provided. if not, default 
    # if playlist_name == "":
        # playlist_name = "i like potatos"


    # user_playlist_create(user, name, public=True, collaborative=False, description='')
        # Creates a playlist for a user

        # Parameters:
        # user - the id of the user
        # name - the name of the playlist
        # public - is the created playlist public
        # collaborative - is the created playlist collaborative
        # description - the description of the playlist

    # tracks_to_add = []
    # for song in queue:
        # tracks_to_add.append(song[0])

    # playlist_add_items(playlist_id, tracks_to_add, position=None)

async def startListeningParty():
    """
    start the listening party
    
    
    Runs whenever the user list is not empty
    While the queue is not empty, run the commands below:
    Gets the total time length of getCurrentSong() using Spotipy object to find duration_ms of the song from the JSON data given when song searched using Spotify Web API search endpoint then store the integer to local variable
    Use time.sleep() until the current_position = total time length of song (local variable)
    Run skip() command

    """
    

