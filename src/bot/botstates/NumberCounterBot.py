from twitchio.dataclasses import Context
import logging

from .BotState import BotState
from .DefaultBot import DefaultBot

log = logging.getLogger(__name__)


class NumberCounterBot(BotState):

    def __init__(self, target_number: int, num_teams: int = 2):
        """
        Parameters
        ----------
        num_teams: number of teams
        target_number: the value that defines the range users must count to
        """
        if num_teams <= 1:
            num_teams = 2
        self.num_teams = num_teams

        self.team_numbers = [set() for _ in range(num_teams)]

        if target_number <= 0:
            target_number = 1
        self.target_number = target_number

        self.teams: dict[int, int] = {}
        log.debug("Number game started with num_teams: %s. target_number: %s." % (num_teams, target_number))
        # TODO start a timer to block joins

    def handle_join(self, ctx: Context) -> None:
        if ctx.author.id in self.teams:
            # User already on a team
            return

        all_teams = self.teams.values()

        if len(all_teams) < self.num_teams:
            self.teams[ctx.author.id] = len(all_teams)
            return

        team_counts: dict[int, int] = {}
        for team_id in all_teams:
            team_counts[team_id] = team_counts.setdefault(team_id, 0) + 1

        min_member_team_id = min(team_counts, key=team_counts.get)
        self.teams[ctx.author.id] = min_member_team_id

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
