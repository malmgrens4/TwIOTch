import asyncio

from collections.abc import Callable
from typing import Dict
from src.bot.TeamData import TeamData

from twitchio.dataclasses import Message


class TeamGameHandler:

    def __init__(self, team_data: TeamData):
        """
        Parameters
        ----------
        num_teams: number of teams
        target_number: the value that defines the range users must count to
        """
        self.team_data = team_data
        self.game_started = False

    async def handle_join(self, msg: Message) -> None:
        return

    @property
    def game_started(self):
        return self._game_started

    @game_started.setter
    def game_started(self, game_state: bool):
        self._game_started = game_state

    async def game_start(self):
        self.game_started = True

    async def can_join(self, _msg: Message) -> bool:
        return not self.game_started





