import logging
from collections.abc import Callable
import asyncio


class Round:
    def __init__(self, name: str, on_round_start: Callable, on_round_end: Callable = None):
        self.name = name
        self.on_round_start = on_round_start
        self.on_round_end = on_round_end


class RoundsQueue:
    def __init__(self, new_time_between_rounds: int = 5, rounds: [Round] = []):
        self.current_round = None
        self.rounds = rounds
        self.time_between_rounds = new_time_between_rounds

    def set_time_between_rounds(self, new_time_between_rounds: int):
        if new_time_between_rounds < 1:
            new_time_between_rounds = 1
        self.time_between_rounds = new_time_between_rounds

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


