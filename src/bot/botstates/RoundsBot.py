import argparse
import logging
from twitchio import Message
from src.bot.RoundsQueue import RoundsQueue, Round
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
        if not msg.author.is_mod or "!rounds" in msg.content:
            return

        if msg.content.lower() == "start":
            await self.rounds_queue.start()
            return

        parser = ArgumentParser(description='Create a round.')
        parser.add_argument('repeats', metavar='n', type=int, help='Number of times the game should repeat.')

        subparsers = parser.add_subparsers(help='trivia or number', dest='game')

        number_parser = subparsers.add_parser('number', help='Specify a number to count to!')
        number_parser.add_argument('-c', '--count', type=int, help="Number users will count to.")

        trivia_parser = subparsers.add_parser('trivia', help='Optionally specify a category')
        trivia_parser.add_argument('-c', '--category', metavar='TRIVIA CATEGORY', type=str,
                                   help='Any valid trivia category.')

        msg_content = msg.content.lower()
        try:
            round_args = parser.parse_args(msg_content.split())
        except Exception as err:
            logging.error(err)
            await msg.channel.send(err)
            return

        for i in range(0, round_args.repeats):
            if round_args.game == 'trivia':
                self.rounds_queue.add_round(Round(name=round_args.game, on_round_start=lambda: trivia.start_trivia(send_message=msg.channel.send, category=round_args.category, team_data=self.team_data, botState=self.context)))
            elif round_args.game == 'number':
                self.rounds_queue.add_round(Round(name=round_args.game, on_round_start=lambda: number_game.start_number_game(team_data=self.team_data, botState=self.context, send_message=msg.channel.send, target_number=round_args.count)))

