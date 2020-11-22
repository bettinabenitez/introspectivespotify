import os
import sys
import discord
from discord.ext import commands
sys.path.append('../')

from SpotifyAuth.SpotifyAuth import spotify_login
from MusicHistory.MusicHistory import reply_top_songs_theory
from MusicTheory.MusicTheory import reply_all_musictheory

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
        

def setup(bot):
    bot.add_cog(InputClass(bot))