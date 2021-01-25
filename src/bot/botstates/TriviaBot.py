import asyncio
from twitchio.dataclasses import Message
from typing import Dict

from src.bot.gameobservers.Observer import Observer
from src.bot.gameobservers.Subject import Subject
from src.bot.botstates.BotState import BotState
from src.bot.botstates.TeamGameHandler import TeamGameHandler
from src.bot.botstates.DefaultBot import DefaultBot


class TriviaBot(TeamGameHandler, BotState, Subject):

    def __init__(self, num_teams: int, question: str,
                 options: Dict[str, str], correct_responses: [str], msg: Message):

        super().__init__(num_teams=num_teams)
        self.question = question
        self.options = options
        self.correct_responses = correct_responses

        self.observers = []
        self.won = False
        self.winning_team_ids = []

        self.msg = msg

        """
            Contains teams answers (a list of teams maps: 
            map containing the user and their answer) 
            [{user_id: answer}]
        """
        self.team_answers: [Dict[int, str]] = [{} for _ in range(self.num_teams)]

    def attach(self, observer: Observer) -> None:
        self.observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self.observers.remove(observer)

    async def notify(self) -> None:
        for observer in self.observers:
            await observer.update(self)

    async def handle_join(self, msg: Message) -> None:
        self.msg = msg
        await super().handle_join(msg)
        await self.notify()

    async def game_start(self):
        await super().game_start()
        await self.notify()

    async def handle_event_message(self, msg: Message) -> None:
        """
        Process incoming user message in trivia state
        """
        self.msg = msg

        if not self.game_started:
            return

        team_id = self.teams.get(msg.author.id)
        if team_id is None:
            return

        if msg.author.id in self.team_answers[team_id]:
            return

        user_input = msg.content
        if user_input in self.options:
            self.team_answers[team_id][msg.author.id] = user_input

            # every user that joined has answered so end the game
            if sum([len(answers.values()) for answers in self.team_answers]) == len(self.teams):
                await self.end_game()
                return

        await self.notify()

    def get_tally(self):
        """
        :return: Dict {team_id: percentage_right (float)}
        """
        team_weights: [float] = [0 for _ in range(self.num_teams)]
        for i, answers in enumerate(self.team_answers):

            all_answers = list(answers.values())

            if len(all_answers) == 0:
                team_weights[i] = 0
                continue

            num_correct_answers = len([answer for answer in all_answers if answer in self.correct_responses])
            team_weights[i] = num_correct_answers / len(all_answers)

        return team_weights

    async def end_game(self):
        """
        Talley results and determine a winner
        """
        team_weights = self.get_tally()
        winning_team_ids = [i for i, team_weight in enumerate(team_weights) if team_weight == max(team_weights)]
        if max(team_weights) == 0:
            winning_team_ids = []
        await self.win(winning_team_ids)

    async def win(self, winning_team_ids: int):
        self.won = True
        self.winning_team_ids = winning_team_ids
        self.context.transition_to(DefaultBot())
        await self.notify()
