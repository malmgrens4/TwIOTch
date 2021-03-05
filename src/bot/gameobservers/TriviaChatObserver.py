from __future__ import annotations
import logging

from src.bot.gameobservers.Observer import Observer
from src.bot.botstates.TriviaBot import TriviaBot

log = logging.getLogger(__name__)


class TriviaChatObserver(Observer):
    def __init__(self):
        self.question_asked = False

    async def update(self, subject: TriviaBot) -> None:

        if not self.question_asked and subject.game_started:
            self.question_asked = True
            await subject.msg.channel.send("Question: %s" % subject.question)
            for key, value in subject.options.items():
                await subject.msg.channel.send("%s: %s" % (key, value))

        if subject.won:
            await subject.msg.channel.send("The correct answers were: %s" % ", ".join(subject.correct_responses))