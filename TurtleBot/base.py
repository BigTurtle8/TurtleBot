import os
import random as r
from dotenv import load_dotenv
from TurtleBot.functions import *
import json
import asyncio
import aiohttp
import time
import math

# 1
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# 2
bot = commands.Bot(command_prefix='tur ')

# IMPORTANT --- "Avatar" is the term for profile pic.
# Setting variables.
baseDir = os.path.dirname(__file__)
with open(os.path.join(baseDir, 'info.json'), 'r') as f:
    info = json.load(f)
    toDoList = info['toDoList']
    economy = info['economy']
    games = info['games']


# Base Json import
def input_json():
    info['toDoList'] = toDoList
    info['economy'] = economy
    info['games'] = games
    with open(os.path.join(baseDir, 'info.json'), 'w') as f:
        f.write(json.dumps(info, indent=3))
