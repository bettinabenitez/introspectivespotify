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

info = ["", "", ""]  # info[0] = spotify user, info[1] = playlist_id, info[2] = playlist_link
listening_party = [False]
queue = []
start_bot_message = "Looks like you haven't started a listening party. Run !start to get started ;)"

### TODO: update for all the other thigs whe we merge
scope = "user-read-recently-played, user-top-read, user-read-playback-position, user-read-playback-state, user-modify-playback-state, user-read-currently-playing, playlist-modify-public, playlist-modify-private, user-read-private, playlist-read-private, playlist-read-collaborative, ugc-image-upload"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope, cache_path=".oAuthCache"))

#################
# THINGS TO DO:
#################

## MUST FIX: things to fix about current implementation
# TODO: can't find song in addSong should return error message to user
# TODO: fix remove POSITION !!
# TODO: fix get current song in the input class

## MUST FIX/HAVE: ALL THE MERGE RELATED TASKS :OOOO
# TODO: do API calls for multiple users?
# TODO: get everyone's spotify ID and play the playlist for everyone. SO pause can finally work :)
# TODO: write join and leave
# TODO: write end listening party
# TODO: refactor here

## SHOULD HAVE: after we merge tasks
# TODO: refactor here again :( so much to refactor
# TODO: write shuffle

## SHOULD HAVE: functionality to add
# TODO: Assign people to roles/groups -> those roles and those people in the listening party this is instead of using the database DEVIKA WILL HELP

## NICE TO HAVE:
# TODO: vote to confirm removing
# TODO: EMOJI REPLIES

# def func(param_1: type, param_2: type):
#     """
#     [Function Description]
#     (Optional for any important information) NOTE:
    
#     Argument(s) 
#     -----------------------
#         param_1: [param_1 description] in [parameter type] format. Example (Optional Example Description): 
#                  [param_1 Example]
#                  (Optional) NOTE: 
#         param_2: [param_2 description] in [parameter type] format. Example (Optional Example Description): 
#                  [param_2 Example]
#                  (Optional) NOTE: 
    
#     Output
#     -----------------------
#     [Output] in [output type] format. Example:
#         [Example] 
#         (Optional) NOTE: 
#     """

def get_current_song():
    """ gets information about listening party's current song 

    Output
    -----------------------
    Current song info as dictionary. Example:
        {"trackID": "0124u1dnfl", "trackName": "pov", 
         "trackArtist": "Ariana Grande", 
         "duration": "14000", "currentPos": "12000"
         }
    """
    
    # get user's current song's ID
    results = sp.current_user_playing_track()

    trackID = results['item']['id']
    trackName = results['item']['name']
    trackArtist = results['item']['artists'][0]['name']
    duration = results['item']['duration_ms']
    currentPos = results['progress_ms']
    
    for artist_index in range(1, len(results['item']['artists'])):
        trackArtist = trackArtist + ", " + results['item']['artists'][artist_index]['name']

    print({"trackID": trackID, "trackName": trackName, 
            "trackArtist": trackArtist, 
            "duration": duration, "currentPos": currentPos})
    
    return {"trackID": trackID, "trackName": trackName, 
            "trackArtist": trackArtist, 
            "duration": duration, "currentPos": currentPos}

def reply_current_song():
    """
    formats a reply message containing current song for discord

    Output
    -----------------------
    "Your current song is {trackName} by {trackArtist}!" Example:
        "Your current song is pov by Ariana Grande!"
    """
    if not listening_party[0]:
        return start_bot_message

    songInfo = getCurrentSong() 
    trackName = songInfo["trackName"]
    trackArtist = songInfo["trackArtist"]
    return f"Your current song is {trackName} by {trackArtist}!"

