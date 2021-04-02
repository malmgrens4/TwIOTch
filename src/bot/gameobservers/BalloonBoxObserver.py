import logging
from src.blueteeth.toolbox import toolbox
from src.bot.botstates.TeamGameHandler import TeamGameHandler
from src.bot.gameobservers.Observer import Observer

log = logging.getLogger(__name__)


class BalloonBoxTeamObserver(Observer):
    def __init__(self):
        self.balloon_box = toolbox.get_balloon_box()

    async def update(self, subject: TeamGameHandler) -> None:
        if subject.won and subject.team_data.num_teams == 2:
            if 0 in subject.winning_team_ids:
                log.debug("Team 0 win. Inflating left balloon.")
                self.balloon_box.left_pump()
            if 1 in subject.winning_team_ids:
                log.debug("Team 1 win. Inflating right balloon.")
                self.balloon_box.right_pump()




