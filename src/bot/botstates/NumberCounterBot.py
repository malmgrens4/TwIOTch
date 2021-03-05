from __future__ import annotations
from twitchio.dataclasses import Message
import logging

from typing import TYPE_CHECKING
from src.bot.botstates.BotState import BotState
from src.bot.botstates.DefaultBot import DefaultBot
from src.bot.botstates.TeamGameHandler import TeamGameHandler

from src.bot.gameobservers.Subject import Subject
from src.bot.TeamData import TeamData

if TYPE_CHECKING:
    from src.bot.gameobservers.Observer import Observer

log = logging.getLogger(__name__)


class NumberCounterBot(TeamGameHandler, BotState, Subject):

    def __init__(self, target_number: int, team_data: TeamData):
        super().__init__(team_data)
        if target_number < 0:
            target_number = abs(target_number)

        self.target_number = target_number
        self.winning_team_id: int = None
        self.team_numbers = None
        self.won = False
        self.observers = []
        self.msg = None

    def attach(self, observer: Observer) -> None:
        self.observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self.observers.remove(observer)

    async def notify(self) -> None:
        for observer in self.observers:
            await observer.update(self)

    async def handle_event_message(self, msg: Message) -> None:
        self.msg = msg

        if not self.game_started:
            return

        team_id = self.team_data.teams.get(msg.author.id)
        if team_id is None:
            return

        user_input_number = int(msg.content)
        if 0 < user_input_number <= self.target_number:
            if user_input_number not in self.team_numbers[team_id]:
                self.team_numbers[team_id].add(user_input_number)
                # check for win condition
                if len(self.team_numbers[team_id]) == self.target_number:
                    await self.win(team_id)
                    return
        await self.notify()

    # TODO remove this
    def get_team_member_map(self):
        return self.team_data.get_team_member_map()

    async def game_start(self):
        self.team_numbers = [set() for _ in range(self.team_data.num_teams)]
        await super().game_start()
        await self.notify()

    async def win(self, winning_team_id: int) -> None:
        self.won = True
        self.winning_team_id = winning_team_id
        self.context.transition_to(DefaultBot())
        await self.notify()

    async def can_join(self, msg: Message) -> bool:
        return await super().can_join(msg)
