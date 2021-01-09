from twitchio.dataclasses import Context

from . import BotState
from . import Default

class NumberCounter(BotState):

    def __init__(self, num_teams: int, target_number: int):
        """
        Parameters
        ----------
        num_teams: number of teams
        target_number: the value that defines the range users must count to
        """
        self.teams: dict[int, int] = {}
        if num_teams <= 1:
            num_teams = 2
        self.num_teams = num_teams

        self.team_numbers = [set() for _ in num_teams]

        if target_number <= 0:
            target_number = 1
        self.target_number = int(target_number)

        #TODO start a timer to block joins

    def handle_join(self, ctx: Context) -> None:
        if ctx.author.id in self.teams:
            # User already on a team
            return

        all_teams = self.teams.values()
        team_counts: dict[int, int] = {}
        for team_id in all_teams:
            team_counts[team_id] = team_counts.setdefault(team_id, 0) + 1

        min_member_team_id = min(team_counts, team_counts.get)
        self.teams[ctx.author.id] = min_member_team_id

    def handle_event_message(self, ctx: Context) -> None:

        team_id = self.teams[ctx.author.id]

        #TODO diff between clean_content, content, raw_data, etc.
        user_input_number = int(ctx.message.clean_content)
        if 0 < user_input_number and user_input_number < self.target_number:
            if user_input_number in self.team_numbers[team_id]:
                # check for win condition
                if len(self.team_numbers[team_id]) == self.team_numbers:
                    self.win()

    def win(self, winning_team_id: int, ctx: Context) -> None:
        self.context.transition_to(DefaultBot())

