import os
import sys
import discord
from discord.ext import commands
sys.path.append('../')

from SpotifyAuth.SpotifyAuth import spotify_login
from MusicHistory.MusicHistory import reply_top_songs_theory
from MusicTheory.MusicTheory import reply_all_musictheory
from MusicTheory.MusicTheory import reply_get_tempo 
from MusicTheory.MusicTheory import reply_get_key 
from MusicTheory.MusicTheory import reply_get_time_signature
from MusicTheory.MusicTheory import reply_get_mode 
from MusicTheory.MusicTheory import reply_get_mood 
from MusicTheory.MusicTheory import reply_get_danceability 
from MusicTheory.MusicTheory import reply_get_acousticness
from MusicTheory.MusicTheory import reply_get_energy
from MusicTheory.MusicTheory import reply_get_instrumentalness 
from MusicTheory.MusicTheory import reply_compare_theory
from MusicTheory.MusicTheory import reply_suggest_theory
from MusicHistory.MusicHistory import reply_top_songs_theory
from MusicHistory.MusicHistory import reply_top_genres
from MusicHistory.MusicHistory import reply_top_songs
from MusicHistory.MusicHistory import reply_top_artists


# import MusicHistory

class InputClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ##### SPOTIFY AUTH COMMANDS ##### 
    @commands.command()
    async def login(self, ctx):
        user = ctx.author
        results = spotify_login(user)
        for idx, item in enumerate(results['items']):
            artist = item['name']
            await user.send(str(idx) + " " + artist)

    @commands.command()
    async def logout(self, ctx):
        user = ctx.author
        # return SpotifyAuth.spotify_login(user)

    ##### MUSIC THEORY COMMANDS ##### 
    @commands.command()
    async def musictheory(self, ctx, song):
        reply = reply_all_musictheory(song)
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
        time_range = "medium_term"
        limit = 5
        if len(args) > 0:
            for arg in args:
                if arg == "medium" or arg == "medium_term" or arg == "m":
                    time_range = "medium_term"
                elif arg == "long" or arg == "long_term" or arg == "l":
                    time_range = "long_term"
                elif arg == "short" or arg == "short_term" or arg == "s":
                    time_range = "short_term"
                elif arg.isdigit():
                    limit = int(arg)
        reply = reply_top_genres(time_range, limit)
        await user.send(reply)

    @commands.command()
    async def topsongs(self, ctx, *args):
        user = ctx.author
        time_range = "medium_term"
        limit = 5
        if len(args) > 0:
            for arg in args:
                if arg == "medium" or arg == "medium_term" or arg == "m":
                    time_range = "medium_term"
                elif arg == "long" or arg == "long_term" or arg == "l":
                    time_range = "long_term"
                elif arg == "short" or arg == "short_term" or arg == "s":
                    time_range = "short_term"
                elif arg.isdigit():
                    limit = int(arg)
        reply = reply_top_songs(time_range, limit)
        await user.send(reply)

    @commands.command()
    async def topartists(self, ctx, *args):
        user = ctx.author
        time_range = "medium_term"
        limit = 5
        if len(args) > 0:
            for arg in args:
                if arg == "medium" or arg == "medium_term" or arg == "m":
                    time_range = "medium_term"
                elif arg == "long" or arg == "long_term" or arg == "l":
                    time_range = "long_term"
                elif arg == "short" or arg == "short_term" or arg == "s":
                    time_range = "short_term"
                elif arg.isdigit():
                    limit = int(arg)
        reply = reply_top_artists(time_range, limit)
        await user.send(reply)

    @commands.command()
    async def topsongstheory(self, ctx, *args):
        user = ctx.author
        time_range = "medium_term"
        limit = 5
        if len(args) > 0:
            for arg in args:
                if arg == "medium" or arg == "medium_term" or arg == "m":
                    time_range = "medium_term"
                elif arg == "long" or arg == "long_term" or arg == "l":
                    time_range = "long_term"
                elif arg == "short" or arg == "short_term" or arg == "s":
                    time_range = "short_term"
                elif arg.isdigit():
                    limit = int(arg)
        reply = reply_top_songs_theory(time_range, limit)
        await user.send(reply)
        

def setup(bot):
    bot.add_cog(InputClass(bot))