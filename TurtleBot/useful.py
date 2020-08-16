from TurtleBot.base import *


@bot.command(name='add_list', brief='Adds an object to your to do list.',
             description='Adds an object to your to do list, even with spaces.')
async def add_list(ctx, *, obj: str):
    # *, obj means that all other arguments are put into obj, 'consume rest'
    # https://discordpy.readthedocs.io/en/latest/faq.html?highlight=channel#why-do-my-arguments-require-quotes
    users = toDoList.keys()
    did_find = False
    for user in users:
        if user == str(ctx.author.id):
            did_find = True
        else:
            pass

    if did_find:
        toDoList[str(ctx.author.id)].append(obj)
    else:
        toDoList[str(ctx.author.id)] = [obj]

    await ctx.send(f'Added {obj} to {ctx.author.mention}\'s list.')

    input_json()


@bot.command(name='remove_list', help='Removes an object from your to do list by number.')
async def remove_list(ctx, number):
    try:
        num = int(number)
    except ValueError:
        await ctx.send('That\'s not a number!')
        return
    users = toDoList.keys()
    did_find = False
    for user in users:
        if user == str(ctx.author.id):
            did_find = True
        else:
            pass

    if not did_find:
        await ctx.send('You currently do not have a list. Change that by using \'!add_list\'!')
    else:
        try:
            test = toDoList[str(ctx.author.id)][num - 1]
        except IndexError:
            await ctx.send('You don\'t have an object in your list with that number!')
        else:
            await ctx.send(f'Removed object {num} from {ctx.author.mention}\'s list'
                           f', which had contents: {test}')
            del toDoList[str(ctx.author.id)][num - 1]
            input_json()


@bot.command(name='print_list', help='Prints your to do list.')
async def print_list(ctx):
    users = toDoList.keys()
    user_list = []
    did_find = False
    for user in users:
        if user == str(ctx.author.id):
            user_list = toDoList[user]
            did_find = True
            break
        else:
            pass

    if not did_find:
        await ctx.send('You do not have a list yet.')
    else:
        embed_var = discord.Embed(title='To Do List', description=f'{ctx.author.mention}\'s to do list!')
        for i, thing in enumerate(user_list):
            i += 1
            full_number = []
            for digit in str(i):
                discord_number = list_to_str([':', num_to_str[int(digit)], ':'])
                full_number.append(discord_number)
            embed_var.add_field(name=f'{list_to_str(full_number)}.', value=thing, inline=False)
        await ctx.send(embed=embed_var)
