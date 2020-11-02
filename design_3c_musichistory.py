import Spotipy 
# Spotipy gives full access to all of the music data provided by the Spotify Web API
# use Spotipy library instead of calling Spotify API directly b
from spotipy.oauth2 import SpotifyClientCredentials

class MusicHistory(commands.Cog):
    # add a private instance variable
    # instance of the spotify class
    auth_manager = SpotifyClientCredentials() 
    sp = spotipy.Spotify(auth_manager=auth_manager) 

    async def compute_genre(self, time_range, limit, discord_user):
        # create a queue that will store top genres
        # calls getAccessToken(discord username) from Spotify Auth class 
        # uses accessToken and Spotipy object and get user's top 20 artists in JSON 
        # parses through JSON to get the genres of the top 20 artists
        # pushes the top genres (based on highest occurance) into queue.
        # ties are broken based what genre is associated with the artist(s) is the listened to more.
        # returns the queue
        pass
    async def compute_top_songs(self, time_range, limit, discord_user):
        # creates a queue that will store the top songs 
        # calls getAccessToken(discord username) from Spotify Auth class 
        # uses accessToken and Spotipy object and get user's top artists songs in JSON (uses limit parameter)
        # parses through JSON to get the top songs. Pushes top songs into the queue. 
        # return the queue 
        pass
    async def compute_top_artists(self, time_range, limit, discord_user):
        # creates a queue that will store the top artists 
        # calls getAccessToken(discord username) from Spotify Auth class 
        # uses accessToken and Spotipy object and get user's top artists in JSON (uses limit parameter)
        # parses through JSON to get the top artists. Pushes top artists into the queue. 
        # return the queue 
        pass
    async def compute_top_songs_theory(self, top_songIDs):
        # create a dictionary which will have the following keys:
        # key, mode, danecibility.... 
        # loop through the top_songIDs and calls methods from the 
        pass
        # https://discordjs.guide/popular-topics/collectors.html#message-collectors


    async def reply_genre(self, time_range, limit, discord_user):
        # calls compute_genre using the same parameters 
        # stores the output of reply_genre in a queue
        # loop through the queue and format a string ("Your top genres are ___")
        # use Discord API to respond in Discord chat 
        pass
    async def reply_top_songs(self, time_range, limit, discord_user):
        # calls compute_top_songs using the same parameters 
        # stores the output of reply_genre in a queue
        # loop through the queue and format a string ("Your top songs are ___")
        # use Discord API to respond in Discord chat 
        pass
    async def reply_top_artists(self, time_range, limit, discord_user):
        # calls compute_top_arists using the same parameters 
        # stores the output of reply_genre in a queue
        # loop through the queue and format a string ("Your top artists are ___")
        # use Discord API to respond in Discord chat 
        pass
    async def reply_top_songs_theory(self, top_songIDs):
        pass

