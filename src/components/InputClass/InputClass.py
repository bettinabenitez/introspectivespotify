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


# import MusicHistory

class InputClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @commands.command()
    async def genre(self, ctx):
        user = ctx.author
        # return MusicHistory.compute_genre(user)

    @commands.command()
    async def test(self, ctx):
        user = ctx.author
        reply = reply_top_songs_theory('long_term', 5)
        await user.send(reply)

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
        

def setup(bot):
    bot.add_cog(InputClass(bot))