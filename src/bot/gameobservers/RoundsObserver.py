import logging
from src.bot.botstates.TeamGameHandler import TeamGameHandler
from src.bot.gameobservers.Observer import Observer
from src.bot.RoundsQueue import rounds_queue


class RoundsObserver(Observer):
    def __init__(self):
        self.rounds_queue = rounds_queue

    async def update(self, subject: TeamGameHandler) -> None:
        if subject.won and self.rounds_queue.current_round:
            logging.debug("Subject won. Starting next round.")
            await self.rounds_queue.end_round()

    async def on_abort(self, subject: TeamGameHandler) -> None:
        pass
