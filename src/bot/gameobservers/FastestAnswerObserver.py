from src.bot.gameobservers.Observer import Observer
from src.bot.botstates.TriviaBot import TriviaBot


class FastestAnswerObserver(Observer):
    def __init__(self):
        pass

    def update(self, subject: TriviaBot) -> None:
        if subject.won:
            answer_times = []

    def on_abort(self, subject: TriviaBot) -> None:
        pass
