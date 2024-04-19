# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command(name="parse")
async def parse(ctx, args):
    print("$lasher")
    print(ctx)
    print(args)
    await ctx.send("Shut up")

client = discord.Client(intents=intents)
@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    # await bot.process_commands(message)
    print(message)
    print(message.author)
    print(message.type)




# client.run(TOKEN)
bot.run(TOKEN)