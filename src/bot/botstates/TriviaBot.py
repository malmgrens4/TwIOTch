from twitchio.dataclasses import Message
from typing import Dict, Callable
from datetime import datetime
from dataclasses import dataclass

from src.bot.gameobservers.Observer import Observer
from src.bot.gameobservers.Subject import Subject
from src.bot.botstates.BotState import BotState
from src.bot.botstates.TeamGameHandler import TeamGameHandler
from src.bot.botstates.DefaultBot import DefaultBot
from src.bot.TeamData import TeamData


@dataclass
class TriviaResponse:
    time_to_answer: int = None
    answer: str = None


class TriviaBot(TeamGameHandler, BotState, Subject):

    def __init__(self, team_data: TeamData, question: str,
                 options: Dict[str, str], correct_options: [str], send_message: Callable[[str], None]):

        super().__init__(team_data=team_data)
        self.question = question
        self.options = options
        self.correct_options = correct_options
        self.observers = []
        self.won = False
        self.winning_team_ids = []
        self.team_data = team_data
        self.send_message = send_message
        self.game_start_time = datetime.utcnow()
        """
            Contains teams answers (a list of teams maps: 
            map containing the user and their answer) 
            [{user_id: answer}]
        """
        self.team_responses: [Dict[int, TriviaResponse]] = None

    def attach(self, observer: Observer) -> None:
        self.observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self.observers.remove(observer)

    async def notify(self) -> None:
        for observer in self.observers:
            await observer.update(self)

    async def game_start(self):
        self.team_responses = [{} for _ in range(self.team_data.num_teams)]
        await super().game_start()
        await self.notify()

    async def handle_event_message(self, msg: Message) -> None:
        """
        Process incoming user message in trivia state
        """

        if not self.game_started:
            return

        team_id = self.team_data.teams.get(msg.author.id)
        if team_id is None:
            return

        if msg.author.id in self.team_responses[team_id]:
            return

        user_input = msg.content.lower()
        if user_input in self.options:
            time_elapsed = int((datetime.utcnow() - self.game_start_time).total_seconds() * 1000)
            self.team_responses[team_id][msg.author.id] = TriviaResponse(time_to_answer=time_elapsed, answer=user_input)

            # every user that joined has answered so end the game
            if sum([len(responses.values()) for responses in self.team_responses]) == len(self.team_data.teams):
                await self.end_game()
                return

        await self.notify()

    def get_tally(self):
        """
        :return: Dict {team_id: percentage_right (float)}
        """
        team_weights: [float] = [0 for _ in range(self.team_data.num_teams)]
        for i, responses in enumerate(self.team_responses):

            team_responses: [TriviaResponse] = list(responses.values())

            if len(responses) == 0:
                team_weights[i] = 0
                continue

            num_correct_responses: int = len([response for response in team_responses
                                              if response.answer in self.correct_options])
            team_weights[i] = num_correct_responses / len(responses)

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

    async def can_join(self, msg: Message) -> bool:
        return await super().can_join(msg)
