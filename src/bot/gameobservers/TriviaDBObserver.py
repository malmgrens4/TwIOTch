from sqlalchemy.exc import DBAPIError, DisconnectionError, SQLAlchemyError
import logging

from src.bot.gameobservers.Observer import Observer
from src.bot.botstates.TriviaBot import TriviaBot
from src.bot.db.schema import session_scope, User

log = logging.getLogger(__name__)


class TriviaDBObserver(Observer):
    def __init__(self):
        pass

    async def update(self, subject: TriviaBot) -> None:
        if subject.won:
            correct_individuals = []
            for team_answers in subject.team_answers:
                correct_individuals.extend([k for k, v in team_answers.items if v in subject.correct_responses])

            try:
                with session_scope() as session:
                    winning_users = session.query(User).filter(User.id.in_(correct_individuals))
                    for user in winning_users:
                        user.trivia_wins += 1

            except DBAPIError as dp_api_err:
                log.error(dp_api_err)
            except DisconnectionError as dis_err:
                log.error(dis_err)
            except SQLAlchemyError as sql_err:
                log.error(sql_err)
            except IndexError as index_err:
                log.error(index_err)