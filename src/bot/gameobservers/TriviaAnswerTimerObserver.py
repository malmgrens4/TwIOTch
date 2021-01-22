from __future__ import annotations
import asyncio
import logging

from src.bot.gameobservers.Observer import Observer
from src.bot.botstates.TriviaBot import TriviaBot

log = logging.getLogger(__name__)


class TriviaAnswerTimerObserver(Observer):
    def __init__(self):
        self.trivia_started = False
        self.task = None
        pass

    async def update(self, subject: TriviaBot) -> None:
        async def close_trivia():
            await asyncio.sleep(30)
            await subject.end_game()

        if subject.won and self.task:
            self.task.cancel()

        if subject._game_started and not self.task:
            self.task = asyncio.create_task(close_trivia())
            await self.task
