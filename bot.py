import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
intents.message_content = True  # Needed to receive messages
bot = commands.Bot(command_prefix='#', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} online')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
bot.run(token)
