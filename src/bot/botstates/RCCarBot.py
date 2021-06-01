from __future__ import annotations
from twitchio.dataclasses import Message
import logging

from typing import TYPE_CHECKING
from src.bot.botstates.BotState import BotState
from src.bot.botstates.DefaultBot import DefaultBot
from src.bot.botstates.TeamGameHandler import TeamGameHandler

from src.bot.gameobservers.Subject import Subject
from src.bot.TeamData import TeamData

from src.blueteeth.toolbox.toolbox import get_camaro
from src.blueteeth.toolbox.toolbox import get_needle
from src.blueteeth.models.RCCar import RCCar

if TYPE_CHECKING:
    from src.bot.gameobservers.Observer import Observer


class RCCarBot(TeamGameHandler, BotState, Subject):

    def __init__(self, team_data: TeamData, msg: Message):
        super().__init__(team_data)
        self.won = False
        self.team_bot_map = {}
        self.msg = msg
        self._observers = []

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
        self.msg = msg

        if not self.game_started:
            return

        team_id = self.team_data.teams.get(msg.author.id)
        if team_id is None:
            return

        #process request by teams
        args = msg.content.lower().split(' ')
        direction = args[0]
        steps = 1
        if len(args) == 2:
            try:
                steps = max(1, min(int(args[1]), 5))
            except ValueError:
                steps = 1

        duration = self.steps_to_duration(direction, steps)
        self.execute_instruction(direction=direction, duration=duration, car=self.team_bot_map[team_id])

        await self.notify()

    @staticmethod
    def steps_to_duration(direction: str, steps: int):
        """The instructions are recieved on a scale of 1 - 5.
                This number is the multiplier to translate that to an appropriate
                number of ms"""
        if direction == 'l' or 'r':
            return steps * 150
        if direction == 'f' or 'b':
            return steps * 200


    @staticmethod
    def execute_instruction(direction: str, duration: int, car: RCCar):
        if direction == 'l':
            car.left(duration)
        if direction == 'r':
            car.right(duration)
        if direction == 'f':
            car.forward(duration)
        if direction == 'b':
            car.backward(duration)

    async def handle_join(self, msg: Message) -> None:
        return await super().handle_join(msg)

    # TODO remove this
    def get_team_member_map(self):
        return self.team_data.get_team_member_map()

    async def game_start(self):
        await super().game_start()
        try:
            needle = get_needle()
            await self.msg.channel.send("Needle online.")
            camaro = get_camaro()
            await self.msg.channel.send("Camaro online.")
            self.team_bot_map = {0: needle, 1: camaro}
        except Exception as err:
            await self.msg.channel.send("Please make sure all cars are turned on and in range and try again.")
            raise err

        await self.notify()

    async def win(self, winning_team_id: int) -> None:
        self.won = True
        self.winning_team_id = winning_team_id
        self.context.transition_to(DefaultBot())
        await self.notify()

    async def can_join(self, msg: Message) -> bool:
        return await super().can_join(msg)