def display_queue():
    """ Displays songs added in the listening party’s playlist with
    the current song as the first item 

    breaks ties by printing from earlier occurance of current song (earlier-optimal)

    :rtype: string 
    :returns a formatted string describing the queue 
    """
    if not listening_party[0]:
        return start_bot_message
        
    # pass in playlist_id
    queue = sp.playlist_items(playlist_id=info[1])

    output = []

    # Iterate through the results specifically for tracks in items
    # grab track id, name, and artist(s) and add to our queue
    counter = 1
    counter_prev = -1
    found = False 
    found_previous = False

    currentID = getCurrentSong()[0]
    lastSongs = sp.current_user_recently_played(limit=1, after=None, before=None)
    prevListenedTo = lastSongs['items'][0]['track']['name']

    curr_offer = 0
    old_offer = 0
    prevInPlaylist = ""

    for item in queue['items']:
        # get song name and artist
        trackID = item['track']['id']
        if (counter_prev) >= 0:
            prevInPlaylist = queue['items'][(counter_prev)]['track']['name']
        
        counter_prev += 1
                    
        # we found the current song in playlist 
        if currentID == trackID:

            # Checks if the previous in the playlist = the previous listened to only 
            if prevInPlaylist == prevListenedTo:
                curr_offer = 1

            # multiple current songs in playlist 
            if found == True:
                if curr_offer > old_offer:
                    output = []
                    old_offer = curr_offer
                    counter = 1
            found = True
           
        # add song and artist name to output
        if found == True:
            trackName = item['track']['name']
            trackArtist = item['track']['artists'][0]['name']

            # if song has multiple artists, add them to trackArtist
            for artist_index in range(1, len(item['track']['artists'])):
                trackArtist = trackArtist + ", " + item['track']['artists'][artist_index]['name']
            
            if counter == 1: # this if statement checks whether the first song is the one currently planning
                output.append(str(counter) + ". " + trackName + " by " + trackArtist + "  🎶NOW PLAYING🎶 \n")
            else:
                output.append(str(counter) + ". " + trackName + " by " + trackArtist + "\n")
                
            counter += 1
    
    output_string = ""
    
    for i in range(min(15, len(output))):
        output_string += output[i]
    
    if len(output) > 15:
        output_string += "Additional songs not displayed."
    
    return "Your songs in the queue are: \n \n" + output_string


def play_party():
    """ plays Spotify user's Spotify 

    :rtype: string
    :returns a notification to user  

    TODO: add play song? what happens if you say play before start listening party? 
    """
    if not listening_party[0]:
        return start_bot_message

    sp.start_playback()

    return "Listening Party is playing"


def skip_party(user):
    """ Skips the current song 
    
    :rtype: string
    :returns a notification to user 
    """
    if not listening_party[0]:
        return start_bot_message

    currentSong = getCurrentSong()
    song_duration = currentSong[3]-1
    sp.seek_track(song_duration)

    return user + " skipped to the next track"


def rewind_party(user):
    """ Rewinds to beginning of song OR previous song on the queue
    
    rtype: string
    returns a notification to user 
    """
    if not listening_party[0]:
        return start_bot_message
        
    current_song = getCurrentSong()

    # rewind to beginning if we have played over 5 seconds of the current song
    if current_song[1] >= 5000:  # 5 seconds
        sp.seek_track(0)
        return user + " rewinded song to beginning"
    
    # rewind to previous song 
    sp.previous_track()
    return user + " rewinded song to previous song"

def add_playlist(playlist_url):
    """
    """
    if not listening_party[0]:
        return start_bot_message

    # get songs in queue playlist (before adding new playlist songs to our playlist)
    playlist_items = sp.playlist_items(info[1], fields=None, limit=100, offset=0, market=None, additional_types=('track', 'episode'))

    id_found = check_device()
    if id_found == "":
        return "No Device Found. Please check that one of your devices is active by playing a song."
    
    try:
        results = sp.playlist(playlist_url)
    except SpotifyException:
        return "Invalid playlist link was given. Make sure you aren't passing in album, track, or podcast!"

    num_tracks = len(results['tracks']['items'])
    # For every item in the plalyist, grab track ID
    for item in results['tracks']['items']:
        song_id = item['track']['id']
        sp.playlist_add_items(info[1], [song_id], position=None)

    # ONLY RUNS IF WE JUST STARTED LISTENING PARTY. check if playlist was empty before adding current song. if so, play playlist 
    if playlist_items['total'] == 0:
        sp.start_playback(device_id = id_found, context_uri="spotify:playlist:" + info[1])
    
    return f"Added {num_tracks} songs from your playlist into the queue!"

