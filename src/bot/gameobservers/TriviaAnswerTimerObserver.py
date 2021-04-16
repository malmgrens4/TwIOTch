import logging
import os
import asyncio

from src.bot.gameobservers.Observer import Observer
from src.bot.botstates.TriviaBot import TriviaBot


class TriviaAnswerTimerObserver(Observer):
    def __init__(self):
        self.trivia_started = False
        self.task = None
        self.max_response_time = int(os.environ['TRIVIA_RESPONSE_TIME_SECONDS'])

    async def update(self, subject: TriviaBot) -> None:
        async def close_trivia():
            try:
                await asyncio.sleep(self.max_response_time)
                logging.debug("Game ending because of timeout. Not all users answered.")
                await subject.end_game()
            except asyncio.CancelledError:
                print("cancelled!")
                raise

        if subject.game_started and not self.task:
            self.task = asyncio.create_task(close_trivia())
            await self.task

        if subject.won and self.task:
            self.task.cancel()


