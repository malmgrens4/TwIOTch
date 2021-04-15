import argparse
import sys
import logging
from twitchio import Message
from src.bot.RoundsManager import RoundsQueue, Round
from src.bot.TeamData import TeamData
from src.bot.botstates.BotState import BotState
from src.bot.commandhandlers import trivia, number_game


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        raise Exception(message)

class RoundsBot(BotState):

    async def can_join(self, msg: Message) -> bool:
        return True

    def __init__(self, rounds_queue: RoundsQueue, team_data: TeamData):
        self.rounds_queue = rounds_queue
        self.team_data = team_data

    async def handle_join(self, msg: Message) -> None:
        pass

    async def handle_event_message(self, msg: Message) -> None:
        if not msg.author.is_mod or msg.content == "!rounds":
            return

        if msg.content == "start":
            self.rounds_queue.start()

        parser = ArgumentParser(description='Create a round.')
        parser.add_argument('repeats', metavar='n', type=int, nargs='?', help='Number of times the game should repeat.')

        number_group = parser.add_argument_group('number')
        number_group.add_argument('number', metavar='N', help='Play the number game.')
        number_group.add_argument('-c', '--count', type=int, help="Number users will count to.")

        trivia_group = parser.add_argument_group('trivia')
        trivia_group.add_argument('trivia', metavar='T', help='Play trivia')
        trivia_group.add_argument('-t', '--category', metavar='TRIVIA CATEGORY', type=str,
                                  help='Any valid trivia category.')

        msg_content = msg.content.lower()
        try:
            round_args = parser.parse_args(msg_content.split())
        except Exception as err:
            logging.error(err)
            await msg.channel.send(err)
            return

        for i in range(0, round_args.repeats + 1):
            if round_args.trivia:
                self.rounds_queue.add_round(Round(on_round_start=lambda: trivia.start_trivia(send_message=msg.channel.send, category=round_args.category, team_data=self.team_data, botState=self)))
            elif round_args.number:
                self.rounds_queue.add_round(Round(on_round_start=lambda: number_game.start_number_game(team_data=self.team_data, botState=self, send_message=msg.channel.send)))

