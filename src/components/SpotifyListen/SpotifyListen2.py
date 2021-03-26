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

# TODO: figure out why strings dont fucking work
info = []  # info[0] = spotify user, info[1] = playlist_id
total_number_songs = 0
listening_party = False
queue = []

### TODO: update for all the other thigs whe we merge
scope = "user-read-recently-played, user-top-read, user-read-playback-position, user-read-playback-state, user-modify-playback-state, user-read-currently-playing, playlist-modify-public, user-read-private, playlist-modify-private, playlist-read-private, playlist-read-collaborative"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope, cache_path=".oAuthCache"))

##### new design idea - make playlist for each listening party #####

## methods that need to change
# start listening party --- needs to make a playlist + start playing it? 
# addSong --- needs to add song to playlist (not to user's queue)
# remove song --- playlist_remove_all_occurrences_of_items or playlist_remove_specific_occurrences_of_items
# displayQueue --- call getQueue and format 
# getQueue ---
    # call playlist_tracks from Spotipy and loop through the output to get ID, name, and artist(s) 
    # look at recently played
# shuffle ---
    # can we change all of the songs in playlist? yes we can!
    # Or we can take off all the items after our current song and readd them in a diff order

## methods that can stay the same
# getCurrentSong 
# skip 
# play/pause 

## lingering questions
# do we still need to keep track of the queue in a list? or can we just let spotify handle it?
    # answer: maybe don't need to keep track. we can get the queue by getting current song + comparing to tracks in playlist
    # depends on if we want our queue to automatically store name, artist, ID
    

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

def rewind_party(user):
    """
    rewind to previous song on the queue
    void

    Rewinds the playback for all users in the listening party.
    This is done by selecting the song on the queue from the database prior to song currently being played 
    then using the spotipy object to play that song for all the users

    TODO: fix comments

    """

            
    return user + " rewinded song to previous song"

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
    
    # Iterate through the results specifically for tracks in items
    # grab track id, name, and artist(s) and add to our queue
    for item in results['tracks']['items']:     
        trackID = item['id']
        trackName = item['name']
        trackArtist = item['artists'][0]['name']
        for artist_index in range(1, len(item['artists'])):
            trackArtist = trackArtist + ", " + item['artists'][artist_index]['name']
    queue.append((trackID, trackName, trackArtist))

    # get songs in playlist (before adding song to playlist)
    playlist_items = sp.playlist_items(info[1], fields=None, limit=100, offset=0, market=None, additional_types=('track', 'episode'))

    # add song to Spotify playlist. pass in playlist_id, list of song id
    sp.playlist_add_items(info[1], [trackID], position=None)

    # find device to play on
    # TO DO: need to add try and except in case no active devices are found. 
    id_found = ""
    devices = sp.devices()
    print(f"devices are here: {sp.devices()}")
    for device in devices['devices']:
        print(device)
        print(".....")
        if device['is_active'] == True:
            id_found = device['id']
            break

    # check if playlist was empty before adding current song. if so, play playlist 
    if playlist_items['total'] == 0:
        sp.start_playback(device_id = id_found, context_uri="spotify:playlist:" + info[1])

    return trackName + " by " + trackArtist + " was added to the queue"

def remove(self, song, listening_party_id):
    """
    remove a song from our queue (just the first time we see it)

    removes a song to the playback for all users in the listening party.
    This is done by selecting the song from the database either from direct quote or song name and deleting it from the database. 
    Decrement all the positions of the songs after the deleted song by 1
    Decrement the total_number_songs variable by 1
    Note: By removing a song the song will not be added if a playlist is created
    If there are no songs on in the queue at all, then nothing is run

    Args:
        song (string): name of the song

    """

    results = sp.search(q= song, type="track", limit=1)

    # Iterate through the results specifically for tracks in items and grab

    for item in results['tracks']['items']:      
        trackID = item['id']
    
    if trackID not in q:
        return song + "not in queue"
    
    q = q.remove(trackID)
    return song + "was removed from queue"

def getUserID():
    return sp.current_user()['id']

def start_listening_party(playlist_name):
    """
    start the listening party
    create a playlist + start playing the playlist?
    
    """
    # store user ID
    info.append(getUserID())
    
    # create a playlist and store playlist ID 
    playlist = sp.user_playlist_create(info[0], playlist_name, public=False, collaborative=False, description= "This playlist was made by Introspective Spotify!")
    info.append(playlist['id']) 

    # return link of spotify playlist
    playlist_link = playlist['external_urls']['spotify']
    return f"We created a playlist for you! Here is the link: {playlist_link}"


def delete_playlist():
    """
    """   
    # pass in spotify user and playlist id 
    sp.user_playlist_unfollow(info[0], info[1])
    
    return "we deleted the playlist for the listening party"


###############################################################
# functions to implement later below!

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