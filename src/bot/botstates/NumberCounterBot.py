from __future__ import annotations
from twitchio.dataclasses import Message
import logging

from typing import TYPE_CHECKING, Callable
from src.bot.botstates.BotState import BotState
from src.bot.botstates.DefaultBot import DefaultBot
from src.bot.botstates.TeamGameHandler import TeamGameHandler

from src.bot.gameobservers.Subject import Subject
from src.bot.TeamData import TeamData

if TYPE_CHECKING:
    from src.bot.gameobservers.Observer import Observer


class NumberCounterBot(TeamGameHandler, BotState, Subject):

    def __init__(self, target_number: int, team_data: TeamData, send_message: Callable[[str], None]):
        super().__init__(team_data)
        if target_number < 0:
            target_number = abs(target_number)

        self.target_number = target_number
        self.winning_team_id: int = None
        self.team_numbers = {}
        for i in range(0, team_data.num_teams):
            self.team_numbers[i] = []
        self.won = False
        self._observers = []
        self.send_message = send_message

    @property
    def observers(self) -> None:
        return self._observers

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    async def notify(self) -> None:
        for observer in self._observers:
            await observer.update(self)

    async def handle_event_message(self, msg: Message) -> None:

        if not self.game_started:
            return

        team_id = self.team_data.teams.get(msg.author.id)
        if team_id is None:
            return
        try:
            user_input_number = int(msg.content)
            if 0 < user_input_number <= self.target_number:
                if user_input_number not in self.team_numbers[team_id]:
                    self.team_numbers[team_id].add(user_input_number)
                    # check for win condition
                    if len(self.team_numbers[team_id]) == self.target_number:
                        await self.win(team_id)
                        return
            await self.notify()
        except Exception as err:
            logging.error(err)

    async def handle_join(self, msg: Message) -> None:
        return await super().handle_join(msg)

    async def game_start(self):
        self.team_numbers = [set() for _ in range(self.team_data.num_teams)]
        await super().game_start()
        await self.notify()

    async def win(self, winning_team_id: int) -> None:
        self.won = True
        self.winning_team_id = winning_team_id
        await self.notify()
        self.context.transition_to(DefaultBot())

    async def can_join(self, msg: Message) -> bool:
        return await super().can_join(msg)
