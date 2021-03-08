from twitchio.dataclasses import Message
from src.bot.TeamData import TeamData
from src.bot.botstates.BotState import BotState
from src.bot.botstates.RCCarBot import RCCarBot
from src.bot.commandhandlers.utils import parse_args


async def start_battle_car(msg: Message, team_data: TeamData, botState: BotState):
    """Starts a game where teams compete to list every number between 1 and the target number"""
    if not msg.author.is_mod:
        return

    rc_car_bot = RCCarBot(team_data=team_data, msg=msg)

    botState.transition_to(rc_car_bot)
    await rc_car_bot.game_start()
    await msg.channel\
        .send("May the best car win.")
    return


async def end_battle_car(msg: Message, botState: BotState):
    if not msg.author.is_mod:
        return

    args = parse_args(msg, ['winning_team_id'])
    await botState.context.win(int(args['winning_team_id']))