import logging

from src.bot.gameobservers.Observer import Observer
from src.bot.botstates.TriviaBot import TriviaBot


class TriviaChatObserver(Observer):
    def __init__(self):
        self.question_asked = False

    async def update(self, subject: TriviaBot) -> None:

        # With how long the display takes we don't want to fire
        # this off and have it be buried. TODO make this a config option
        # if not self.question_asked and subject.game_started:
        #     self.question_asked = True
        #     await subject.send_message("Question: %s" % subject.question)
        #     for key, value in subject.options.items():
        #         await subject.send_message("%s: %s" % (key, value))

        if subject.won:
            await subject.send_message("Correct answers: %s" % ", ".join(subject.correct_options))

    async def on_abort(self, subject: TriviaBot) -> None:
        if not subject.won:
            await subject.send_message("Game ended early. Correct answers: %s" % ", ".join(subject.correct_options))
