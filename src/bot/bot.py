import os
import logging
from asyncio import sleep
from twitchio.ext import commands
from src.bot.RoundsQueue import RoundsQueue
from src.bot.botstates.DefaultBot import DefaultBot
from src.blueteeth.toolbox.toolbox import get_phuelight
from src.bot.botstates.Context import Context as BotStateContext
from twitchio.dataclasses import Message
from src.bot.botstates.RoundsBot import RoundsBot
from src.bot.commandhandlers.utils import parse_args
from src.bot.db.schema import session_scope, User, Team
from src.bot.TeamData import TeamData
from src.bot.commandhandlers import trivia, number_game, battle_car, admin
# we need a game context with
# teams (all twitch chat members that opt in)
botState = BotStateContext(DefaultBot())

team_data = TeamData(2)
rounds_queue = RoundsQueue(new_time_between_rounds=20)

bot = commands.Bot(
    # set up the bot
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

rounds_queue = rounds_queue


@bot.event
async def event_message(ctx: Message):
    # make sure the bot ignores itself and the streamer
    if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
        return

    await bot.handle_commands(ctx)
    await botState.handle_event_message(ctx)
    # otherwise check if we are in a message listening state (e.g. trivia)
    # TODO see if this fires on commands as well
    # first step is to pass the message along to the ones that care
    # how do we know whether or not we care about messages
    # I'm thinking state so (event_message_ctx.event_message(ctx))
    # The different states will be like (trivia, number_counter, default)
    # Let's start with the number counter to see how this will look


@bot.event
async def event_ready():
    """Called once when the bot goes online."""
    print(f"{os.environ['BOT_NICK']} is online now!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ['CHANNEL'], f"/me has arrived.")


@bot.command(name='cancel')
async def cancel(msg: Message):
    await admin.cancel(msg.channel.send, botState)
    botState.transition_to(DefaultBot())


@bot.command(name='rounds')
async def rounds(msg: Message):
    global rounds_queue
    rounds_queue.clear()
    args = parse_args(msg, ['time_between_rounds'])
    time_between_rounds = 30

    if args['time_between_rounds']:
        time_between_rounds = int(args['time_between_rounds'])

    rounds_queue.set_time_between_rounds(time_between_rounds)
    botState.transition_to(RoundsBot(rounds_queue=rounds_queue, team_data=team_data))


@bot.command(name='create_teams', aliases=['teams', 'resetteams'])
async def create_teams(msg: Message):
    if not msg.author.is_mod:
        return

    args = parse_args(msg, ['num_teams'])
    team_data.reset(int(args['num_teams']))
    await msg.channel.send("Game session has started. Type !joingame to play!")


@bot.command(name='join_game', aliases=['jointrivia', 'joinnumber', 'joingame'])
async def join_game(msg: Message):
    """User (Sender) is joining the current event. Default state ignores if no current game."""
    with session_scope() as session:
        session.add(User(id=msg.author.id, name=msg.author.name))

    if await botState.can_join(msg):
        await team_data.handle_join(msg)
        await botState.handle_join(msg)
        team_id: int = team_data.teams[msg.author.id]
        team_name = get_team_name(team_id)
        await msg.channel.send(f'{msg.author.name} has joined the {team_name}')
    else:
        await msg.channel.send("You may not currently join the game.")


def get_team_name(team_id: int):
    with session_scope() as session:
        team_name = session.query(Team).get(team_id + 1).name
    return team_name


@bot.command(name='start_number_game')
async def start_number_game(msg: Message):
    """Starts a game where teams compete to list every number between 1 and the target number"""
    if not msg.author.is_mod:
        return

    args = parse_args(msg, ['target_number'])
    target_number = int(args['target_number'])
    return await number_game.start_number_game(send_message=msg.channel.send, target_number=target_number, botState=botState, team_data=team_data)


@bot.command(name='start_battle_car')
async def start_battle_car(msg: Message):
    return await battle_car.start_battle_car(msg=msg, botState=botState, team_data=team_data)


@bot.command(name='end_battle_car')
async def end_battle_car(msg: Message):
    return await battle_car.end_battle_car(msg=msg, botState=botState)


@bot.command(name='leaderboard')
async def leaderboard(msg: Message):
    """Lists leader board for given game. Number or Trivia."""
    args = parse_args(msg, ['game_name'])
    game_name = args['game_name']

    if not game_name:
        await msg.channel.send("Please specify a game: number or trivia.")
        return

    with session_scope() as session:
        if game_name == 'number':
            leaderboard_query = session.query(User).order_by(User.number_game_wins.desc()).limit(10).all()
        else:
            leaderboard_query = session.query(User).order_by(User.trivia_points.desc()).limit(10).all()

        for i, user in enumerate(leaderboard_query):
            if game_name == 'number':
                points = user.number_game_wins
            else:
                points = user.trivia_points
            await msg.channel.send(f"{i + 1}. {user.name} {points}")


@bot.command(name='categories')
async def categories(msg: Message):
    """Lists categories for trivia."""
    return await trivia.categories(msg)


@bot.command(name='start_trivia', aliases=['trivia'])
async def start_trivia(msg: Message):
    """Starts a game of trivia. A category may be specified."""

    args = msg.content.split()
    category = None

    if len(args) >= 2:
        category = "".join(args[1:]).replace('"', '')

    return await trivia.start_trivia(send_message=msg.channel.send, category=category, botState=botState, team_data=team_data)


@bot.command(name='help')
async def help(msg: Message):
    """See this list of commands."""
    for name, command in bot.commands.items():
        names = [name]
        if command.aliases:
            names.extend(command.aliases)

        await msg.channel.send("""!%s: %s""" % (", ".join(names), command._callback.__doc__))


@bot.command(name='light')
async def light(ctx):
    """light"""
    phueLight = get_phuelight()

    phueLight.set_light()
    try:
        indices = []
        args = ctx.content.split()[1:]

        if len(args) <= 0:
            await ctx.send('Specify a color! Ex. !light pink')
        color_name = args[0]
        if color_name == 'disco':
            phueLight.disco_light()
            return
        if len(args) > 1:
            # allow users to specify index
            for i in range(1, len(args)):
                index = int(args[i]) - 1
                if index < len(phueLight.bridge.lights):
                    indices.append(index)
        if len(indices) <= 0:
            indices = list(range(0, len(phueLight.bridge.lights)))
        phueLight.set_light(color_name, indices)
    except:
        await ctx.send('Try a different color.')
