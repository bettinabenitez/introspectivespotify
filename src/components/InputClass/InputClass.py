import os
import sys
import discord
from discord.ext import commands
sys.path.append('../')

# from SpotifyAuth.SpotifyAuth import spotify_login
# from SpotifyAuth.SpotifyAuth import spotify_logout
# from SpotifyAuth.auth_test import test_all_auth
from MusicAnalytics.MusicTheory import reply_all_music_theory
from MusicAnalytics.MusicTheory import reply_get_tempo 
from MusicAnalytics.MusicTheory import reply_get_key 
from MusicAnalytics.MusicTheory import reply_get_time_signature
from MusicAnalytics.MusicTheory import reply_get_mode 
from MusicAnalytics.MusicTheory import reply_get_mood 
from MusicAnalytics.MusicTheory import reply_get_danceability 
from MusicAnalytics.MusicTheory import reply_get_acousticness
from MusicAnalytics.MusicTheory import reply_get_energy
from MusicAnalytics.MusicTheory import reply_get_instrumentalness 
from MusicAnalytics.MusicTheory import reply_compare_theory
from MusicAnalytics.MusicTheory import reply_suggest_theory
from MusicAnalytics.MusicHistory import reply_top_genres
from MusicAnalytics.MusicHistory import reply_top_songs_theory
from MusicAnalytics.MusicHistory import reply_top_songs
from MusicAnalytics.MusicHistory import reply_top_artists
from MusicAnalytics.MusicHistory import reply_top_songs_theory
# from SpotifyListen.SpotifyListen import add_song
# from SpotifyListen.SpotifyListen import play_party
# from SpotifyListen.SpotifyListen import pause_party
# from SpotifyListen.SpotifyListen import skip_party
# from SpotifyListen.SpotifyListen import rewind_party
# from SpotifyListen.SpotifyListen import display_queue
from SpotifyListen.SpotifyListen2 import add_song
from SpotifyListen.SpotifyListen2 import play_party
from SpotifyListen.SpotifyListen2 import pause_party
from SpotifyListen.SpotifyListen2 import skip_party
from SpotifyListen.SpotifyListen2 import rewind_party
from SpotifyListen.SpotifyListen2 import display_queue
from SpotifyListen.SpotifyListen2 import start_listening_party
from SpotifyListen.SpotifyListen2 import delete_playlist
# import MusicHistory

class InputClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ##### SPOTIFY AUTH COMMANDS ##### 
    @commands.command()
    async def login(self, ctx):
        user = ctx.author
        response = await spotify_login(self.bot, user)
        await user.send(response)
        
    @commands.command()
    async def logout(self, ctx):
        user = ctx.author
        response = spotify_logout(user)
        await user.send(response)

    ##### MUSIC THEORY COMMANDS ##### 
    @commands.command()
    async def musictheory(self, ctx, song):
        reply = reply_all_music_theory(song)
        await ctx.send(reply)
    
    @commands.command()
    async def tempo(self, ctx, song):
        reply = reply_get_tempo(song)
        await ctx.send(reply)
    
    @commands.command()
    async def key(self, ctx, song):
        reply = reply_get_key(song)
        await ctx.send(reply)

    @commands.command()
    async def timesignature(self, ctx, song):
        reply = reply_get_time_signature(song)
        await ctx.send(reply)
    
    @commands.command()
    async def mode(self, ctx, song):
        reply = reply_get_mode(song)
        await ctx.send(reply)

    @commands.command()
    async def mood(self, ctx, song):
        reply = reply_get_mood(song)
        await ctx.send(reply)
    
    @commands.command()
    async def danceability(self, ctx, song):
        reply = reply_get_danceability(song)
        await ctx.send(reply)

    @commands.command()
    async def acousticness(self, ctx, song):
        reply = reply_get_acousticness(song)
        await ctx.send(reply)
    
    @commands.command()
    async def energy(self, ctx, song):
        reply = reply_get_energy(song)
        await ctx.send(reply)

    @commands.command()
    async def instrumentalness(self, ctx, song):
        reply = reply_get_instrumentalness(song)
        await ctx.send(reply)
    
    @commands.command()
    async def compare(self, ctx, song_a, song_b):
        reply = reply_compare_theory(song_a, song_b)
        await ctx.send(reply)

    @commands.command()
    async def suggest(self, ctx, song_a, song_b):
        reply = reply_suggest_theory(song_a, song_b)
        await ctx.send(reply)

    ##### MUSIC HISTORY COMMANDS #####
    @commands.command()
    async def topgenres(self, ctx, *args):
        user = ctx.author
        
        # set default values 
        time_range = "medium_term"
        limit = 5

        # check if user specified a time_range and/or limit
        if len(args) > 0:
            for arg in args:
                if arg == "medium" or arg == "medium_term" or arg == "m":
                    time_range = "medium_term"
                elif arg == "long" or arg == "long_term" or arg == "l":
                    time_range = "long_term"
                elif arg == "short" or arg == "short_term" or arg == "s":
                    time_range = "short_term"
                elif arg.isdigit() or arg[1:].isdigit():
                    limit = int(arg)
        
        # handle limit out of bounds 
        if limit <= 0:
            reply = "Try asking for at least 1 top genre :)"
        else:
            if limit > 10:
                limit = 10
            
            # If a runtime error occurs, send a short sorry message to the user.
            try:
                reply = reply_top_genres(time_range, limit)
            except RuntimeError:
                reply = "Uh oh! We couldn't get your top genres. Sorry about that :( We'll try to fix this issue ASAP"
        
        await ctx.send(reply)

    @commands.command()
    async def topsongs(self, ctx, *args):
        user = ctx.author

        # set default values 
        time_range = "medium_term"
        limit = 5

        # check if user specified a time_range and/or limit
        if len(args) > 0:
            for arg in args:
                if arg == "medium" or arg == "medium_term" or arg == "m":
                    time_range = "medium_term"
                elif arg == "long" or arg == "long_term" or arg == "l":
                    time_range = "long_term"
                elif arg == "short" or arg == "short_term" or arg == "s":
                    time_range = "short_term"
                elif arg.isdigit() or arg[1:].isdigit():
                    limit = int(arg)
        
        # handle limit out of bounds 
        if limit <= 0:
            reply = "Try asking for at least 1 top song :)"
        else:
            if limit > 10:
                limit = 10

            # If a runtime error occurs, send a short sorry message to the user.
            try:
                reply = reply_top_songs(time_range, limit)
            except RuntimeError:
                reply = "Uh oh! We couldn't get your top songs. Sorry about that :( We'll try to fix this issue ASAP"
            
        await ctx.send(reply)

    @commands.command()
    async def topartists(self, ctx, *args):
        user = ctx.author

        # set default values 
        time_range = "medium_term"
        limit = 5

        # check if user specified a time_range and/or limit
        if len(args) > 0:
            for arg in args:
                if arg == "medium" or arg == "medium_term" or arg == "m":
                    time_range = "medium_term"
                elif arg == "long" or arg == "long_term" or arg == "l":
                    time_range = "long_term"
                elif arg == "short" or arg == "short_term" or arg == "s":
                    time_range = "short_term"
                elif arg.isdigit() or arg[1:].isdigit():
                    limit = int(arg)
        
        # handle limit out of bounds 
        if limit <= 0:
            reply = "Try asking for at least 1 top artist :)"
        else:
            if limit > 10:
                limit = 10

            # If a runtime error occurs, send a short sorry message to the user.
            try:
                reply = reply_top_artists(time_range, limit)
            except RuntimeError:
                reply = "Uh oh! We couldn't get your top artists. Sorry about that :( We'll try to fix this issue ASAP"
            
        await ctx.send(reply)

    @commands.command()
    async def topsongstheory(self, ctx, *args):
        user = ctx.author
        
        # set default values 
        time_range = "medium_term"
        limit = 5

        # check if user specified a time_range and/or limit        
        if len(args) > 0:
            for arg in args:
                if arg == "medium" or arg == "medium_term" or arg == "m":
                    time_range = "medium_term"
                elif arg == "long" or arg == "long_term" or arg == "l":
                    time_range = "long_term"
                elif arg == "short" or arg == "short_term" or arg == "s":
                    time_range = "short_term"
                elif arg.isdigit() or arg[1:].isdigit():
                    limit = int(arg)
        
        # handle limit out of bounds 
        if limit <= 0:
            reply = "Try asking for at least 1 top song's theory data :)"
        else:
            if limit > 10:
                limit = 10

            # If a runtime error occurs, send a short sorry message to the user.
            try:
                reply = reply_top_songs_theory(time_range, limit)
            except RuntimeError:
                reply = "Uh oh! We couldn't get your top artists. Sorry about that :( We'll try to fix this issue ASAP"

        await ctx.send(reply)
        
    @commands.command()
    async def testAuth(self, ctx):
        user = ctx.author
        await test_all_auth(self.bot, user)

    # @commands.command()
    # async def addSong(self, ctx, *, arg):
    #     reply = add_song(arg)
    #     await ctx.send(reply)

    # @commands.command()
    # async def play(self, ctx):
    #     reply = play_party()
    #     await ctx.send(reply)
    
    # @commands.command()
    # async def pause(self, ctx):
    #     reply = pause_party()
    #     await ctx.send(reply)

    # @commands.command()
    # async def skip(self, ctx):
    #     user = ctx.author.name
    #     reply = skip_party(user)
    #     await ctx.send(reply)

    # @commands.command()
    # async def rewind(self, ctx):
    #     user = ctx.author.name
    #     reply = rewind_party(user)
    #     await ctx.send(reply)

    # @commands.command()
    # async def display(self, ctx):
    #     #user = ctx.author.name
    #     reply = display_queue()
    #     await ctx.send(reply)

    ####### new spotify listening commands here #######
    # TO DO: test start with and without arg
    @commands.command()
    async def start(self, ctx, *, arg):
        print(arg)
        reply = start_listening_party(arg)
        await ctx.send(reply)

    @commands.command()
    async def delete(self, ctx):
        reply = delete_playlist()
        await ctx.send(reply)


def setup(bot):
    bot.add_cog(InputClass(bot))