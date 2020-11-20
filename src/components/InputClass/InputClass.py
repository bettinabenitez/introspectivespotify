import os
import sys
import discord
from discord.ext import commands
sys.path.append('../')

from SpotifyAuth.SpotifyAuth import spotify_login

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
        

def setup(bot):
    bot.add_cog(InputClass(bot))