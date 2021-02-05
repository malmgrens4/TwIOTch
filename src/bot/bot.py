import os
import asyncio

import configparser
import logging.config
from twitchio.ext import commands
from sqlalchemy.sql.expression import func

from src.bot.botstates.DefaultBot import DefaultBot
# from src.blueteeth.toolbox.toolbox import get_phuelight
from src.bot.botstates.Context import Context as BotStateContext
from twitchio.dataclasses import Message
from src.bot.botstates.NumberCounterBot import NumberCounterBot
from src.bot.botstates.TriviaBot import TriviaBot
from src.bot.gameobservers.NumberGameChatObserver import NumberGameChatObserver
from src.bot.gameobservers.NumberGameScoreObserver import NumberGameScoreObserver
from src.bot.gameobservers.TriviaChatObserver import TriviaChatObserver
from src.bot.gameobservers.TriviaAnswerTimerObserver import TriviaAnswerTimerObserver
from src.bot.db.schema import session_scope, User, TriviaQuestion

config = configparser.ConfigParser()
config.read('config.ini')

log = logging.getLogger(__name__)

# we need a game context with
# teams (all twitch chat members that opt in)
botState = BotStateContext(DefaultBot())

bot = commands.Bot(
    # set up the bot
    irc_token=os.environ['TMI_TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)


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


@bot.command(name='join_game')
async def join_game(msg: Message):
    """User (Sender) is joining the current event. Default state ignores if no current game."""
    with session_scope() as session:
        session.add(User(id=msg.author.id, name=msg.author.name))

    await botState.handle_join(msg)


@bot.command(name='start_number_game')
async def start_number_game(msg: Message):
    """Starts a game where teams compete to list every number between 1 and the target number"""
    if not msg.author.is_mod:
        return

    args = msg.content.split()[1:]
    num_teams = 2
    if len(args) == 2:
        num_teams = int(args[1])

    target_number = int(args[0])
    number_counter_bot = NumberCounterBot(num_teams, target_number)
    number_counter_bot.attach(NumberGameChatObserver())
    number_counter_bot.attach(NumberGameScoreObserver())

    botState.transition_to(number_counter_bot)
    await msg.channel.send("Type !join_game to join a team for number showdown!")
    # sleep for 30 while players join
    await asyncio.sleep(10)
    await number_counter_bot.game_start()
    await msg.channel.send("Number game started with %s teams. First to count to %s wins!" % (num_teams, target_number))


@bot.command(name='trivia_leaderboard')
async def trivia_leaderboard(msg: Message):
    """Send the top 10 players names for trivia wins"""
    with session_scope() as session:
        question_query = session.query(User).order_by(User.trivia_wins).limit(10)
        for i, user in enumerate(question_query):
            await msg.channel.send("""%s. %s \n""" % (i + 1, user.name))



@bot.command(name='start_trivia')
async def start_trivia(msg: Message):
    """Starts a game of trivia."""
    if not msg.author.is_mod:
        return

    args = msg.content.split()[1:]
    category = None
    num_teams = 2

    if len(args) > 0:
        category = args[0]

    if len(args) == 2:
        num_teams = args[1]

    with session_scope() as session:
        if category:
            question_query = session.query(TriviaQuestion).filter(TriviaQuestion.category == category)
        else:
            question_query = session.query(TriviaQuestion)

        question = question_query.order_by(func.random()).first()
        options = question.options

        options_map = {}
        for i, option in enumerate(options):
            options_map[chr(i + 97)] = option.option

        correct_responses = [chr(i + 97) for i, option in enumerate(options) if option.is_correct]

        trivia_bot = TriviaBot(num_teams=num_teams,
                               question=question.question,
                               options=options_map,
                               correct_responses=correct_responses,
                               msg=msg)

        trivia_bot.attach(TriviaChatObserver())
        trivia_bot.attach(TriviaAnswerTimerObserver())
        botState.transition_to(trivia_bot)

        await msg.channel.send("Type !join_game to join a team for trivia!")
        # sleep for 30 while players join
        await asyncio.sleep(30)
        await trivia_bot.game_start()


# TODO need a better way to do arg parsing so every command doesn't
# look like this
# @bot.command(name='light')
# async def light(ctx):
#     """light"""
#     phueLight = get_phuelight()
#
#     phueLight.set_light()
#     try:
#         indices = []
#         args = ctx.content.split()[1:]
#
#         if len(args) <= 0:
#             await ctx.send('Specify a color! Ex. !light pink')
#         color_name = args[0]
#         if color_name == 'disco':
#             phueLight.disco_light()
#             return
#         if len(args) > 1:
#             # allow users to specify index
#             for i in range(1, len(args)):
#                 index = int(args[i]) - 1
#                 if index < len(phueLight.bridge.lights):
#                     indices.append(index)
#         if len(indices) <= 0:
#             indices = list(range(0, len(phueLight.bridge.lights)))
#         phueLight.set_light(color_name, indices)
#     except:
#         await ctx.send('Try a different color.')
