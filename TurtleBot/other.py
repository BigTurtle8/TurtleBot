from TurtleBot.base import *


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'straw' in message.content.lower():
        await message.channel.send('Straw... Is that some sort of kelp?')

    await bot.process_commands(message)
