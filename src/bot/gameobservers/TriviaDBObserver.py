from sqlalchemy.exc import DBAPIError, DisconnectionError, SQLAlchemyError
import os
import logging
from typing import Dict
from src.bot.gameobservers.Observer import Observer
from src.bot.botstates.TriviaBot import TriviaBot, TriviaResponse
from src.bot.db.schema import session_scope, User

log = logging.getLogger(__name__)


class TriviaDBObserver(Observer):
    trivia_max_response_time = int(os.environ['TRIVIA_RESPONSE_TIME_SECONDS']) * 1000

    def __init__(self):
        pass

    async def update(self, subject: TriviaBot) -> None:
        if subject.won:
            correct_user_responses: Dict[int, TriviaResponse] = {}
            for responses in subject.team_responses:
                for k, v in responses.items():
                    if v.answer in subject.correct_options:
                        correct_user_responses[k] = v

            try:
                with session_scope() as session:
                    winning_users = session.query(User).filter(User.id.in_(correct_user_responses.keys()))
                    for user in winning_users:
                        user.trivia_points += \
                            self.trivia_max_response_time - correct_user_responses[user.id].time_to_answer

            except DBAPIError as dp_api_err:
                log.error(dp_api_err)
            except DisconnectionError as dis_err:
                log.error(dis_err)
            except SQLAlchemyError as sql_err:
                log.error(sql_err)
            except IndexError as index_err:
                log.error(index_err)