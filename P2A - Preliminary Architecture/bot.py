# bot.py
import os
import random
from dotenv import load_dotenv


from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


bot = commands.Bot(command_prefix='!')
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='Spotify', help='Pretends as if it were going to join your call, but it does not know how to right now.')
async def spotify_(ctx):
    spotify_commands = [
        'Let me listen to some spotify!:musical_keyboard: ',
        (
            ':musical_note: Dropping in! :musical_note:'
        ),
    ]

    response = random.choice(spotify_commands)
    await ctx.send(response)

bot.run(TOKEN)
