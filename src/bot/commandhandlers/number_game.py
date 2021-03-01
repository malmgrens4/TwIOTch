import asyncio

from twitchio.dataclasses import Message
from src.bot.bot import TeamData
from src.bot.botstates.BotState import BotState
from src.bot.commandhandlers.utils import parse_args
from src.bot.botstates.NumberCounterBot import NumberCounterBot
from src.bot.gameobservers.NumberGameScoreObserver import NumberGameScoreObserver
from src.bot.gameobservers.NumberGameChatObserver import NumberGameChatObserver


async def start_number_game(msg: Message, team_data: TeamData, botState: BotState):
    """Starts a game where teams compete to list every number between 1 and the target number"""
    if not msg.author.is_mod:
        return

    args = parse_args(msg, ['target_number'])
    target_number = int(args['target_number'])

    number_counter_bot = NumberCounterBot(target_number=target_number, team_data=team_data)
    number_counter_bot.attach(NumberGameChatObserver())
    number_counter_bot.attach(NumberGameScoreObserver())

    botState.transition_to(number_counter_bot)
    await number_counter_bot.game_start()
    await msg.channel\
        .send(f"Number game started with {team_data.num_teams} teams. First to count to {target_number} wins!")
    return
