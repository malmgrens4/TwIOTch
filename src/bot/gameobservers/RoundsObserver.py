from src.bot import RoundsManager
from src.bot.botstates.TeamGameHandler import TeamGameHandler
from src.bot.gameobservers.Observer import Observer


class RoundsObserver(Observer):
    def __init__(self, rounds_manager: RoundsManager):
        self.rounds_manager = rounds_manager

    async def update(self, subject: TeamGameHandler) -> None:
        if subject.won:
            await self.rounds_manager.end_round()