def add_song(song):
    """ add a song user's Spotify queue and to our own queue 
    :param song: name of the song
    :type song: string
    
    :rtype: string
    :returns a notification to user letting them know a song was added 
    or that no active device was found
    """
    if not listening_party[0]:
        return start_bot_message

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
    id_found = check_device()
    
    # no device was found. Send error message to discord chat. 
    if id_found == "":
        return "No Device Found. Please check that one of your devices is active by playing a song."

    # add song to Spotify playlist. pass in playlist_id, list of song id
    sp.playlist_add_items(info[1], [trackID], position=None)

    # check if playlist was empty before adding current song. if so, play playlist 
    if playlist_items['total'] == 0:
        sp.start_playback(device_id = id_found, context_uri="spotify:playlist:" + info[1])

    return trackName + " by " + trackArtist + " was added to the queue"

def check_device():
    """ returns the device ID. if no ID is found, return empty string
    """
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
    return id_found
def remove_song_pos(position):
    """ removes a song at position
    """
    if not listening_party[0]:
        return start_bot_message

    delete = [{"uri":trackID, "positions":[position]}]
    sp.playlist_remove_specific_occurrences_of_items(info[1], delete, snapshot_id=None)


def remove_song(song):
    """ removes a song from user's Spotify queue (the playlist)
    
    :param song: name of the song
    :type song: string
    
    # questions: remove all occurences or just one?  do we remove from our queue too? 
    """
    if not listening_party[0]:
        return start_bot_message

    results = sp.search(q= song, type="track", limit=1)

    # Iterate through the results specifically for tracks in items and grab
    trackID = ""
    for item in results['tracks']['items']:      
        trackID = item['id']
        trackName = item['name']
        trackArtist = item['artists'][0]['name']
        for artist_index in range(1, len(item['artists'])):
            trackArtist = trackArtist + ", " + item['artists'][artist_index]['name']
    
    if trackID == "":
        return "We could not find your song in the Spotify database"
    
    queue = sp.playlist_items(playlist_id=info[1])
    counter = 0
    position = 0
    for item in queue['items']:
        curr_trackID = item['track']['id']
        if curr_trackID == trackID:
            position = counter
        counter += 1

    print(trackID, position)
    delete = [{"uri":trackID, "positions":[position]}]

    print(delete)
    sp.playlist_remove_specific_occurrences_of_items(info[1], delete, snapshot_id=None)

    return trackName + " by " + trackArtist + " was removed from queue"

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
    if listening_party[0]:
        return "You already have a listening party started! :D"

    # store user ID
    info[0] = getUserID()

    # create a playlist and store playlist ID 
    playlist = sp.user_playlist_create(info[0], playlist_name, public=False, collaborative=False, description= "This playlist was made by Introspective Spotify!")
    info[1] = playlist['id']

    listening_party[0] = True
    # return link of spotify playlist
    info[2] = playlist['external_urls']['spotify'] # playlist link
    return f"We created a playlist for you! Here is the link: {info[2]}"


def delete_playlist():
    """ Deletes the listening party's playlist

    :rtype: string
    :returns a notification to user saying we deleted the playlist
    """   
    # pass in spotify user and playlist id 
    sp.user_playlist_unfollow(info[0], info[1])

    listening_party[0] = False

    return f"Here's the link to the playlist: {info[2]} but we've removed it from your account. See you next time!"


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

# def pause_party():
#     """ pauses Spotify user's Spotify 

#     :rtype: string
#     :returns a notification to user 

#     TODO: currently only pauses for host. Need to fix by merging w William's branch
#     """
#     sp.pause_playback()

#     return "Listening Party is paused (only for host)"
