from __future__ import annotations
from sqlalchemy.exc import DBAPIError, DisconnectionError, SQLAlchemyError
import logging

from src.bot.gameobservers.Observer import Observer
from src.bot.botstates.TriviaBot import TriviaBot
from src.bot.db.schema import session_scope, User, Team

log = logging.getLogger(__name__)


class TriviaChatObserver(Observer):
    def __init__(self):
        self.question_asked = False

    async def update(self, subject: TriviaBot) -> None:

        if not self.question_asked and subject._game_started:
            self.question_asked = True
            await subject.msg.channel.send("Question: %s" % subject.question)
            for key, value in subject.options.items():
                await subject.msg.channel.send("%s: %s" % (key, value))

        if subject.won and len(subject.get_team_member_map().values()):
            winning_ids = []
            for team_id in subject.winning_team_ids:
                for winner_id in subject.get_team_member_map()[team_id]:
                    winning_ids.append(winner_id)

            winning_team_names = None
            winning_user_names = []

            try:
                with session_scope() as session:
                    winning_user_names = \
                        [col[0] for col in session.query(User.name)
                            .filter(User.id.in_(winning_ids)).all()]

                    winning_team_names = [col[0] for col in session.query(Team.name)
                        .filter(Team.id.in_([team_id + 1 for team_id in subject.winning_team_ids])).all()]

            except DBAPIError as dp_api_err:
                log.error(dp_api_err)
            except DisconnectionError as dis_err:
                log.error(dis_err)
            except SQLAlchemyError as sql_err:
                log.error(sql_err)
            except IndexError as index_err:
                log.error(index_err)

            await subject.msg.channel.send("Team %s wins!" % winning_team_names)
            await subject.msg.channel.send("The following players win: %s" % winning_user_names)
