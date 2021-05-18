from typing import Callable

from twitchio.dataclasses import Message
from src.bot.TeamData import TeamData
from src.bot.botstates.BotState import BotState
from src.bot.commandhandlers.utils import parse_args
from src.bot.botstates.NumberCounterBot import NumberCounterBot
from src.bot.gameobservers.BalloonBoxObserver import BalloonBoxTeamObserver
from src.bot.gameobservers.NumberGameScoreObserver import NumberGameScoreObserver
from src.bot.gameobservers.RoundsObserver import RoundsObserver
from src.bot.gameobservers.WinGameChatObserver import WinGameChatObserver


async def start_number_game(team_data: TeamData, botState: BotState,
                            send_message: Callable[[str], None], target_number: int = 20):
    """Starts a game where teams compete to list every number between 1 and the target number"""
    number_counter_bot = NumberCounterBot(target_number=target_number, team_data=team_data, send_message=send_message)
    number_counter_bot.attach(RoundsObserver())
    number_counter_bot.attach(WinGameChatObserver())
    number_counter_bot.attach(NumberGameScoreObserver())
    number_counter_bot.attach(BalloonBoxTeamObserver())

    botState.transition_to(number_counter_bot)
    await number_counter_bot.game_start()
    await send_message(f"Number game started with {team_data.num_teams} teams. First to count to {target_number} wins!")
    return
