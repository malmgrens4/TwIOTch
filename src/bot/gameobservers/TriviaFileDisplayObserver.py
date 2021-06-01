import logging
import os
import asyncio
from src.bot.gameobservers.Observer import Observer
from src.bot.botstates.TriviaBot import TriviaBot
from src.bot.gameobservers.utils import create_trivia_display
from typing import Dict
from src.bot.RoundsQueue import rounds_queue


class TriviaFileDisplayObserver(Observer):
    trivia_template_path = os.path.join(os.environ['DISPLAY_FILE_PATH'],
                                        os.environ['TRIVIA_TEMPLATE_FILE_NAME']).replace("\\", "/")

    trivia_question_path = os.path.join(os.environ['DISPLAY_FILE_PATH'],
                                        os.environ['TRIVIA_QUESTION_FILE_NAME']).replace("\\", "/")

    def __init__(self):
        self.display_on = False

    async def update(self, subject: TriviaBot) -> None:
        """Toggle all trivia displays to sync with game."""
        if not self.display_on and subject.game_started:
            self.display_on = True
            create_trivia_display(subject.question, subject.options)

        if subject.won:
            # if the time between rounds is greater than 10 seconds display the answers
            # then delete it, otherwise just delete the trivia_question.png file
            if int(rounds_queue.time_between_rounds/5) >= 10:

                correct_options: Dict[str, str] = {}
                # create a display with only right answers
                for key, value in subject.options.items():
                    if key in subject.correct_options:
                        correct_options[key] = value

                create_trivia_display(subject.question, correct_options)
                await asyncio.sleep(10)

            self.clear_trivia_display()

    def clear_trivia_display(self):
        try:
            os.remove(self.trivia_question_path)
        except Exception as err:
            logging.error(err)

    async def on_abort(self, subject: TriviaBot) -> None:
        """
        make sure the current trivia
        display is cleared
        """
        self.clear_trivia_display()





