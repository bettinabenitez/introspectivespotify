import os
import sys
import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import has_role
from discord.utils import get

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
from SpotifyListen.SpotifyListen2 import add_song
from SpotifyListen.SpotifyListen2 import play_party
# from SpotifyListen.SpotifyListen2 import pause_party
from SpotifyListen.SpotifyListen2 import skip_party
from SpotifyListen.SpotifyListen2 import rewind_party
from SpotifyListen.SpotifyListen2 import display_queue
from SpotifyListen.SpotifyListen2 import start_listening_party
from SpotifyListen.SpotifyListen2 import delete_playlist
from SpotifyListen.SpotifyListen2 import remove_song
from SpotifyListen.SpotifyListen2 import add_playlist
from SpotifyListen.SpotifyListen2 import reply_current_song
from Visualization.Visualization import personality_graphs
from Visualization.Visualization import cover_graph
from Visualization.Visualization import upload_cover
from Modeling.data_collection import song_add
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
    async def musictheory(self, ctx, *, arg):
        reply = reply_all_music_theory(arg)
        await ctx.send(reply)
    
    @commands.command()
    async def tempo(self, ctx, *, arg):
        reply = reply_get_tempo(arg)
        await ctx.send(reply)
    
    @commands.command()
    async def key(self, ctx, * , arg):
        reply = reply_get_key(arg)
        await ctx.send(reply)

    @commands.command()
    async def timesignature(self, ctx, * , arg):
        reply = reply_get_time_signature(arg)
        await ctx.send(reply)
    
    @commands.command()
    async def mode(self, ctx, * , arg):
        reply = reply_get_mode(arg)
        await ctx.send(reply)

    @commands.command()
    async def mood(self, ctx, *, arg):
        reply = reply_get_mood(arg)
        await ctx.send(reply)
    
    @commands.command()
    async def danceability(self, ctx, *, arg):
        reply = reply_get_danceability(arg)
        await ctx.send(reply)

    @commands.command()
    async def acousticness(self, ctx, *, arg):
        reply = reply_get_acousticness(arg)
        await ctx.send(reply)
    
    @commands.command()
    async def energy(self, ctx, *, arg):
        reply = reply_get_energy(arg)
        await ctx.send(reply)

    @commands.command()
    async def instrumentalness(self, ctx, *, arg):
        reply = reply_get_instrumentalness(arg)
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
    async def add(self, ctx, *, arg):
        if arg[:5] == 'https':
            reply = add_playlist(arg)
        else:
            reply = add_song(arg)
        await ctx.send(reply)

    @commands.command()
    async def play(self, ctx):
        reply = play_party()
        await ctx.send(reply)
    
    # @commands.command()
    # async def pause(self, ctx):
    #     reply = pause_party()
    #     await ctx.send(reply)

    @commands.command()
    async def skip(self, ctx):
        user = ctx.author.name
        reply = skip_party(user)
        await ctx.send(reply)

    @commands.command()
    async def rewind(self, ctx):
        user = ctx.author.name
        reply = rewind_party(user)
        await ctx.send(reply)

    @commands.command()
    async def display(self, ctx):
        #user = ctx.author.name
        reply = display_queue()
        await ctx.send(reply)

    ####### new spotify listening commands here #######
    @commands.command()
    async def start(self, ctx, *args):
        playlist_name = ""
        if not args:
            playlist_name = "Introspotty Playlist"
        else:
            for word in args:
                playlist_name += word + " "

        reply = start_listening_party(playlist_name)
        await ctx.send(reply)

    @commands.command()
    async def delete(self, ctx):
        reply = delete_playlist()
        await ctx.send(reply)

    @commands.command()
    async def remove(self, ctx, *args):       
        if len(args) > 1:
            nameOfSong = " ".join(args)
            reply = remove_song(nameOfSong)
        elif len(args) == 1:
            if args[0].isDigit():
                reply = remove_song_pos(args[0])
        else:
            nameOfSong = " ".join(args)
            reply = remove_song(nameOfSong)
    
        await ctx.send(reply)

    @commands.command()
    async def current(self, ctx):      
        reply = reply_current_song() 
        await ctx.send(reply)


    ####### Visualization Commands #######
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
            successful = personality_graphs(url, filename)
            if successful == None:
                await ctx.send("An unexpected error occurred :(")
                return
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
            if owner == None:
                await ctx.send("An unexpected error occurred :(")
                return
                
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


    ####### Modeling Commands #######
    @commands.command()
    async def cs181add(self, ctx, url, movie):
        user = ctx.author
        result = song_add(url, movie)
        await ctx.send(result)


    ####### Discord API Testing Commands #######\
    @commands.command(pass_context=True)
    # @has_role("Listening Party Member") < - HOW TO MAKE IT SO SPECIFIC ROLE CAN ONLY CALL CMNDS!! IMPORTANT
    async def role(self, ctx):
        member = ctx.message.author
        role_name = "Listening Party Member"

        # todo: CHECK IF THERES A LISTENING PARTY!!!

        # Get the roles of the guild 
        role = discord.utils.get(member.guild.roles, name=role_name)
        message = await ctx.send(f"Looks like a listening party has started here! Would you like to join?")
        reactions = ["✅"]
        # For the specific approved emojis, add an emoji to the bot's message
        for emoji in reactions: 
            await message.add_reaction(emoji)

        # Check that command calling author reacts to the bot's message with the specified emoji.
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅"] and reaction.message == message
                    
                
        # If the user reacts, check to make sure the user isn't already ranked as the role, 
        # otherwise, add the role and send a confirmation 
        try:
            confirmation = await self.bot.wait_for("reaction_add", check=check, timeout = 15)
            if confirmation:
                if role in ctx.author.roles: 
                    print("HI?")               
                    await ctx.send(f"{member.mention} Hey! You're already jamming out with us 💃 ")
                else:
                    await member.add_roles(role)
                    await ctx.send(f"I gave {member.mention} the role {role_name}, check out <#833213974627352637> to jam out")
        except asyncio.TimeoutError:
            await message.edit(content="You kept me on my toes! I timed out... 😴")


      
        

    @commands.command(pass_context=True)
    async def removerole(self, ctx):
        member = ctx.message.author
        role_name = "Listening Party Member"
        # Get the roles of the guild 
        role = discord.utils.get(member.guild.roles, name=role_name)
        await member.remove_roles(role)
        await ctx.send(f" {member.mention} I took away the role {role_name}, thanks for jamming with us!")
        

def setup(bot):
    bot.add_cog(InputClass(bot))
