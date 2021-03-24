from __future__ import annotations
import os
import asyncio
import logging

from src.bot.gameobservers.Observer import Observer
from src.bot.botstates.TriviaBot import TriviaBot

log = logging.getLogger(__name__)


class TriviaAnswerTimerObserver(Observer):
    def __init__(self):
        self.trivia_started = False
        self.task = None
        self.max_response_time = int(os.environ['TRIVIA_RESPONSE_TIME_SECONDS'])
        pass

    async def update(self, subject: TriviaBot) -> None:
        async def close_trivia():
            await asyncio.sleep(self.max_response_time)
            await subject.end_game()

        if subject.game_started and not self.task:
            self.task = asyncio.create_task(close_trivia())
            await self.task

        if subject.won and self.task:
            self.task.cancel()


