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

info = []  # info[0] = spotify user, info[1] = playlist_id
total_number_songs = 0
listening_party = False
queue = []

### TODO: update for all the other thigs whe we merge
scope = "user-read-recently-played, user-top-read, user-read-playback-position, user-read-playback-state, user-modify-playback-state, user-read-currently-playing, playlist-modify-public, user-read-private, playlist-modify-private, playlist-read-private, playlist-read-collaborative"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope, cache_path=".oAuthCache"))

# TODO: figure out why strings dont fucking work!!!
# TODO: Assign people to roles/groups -> those roles and those people in the listening party this is instead of using the database DEVIKA WILL HELP
# TODO: Prepare for merge    
# TODO: what if you call any of the methods when listening party has not started yet? :(
## another idea: get everyone's spotify ID and play the playlist for everyone. SO pause can finally work :)

def getCurrentSong():
    """ gets information about listening party's current song 

    :rtype: tuple
    :returns: current song (string) and current position (int)
    """
    current_song = ""
    current_pos = 0
    
    # get user's current song's ID
    results = sp.current_user_playing_track()
    trackID = results['item']['id']

    # check if there is a song playing and set global variables
    if trackID != "": 
        current_song = trackID
        current_pos = results['progress_ms']

    return (current_song, current_pos)

def display_queue():
    """ Displays songs added in the listening party’s playlist with
    the current song as the first item 

    :rtype: string 
    :returns a formatted string describing the queue 
    """
    # pass in playlist_id
    queue = sp.playlist_items(playlist_id=info[1])


    output = "Your songs in the queue are: \n \n" 

    # Iterate through the results specifically for tracks in items
    # grab track id, name, and artist(s) and add to our queue
    counter = 1
    for item in queue['items']:
        # get song name and artist
        trackName = item['track']['name']
        trackArtist = item['track']['artists'][0]['name']

        # if song has multiple artists, add them to trackArtist
        for artist_index in range(1, len(item['track']['artists'])):
            trackArtist = trackArtist + ", " + item['track']['artists'][artist_index]['name']
        
        output += str(counter) + ". " + trackName + " by " + trackArtist + "\n"
        counter += 1

    # TODO: finish this method (only display songs in the queue, not whole playlist)
    # helpful link?: https://github.com/spotify/web-api/issues/1288
    # "you can combine the Get Current Playback with Get Recently Played which will
    # give you the previous 50 tracks played (provided the user played at least 30
    # seconds of the track). If you combine that with Get Playlists Tracks, you
    # should be able to piece together what the active index is.
    
    return output


def play_party():
    """ plays Spotify user's Spotify 

    :rtype: string
    :returns a notification to user  

    TODO: add play song? what happens if you say play before start listening party? 
    """
    sp.start_playback()

    return "Listening Party is playing"


def pause_party():
    """ pauses Spotify user's Spotify 

    :rtype: string
    :returns a notification to user 

    TODO: currently only pauses for host. Need to fix by merging w William's branch
    """
    sp.pause_playback()

    return "Listening Party is paused (only for host)"


def skip_party(user):
    """ Skips the current song 
    
    :rtype: string
    :returns a notification to user 
    """
    sp.next_track()

    return user + " skipped to the next track"


def rewind_party(user):
    """ Rewinds to beginning of song OR previous song on the queue
    
    rtype: string
    returns a notification to user 
    """
    current_song = getCurrentSong()

    # rewind to beginning if we have played over 5 seconds of the current song
    if current_song[1] >= 5000:  # 5 seconds
        sp.seek_track(0)
        return user + " rewinded song to beginning"
    
    # rewind to previous song 
    sp.previous_track()
    return user + " rewinded song to previous song"


def add_song(song):
    """ add a song user's Spotify queue and to our own queue 
    :param song: name of the song
    :type song: string
    
    :rtype: string
    :returns a notification to user letting them know a song was added 
    or that no active device was found
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

    # find device to play on
    id_found = ""
    devices = sp.devices()
    for device in devices['devices']:

        # active device was found, so get device ID 
        if device['is_active'] == True:
            id_found = device['id']
            sp.shuffle(state = False, device_id=id_found)
            sp.repeat(state = "context", device_id=id_found)
            break
    
    # no device was found. Send error message to discord chat. 
    if id_found == "":
        return "No Device Found. Please check that one of your devices is active by playing a song."

    # add song to Spotify playlist. pass in playlist_id, list of song id
    sp.playlist_add_items(info[1], [trackID], position=None)

    # check if playlist was empty before adding current song. if so, play playlist 
    if playlist_items['total'] == 0:
        sp.start_playback(device_id = id_found, context_uri="spotify:playlist:" + info[1])

    return trackName + " by " + trackArtist + " was added to the queue"


def remove(song):
    """ removes a song from user's Spotify queue (the playlist)
    
    :param song: name of the song
    :type song: string
    
    # questions: remove all occurences or just one?  do we remove from our queue too? 
    """
    results = sp.search(q= song, type="track", limit=1)

    # Iterate through the results specifically for tracks in items and grab

    for item in results['tracks']['items']:      
        trackID = item['id']
    
    if trackID not in q:
        return song + "not in queue"
    
    # This the
    q = q.remove(trackID)
    return song + "was removed from queue"

    # TODO: write this method with new design
    # playlist_remove_specific_occurrences_of_items(playlist_id, items, snapshot_id=None)
        # Removes all occurrences of the given tracks from the given playlist
        # Parameters:
            # playlist_id - the id of the playlist
            # items - an array of objects containing Spotify URIs of the


def shuffle():
    """ Shuffles the listening party's playlist 

    :rtype: string
    :returns a notification to user saying we shuffled
    """
    # TODO: write this method 
    # reorder songs in playlist
    # Parameters:
        # playlist_id - the id of the playlist
        # range_start - the position of the first track to be reordered
        # range_length - optional the number of tracks to be reordered
        # (default: 1)
        # insert_before - the position where the tracks should be


def getUserID():
    """
    :rtype: string
    :returns user's spotify ID
    """
    return sp.current_user()['id']


def start_listening_party(playlist_name):
    """ Starts the listening party
    :param playlist_name: name of playlist
    :type song: string

    :rtype: string
    :returns a notification to user saying we started the listening party 
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
    """ Deletes the listening party's playlist

    :rtype: string
    :returns a notification to user saying we deleted the playlist
    """   
    # pass in spotify user and playlist id 
    sp.user_playlist_unfollow(info[0], info[1])
    
    return "We deleted the playlist for the listening party!"


###############################################################
# functions to implement later below!

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


# def getQueue():
#     """ get queue based on playlist
#     returns a list

#     Acessor method that gets songs added in the listening party’s queue with the current song as the first item of the list. 
#     This is done by selecting the songs from the list on the song database that are currently on the list of being played.

    
#     Returns:
#         list: track songs of songs currently on the listening party’s queue


#     TODO: fix comments is this needed?
#     """
#     return queue
