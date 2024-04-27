# bot.py
import os
import re
import discord
import json
from discord.ext import commands
from dotenv import load_dotenv
from scrapper import scrap_recipe
from git_helper import commit_file

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

f = open("whitelist.json")
data = json.load(f)
whitelist = data['whitelist']
categories = data['categories']
f.close()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

url_pattern=re.compile(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)")

@bot.command(name="parse")
async def parse(ctx, *args):
    print(ctx.author)
    print(whitelist)
    print(args)
    if str(ctx.author) in whitelist and len(args) > 0 and re.fullmatch(url_pattern, args[0]):
        print("valid url")
        if len(args) < 2 or args[1] not in categories:
            t = "Valid categories include:"
            for c in categories:
                t += "\n" + c
            await ctx.send(t)
        file = scrap_recipe(args)
        if file is not None:
            print(file)
            commit_file(file)
            await ctx.send("Parse recipe successfully")
        else:
            await ctx.send("Error Parsing Url")
    else:
        print("Invalid url")
        await ctx.send("Invalid Url")




bot.run(TOKEN)