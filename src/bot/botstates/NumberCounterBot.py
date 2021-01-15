from twitchio.dataclasses import Context

import logging

from src.bot.botstates.BotState import BotState
from src.bot.botstates.DefaultBot import DefaultBot
from src.bot.botstates.TeamGameHandler import TeamGameHandler

log = logging.getLogger(__name__)


class NumberCounterBot(TeamGameHandler, BotState):

    def __init__(self, target_number: int, num_teams: int):
        super().__init__(target_number=target_number, num_teams=num_teams)
        self.team_numbers = [set() for _ in range(self.num_teams)]

    def handle_join(self, ctx: Context) -> None:
        super().handle_join(ctx)

    def handle_event_message(self, ctx: Context) -> None:

        team_id = self.teams.get(ctx.author.id)
        if team_id is None:
            return

        # TODO diff between clean_content, content, raw_data, etc.
        user_input_number = int(ctx.message.clean_content)
        if 0 < user_input_number <= self.target_number:
            if user_input_number not in self.team_numbers[team_id]:
                self.team_numbers[team_id].add(user_input_number)
                # check for win condition
                if len(self.team_numbers[team_id]) == self.target_number:
                    self.win(team_id, ctx)

    def win(self, winning_team_id: int, ctx: Context) -> None:
        ctx.send("""Team %s wins!""" % winning_team_id)
        self.context.transition_to(DefaultBot())
