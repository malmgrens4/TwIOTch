from src.bot import RoundsQueue
from src.bot.RoundsQueue import RoundsQueue
from src.bot.botstates.TeamGameHandler import TeamGameHandler
from src.bot.gameobservers.Observer import Observer


class RoundsObserver(Observer):
    def __init__(self):
        from src.bot.bot import rounds_queue
        self.rounds_queue = rounds_queue

    async def update(self, subject: TeamGameHandler) -> None:
        if subject.won:
            await self.rounds_queue.end_round()
