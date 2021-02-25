from typing import Dict
from twitchio.dataclasses import Message


class TeamData:

    def __init__(self, num_teams: int = 2):
        self.num_teams = num_teams
        self.teams: Dict[int, int] = {}

    async def handle_join(self, msg: Message) -> None:
        if msg.author.id in self.teams:
            # User already on a team
            return

        all_teams = self.teams.values()

        if len(all_teams) < self.num_teams:
            self.teams[msg.author.id] = len(all_teams)
            return

        team_counts: Dict[int, int] = {}
        for team_id in all_teams:
            team_counts[team_id] = team_counts.setdefault(team_id, 0) + 1

        min_member_team_id = min(team_counts, key=team_counts.get)
        self.teams[msg.author.id] = min_member_team_id

    def get_team_member_map(self):
        reverse_dict = {}
        for k, v in self.teams.items():
            reverse_dict.setdefault(v, []).append(k)
        return reverse_dict

    def reset(self, num_teams: int = 2):
        self.num_teams = num_teams
        self.teams: Dict[int, int] = {}