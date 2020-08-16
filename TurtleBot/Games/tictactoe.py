from TurtleBot.base import *


class TTTGame:
    def __init__(self, player):
        self.player = player
        self.first = False
        if r.random() >= 0.5:
            self.first = True

        self.map = [[':black_large_square:' for _ in range(3)] for _ in range(3)]

    async def wrong(self, ctx):
        await ctx.send("That is not the correct input. Please input a coord - ex: A1")

    async def display(self, ctx):
        msg = [[':three:'], [':two:'], [':one:'], [':blue_square:', ':a:', ':b:', ':regional_indicator_c:']]
        for row, areas in enumerate(self.map):
            for area in areas:
                msg[row].append(area)
            msg[row].append('\n')

        for row, areas in enumerate(msg):
            msg[row] = list_to_str(msg[row])

        embed_var = discord.Embed(description=list_to_str(msg, sep=''))
        embed_var.set_author(name=f'{ctx.author.name}\'s Tic Tac Toe Game', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed_var)

    async def input_action(self, ctx, action):
        action = action.lower()
        real_action = [0, 1]
        if len(action) == 2:
            true_action = [char for char in action]
            if true_action[0] in 'abc' and true_action[1] in '123':
                if true_action[0] == 'a':
                    real_action[1] = 0
                elif true_action[0] == 'b':
                    real_action[1] = 1
                else:
                    real_action[1] = 2

                if true_action[1] == '1':
                    real_action[0] = 2
                elif true_action[1] == '2':
                    real_action[0] = 1
                else:
                    real_action[0] = 0

                if self.map[real_action[0]][real_action[1]] != ':black_large_square:':
                    await ctx.send("That area is already filled.")
                    return True
                else:
                    self.map[real_action[0]][real_action[1]] = ':x:'
                    await ctx.send(f"{ctx.author.name} chose {action.upper()}!")
                    return False

            else:
                await self.wrong(ctx)
                return True
        else:
            await self.wrong(ctx)
            return True

    async def enemy_action(self, ctx):
        possible_locations = []
        for row, areas in enumerate(self.map):
            for column, area in enumerate(areas):
                if area == ':black_large_square:':
                    possible_locations.append((row, column))
        chosen = r.choice(possible_locations)
        self.map[chosen[0]][chosen[1]] = ':o:'

        chosen_print = []
        if chosen[1] == 0:
            chosen_print.append('A')
        elif chosen[1] == 1:
            chosen_print.append('B')
        else:
            chosen_print.append('C')

        if chosen[0] == 0:
            chosen_print.append('3')
        elif chosen[0] == 1:
            chosen_print.append('2')
        else:
            chosen_print.append('1')

        await ctx.send(f"AI chose {list_to_str(chosen_print)}!")

    def check_win(self):
        col_info = [[], [], []]
        for row in self.map:
            counter1 = 0
            counter2 = 0
            for area in row:
                if area == ':x:':
                    counter1 += 1
                elif area == ':o:':
                    counter2 += 1

            if counter1 == 3:
                return 1
            elif counter2 == 3:
                return 2

            col_info[0].append(row[0])
            col_info[1].append(row[1])
            col_info[2].append(row[2])

        for col in col_info:
            counter1 = 0
            counter2 = 0
            for area in col:
                if area == ':x:':
                    counter1 += 1
                elif area == ':o:':
                    counter2 += 1

            if counter1 == 3:
                return 1
            elif counter2 == 3:
                return 2

        diag1 = [self.map[0][0], self.map[1][1], self.map[2][2]]
        diag2 = [self.map[0][2], self.map[1][1], self.map[2][0]]
        counter1 = 0
        counter2 = 0
        for area in diag1:
            if area == ':x:':
                counter1 += 1
            elif area == ':o:':
                counter2 += 1

            if counter1 == 3:
                return 1
            elif counter2 == 3:
                return 2

        counter1 = 0
        counter2 = 0
        for area in diag2:
            if area == ':x:':
                counter1 += 1
            elif area == ':o:':
                counter2 += 1

            if counter1 == 3:
                return 1
            elif counter2 == 3:
                return 2

        return 0

    async def start(self, ctx):
        if not self.first:
            await self.enemy_action(ctx)
            await self.display(ctx)

        else:
            await self.display(ctx)

    async def play(self, ctx, action):
        if await self.input_action(ctx, action):
            return False, 2

        await self.display(ctx)
        if (check := self.check_win()) == 1:
            await ctx.send('Player 1 Wins!')
            del self
            return True, 0

        elif check == 2:
            await ctx.send('Player 2 Wins!')
            del self
            return True, 1

        await self.enemy_action(ctx)
        await self.display(ctx)
        if (check := self.check_win()) == 1:
            await ctx.send('Player 1 Wins!')
            del self
            return True, 0

        elif check == 2:
            await ctx.send('Player 2 Wins!')
            del self
            return True, 1

        return False, 2


ttt_game_list = []


def ttt_check(id):
    user = discord.utils.find(lambda x: x == str(id), games.keys())
    if user is None:
        games[str(id)] = {'ttt': {'games': 0, 'wins': 0}}
    else:
        game = discord.utils.find(lambda x: x == 'ttt', games[str(id)].keys())
        if game is None:
            games[str(id)]['ttt'] = {'games': 0, 'wins': 0}


@bot.group()
async def ttt(ctx):
    pass


@ttt.command(name='info')
async def info(ctx):
    await ctx.send("To start a game, type `tur ttt start`. Then, while playing, type `tur ttt play [loc]`, "
                   "where [loc] is the area, with the bottom left being A1. To see some of your stats, "
                   "type `tur ttt stats`.")


@ttt.command(name='start')
async def start(ctx):
    for g in ttt_game_list:
        if str(g.player.id) == str(ctx.author.id):
            await ctx.send("You already are playing a game of Tic Tac Toe. Type `tur ttt info` for help.")
            return

    await ctx.send("You are starting a game of Tic Tac Toe!")
    g = TTTGame(ctx.author)
    ttt_game_list.append(g)
    await g.start(ctx)


@ttt.command(name='play')
async def play(ctx, action: str):
    for i, g in enumerate(ttt_game_list):
        if str(g.player.id) == str(ctx.author.id):
            finished, winner = await g.play(ctx, action)

            if finished:
                del ttt_game_list[i]

                ttt_check(ctx.author.id)

                games[str(ctx.author.id)]['ttt']['games'] += 1
                if winner == 0:
                    games[str(ctx.author.id)]['ttt']['wins'] += 1

                input_json()

            return

    await ctx.send("You have not started a game of Tic Tac Toe yet. Type `tur ttt info` for help.")


@ttt.command(name='stats')
async def stats(ctx):
    ttt_check(ctx.author.id)

    games_played = games[str(ctx.author.id)]['ttt']['games']
    wins = games[str(ctx.author.id)]['ttt']['wins']

    description = f'**Games Played:** {str(games_played)} \n' \
                  f'**Wins:** {str(wins)}'
    embed_var = discord.Embed(description=description)
    embed_var.set_author(name=f'{ctx.author.name}\'s Stats', icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed_var)

    input_json()
