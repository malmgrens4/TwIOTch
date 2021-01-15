from twitchio.dataclasses import Context

from src.bot.botstates.BotState import BotState
from src.bot.botstates.TeamGameHandler import TeamGameHandler


class TriviaBot(BotState, TeamGameHandler):

    def __init__(self, target_number: int, num_teams: int):

        super().__init__(target_number=target_number, num_teams=num_teams)
        """Contains possible answers to current question"""
        self.options = []
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

    def talley(self):
        # get the percentage right each team had.
        pass
