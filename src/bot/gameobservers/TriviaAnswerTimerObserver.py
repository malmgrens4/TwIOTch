import logging
import os
import asyncio

from src.bot.gameobservers.Observer import Observer
from src.bot.botstates.TriviaBot import TriviaBot


class TriviaAnswerTimerObserver(Observer):
    def __init__(self):
        self.trivia_started = False
        self.task = None
        self.timed_out = False
        self.max_response_time = int(os.environ['TRIVIA_RESPONSE_TIME_SECONDS'])

    async def update(self, subject: TriviaBot) -> None:
        async def close_trivia():
            try:
                await asyncio.sleep(self.max_response_time)
                self.timed_out = True
                logging.debug("Game ending because of timeout. Not all users answered.")
                if not subject.won:
                    await subject.end_game()
            except asyncio.CancelledError as err:
                raise err

        if subject.game_started and not self.task:
            self.task = asyncio.create_task(close_trivia())
            await self.task

        if subject.won and self.task and not self.timed_out:
            self.task.cancel()

    def on_abort(self, subject: TriviaBot) -> None:
        """
        Game ended early - we don't need to end the game
        as the bot context will switch
        """
        if self.task and not self.timed_out:
            self.task.cancel()



