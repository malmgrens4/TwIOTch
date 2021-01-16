import asyncio

from twitchio.dataclasses import Context
from typing import Dict

from src.bot.botstates.BotState import BotState
from src.bot.botstates.TeamGameHandler import TeamGameHandler


class TriviaBot(BotState, TeamGameHandler):

    def __init__(self, target_number: int, num_teams: int, question: str,
                 options: Dict[str, str], correct_response: str):

        super().__init__(target_number=target_number, num_teams=num_teams)
        self.question = question
        self.options = options
        self.correct_response = correct_response

        """Contains teams answers (a map containing the user and their answer)"""
        """{team_id: {user_id: answer}}"""
        self.team_answers = [{} for _ in range(self.num_teams)]

    def handle_join(self, ctx) -> None:
        super().handle_join(ctx)

    def handle_event_message(self, ctx: Context) -> None:
        team_id = self.teams.get(ctx.author.id)
        if team_id is None:
            return

        if ctx.author.id in self.team_answers[team_id]:
            return

        user_input = ctx.message.clean_content
        if user_input in self.options:
            self.team_answers[team_id][ctx.author.id] = user_input

    def get_talley(self):
        """
        :return: Dict {team_id: percentage_right (float)}
        """
        team_weights: Dict[int, float] = {}
        for i, team in enumerate(self.team_answers):
            all_answers = team.values()
            num_correct_answers = all_answers.count(self.correct_response)
            team_weights[i] = num_correct_answers/len(all_answers)
        return team_weights

