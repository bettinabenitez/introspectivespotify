import os
import sys
import discord
import asyncio
from discord.ext import commands
sys.path.append('../')

from SpotifyAuth.SpotifyAuth import spotify_login
from SpotifyAuth.SpotifyAuth import spotify_logout
from SpotifyAuth.auth_test import test_all_auth
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
from Visualization.Visualization import personality_graphs
from Visualization.Visualization import cover_graph
from Visualization.Visualization import upload_cover

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
                reply = reply_top_genres(user, time_range, limit)
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
                reply = reply_top_songs(user, time_range, limit)
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
                reply = reply_top_artists(user, time_range, limit)
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
                reply = reply_top_songs_theory(user, time_range, limit)
            except RuntimeError:
                reply = "Uh oh! We couldn't get your top artists. Sorry about that :( We'll try to fix this issue ASAP"

        await ctx.send(reply)
        
    @commands.command()
    async def testAuth(self, ctx):
        user = ctx.author
        await test_all_auth(self.bot, user)

    @commands.command()
    async def personality(self, ctx, url):
        user = ctx.author

        # create filename using playlist url
        if url[:5] == 'https':
            filename = "personality_" + url[34:56] + ".jpg"
        elif url[:7] == 'spotify':  
            filename = "personality_" + url[17:] + ".jpg"
        else:
            await ctx.send("Please provide a valid playlist URL.")
            return
        
        async with ctx.typing():
            personality_graphs(url, filename)
            await ctx.send(file=discord.File(filename))

        os.remove(filename)

    @commands.command()
    async def cover(self, ctx, url):
        user = ctx.author

        # create filename using playlist url
        if url[:5] == 'https':
            filename = "cover_" + url[34:56] + ".jpg"
        elif url[:7] == 'spotify':  
            filename = "cover_" + url[17:] + ".jpg"
        else:
            await ctx.send("Please provide a valid playlist URL.")
            return

        async with ctx.typing():
            owner = cover_graph(url, user, filename)
            await ctx.send("Here is the cover art for your playlist!")
            await ctx.send(file=discord.File(filename))

            # if user owns the playlist, ask them if they want to update the playlist cover
            if owner:
                msg = await ctx.send("Would you like me to replace your current playlist cover with this masterpiece?\n" \
                                    "React with the 🖌 emoji to confirm.\n" \
                                    " \n"\
                                    " 🚨 !! Warning this will replace your current playlist cover !! 🚨\n ")
                reactions = ["🖌"]
                # For the specific approved emojis, add an emoji to the bot's message
                for emoji in reactions: 
                    await msg.add_reaction(emoji)

                # Check that command calling author reacts to the bot's message with the specified emoji.
                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ["🖌"] and reaction.message == msg
                
                # If the user reacts, upload the generated image as the new playlist image and send a confirmation. 
                # otherwise, if the bot times out after 15 seconds, send a timeout message and end. 
                try:
                    confirmation = await self.bot.wait_for("reaction_add", check=check, timeout = 15)
                    if confirmation:
                        rtn_msg = upload_cover(url, user, filename)
                        await msg.edit(content=rtn_msg)
                except asyncio.TimeoutError:
                    await msg.edit(content="You kept me on my toes! I timed out... 😴")

        # remove file
        os.remove(filename)

def setup(bot):
    bot.add_cog(InputClass(bot))