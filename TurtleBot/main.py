from TurtleBot.base import *
from TurtleBot.useful import *
from TurtleBot.economy import *
from TurtleBot.games import *
from TurtleBot.other import *


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


bot.run(TOKEN)
