from TurtleBot.base import *


timer_list = {}


def econ_check(id):
    users = economy.keys()
    did_find = False
    for user in users:
        if user == str(id):
            did_find = True
        else:
            pass

    if not did_find:
        economy[str(id)] = 0
        input_json()

    return id


@bot.command(name='bal', help='Shows your balance.')
async def bal(ctx):
    real_id = econ_check(ctx.author.id)

    description = f'**Balance**: {number_comma(economy[str(real_id)])} Seashells'
    embed_var = discord.Embed(description=description)
    embed_var.set_author(name=f'{ctx.author.display_name}\'s Collection', icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed_var)


@bot.command(name='work', help='Gains you some money.')
async def work(ctx):
    found = False
    for user in timer_list.keys():
        if user == str(ctx.author.id):
            found = True

    if found:
        if (elapsed_time := (timer_list[str(ctx.author.id)] + 60) - math.floor(time.monotonic())) >= 0:
            await ctx.send(f"You're still a bit tired. You still have to wait for "
                           f"`{elapsed_time} seconds` until you can work again!")
            return

    timer_list[str(ctx.author.id)] = math.floor(time.monotonic())

    real_id = econ_check(ctx.author.id)

    money = r.randrange(50, 150, 10)
    economy[str(real_id)] += money
    embed_var = discord.Embed(description=f'You were able to find {str(money)} seashells for your work.')
    embed_var.set_author(name=f'Good work {ctx.author.display_name}!', icon_url=ctx.author.avatar_url)

    await ctx.send(embed=embed_var)
    input_json()


@bot.command(name='gift', help='Gifts someone seashells.')
async def gift(ctx, recipient, money: int):
    real_id = econ_check(ctx.author.id)
    recip = discord.utils.get(ctx.guild.members, name=recipient)
    if not recip:
        recip = discord.utils.get(ctx.guild.members, display_name=recipient)
        if not recip:
            recip = discord.utils.get(ctx.guild.members, mention=recipient)
            if not recip:
                await ctx.send("That's not a person here.")
                return

    econ_check(recip.id)

    if economy[str(real_id)] < money:
        await ctx.send("You do not have enough seashells.")
        return

    economy[str(real_id)] -= money
    economy[str(recip.id)] += money

    embed_var = discord.Embed(description=f'{str(money)} seashells, just for you, {recip.display_name}!')
    embed_var.set_author(name=f'From {ctx.author.display_name}...', icon_url=ctx.author.avatar_url)
    embed_var.set_thumbnail(url=recip.avatar_url)

    await ctx.send(embed=embed_var)

    input_json()
