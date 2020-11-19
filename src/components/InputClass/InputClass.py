import os
import discord
from discord.ext import commands

# import SpotifyAuth

class InputClass(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def login(self, ctx):
        user = ctx.author
        # return SpotifyAuth.spotify_login(user)

    @commands.command()
    async def logout(self, ctx):
        user = ctx.author
        # return SpotifyAuth.spotify_login(user)

def setup(bot):
    bot.add_cog(InputClass(bot))