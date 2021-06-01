import logging
from collections.abc import Callable
import asyncio


class Round:
    def __init__(self, name: str, on_round_start: Callable, on_round_end: Callable = None):
        self.name = name
        self.on_round_start = on_round_start
        self.on_round_end = on_round_end


class RoundsQueue:
    def __init__(self, time_between_rounds: int = 5, rounds: [Round] = []):
        self.current_round = None
        self.rounds = rounds
        self._time_between_rounds = time_between_rounds

    @property
    def time_between_rounds(self):
        return self._time_between_rounds

    @time_between_rounds.setter
    def set_time_between_rounds(self, time_between_rounds: int):
        if time_between_rounds < 1:
            time_between_rounds = 1
        self._time_between_rounds = time_between_rounds

    def add_round(self, new_round: Round):
        self.rounds.append(new_round)

    def clear(self):
        self.rounds = []
        self.current_round = None

    async def start(self):
        logging.debug("Starting rounds.")
        await self.start_next_round()

    async def end_round(self):
        if self.current_round and self.current_round.on_round_end:
            await self.current_round.on_round_end()
        logging.debug("Round ended.")
        await asyncio.sleep(self.time_between_rounds)
        await self.start_next_round()

    async def start_next_round(self):
        if len(self.rounds):
            self.current_round = self.rounds.pop(0)
            logging.debug("Starting next round.")
            await self.current_round.on_round_start()


rounds_queue = RoundsQueue(time_between_rounds=20)
