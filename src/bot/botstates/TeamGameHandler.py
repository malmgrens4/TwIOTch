import asyncio

from twitchio.dataclasses import Context


class TeamGameHandler:

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

        if target_number <= 0:
            target_number = 1
        self.target_number = target_number

        self.teams: dict[int, int] = {}

        # allow x amount of seconds for users to join
        # before game start
        async def schedule_join():


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
