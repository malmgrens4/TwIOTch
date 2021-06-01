from sqlalchemy.exc import DBAPIError, DisconnectionError, SQLAlchemyError
import logging

from src.bot.gameobservers.Observer import Observer
from src.bot.botstates.NumberCounterBot import NumberCounterBot
from src.bot.db.schema import session_scope, User
from src.bot.gameobservers.Subject import Subject


class NumberGameScoreObserver(Observer):

    def __init__(self):
        pass

    def on_abort(self, subject: Subject) -> None:
        pass

    async def update(self, subject: NumberCounterBot) -> None:
        if subject.won:
            logging.debug("Giving number game winners points.")
            winning_ids = subject.team_data.get_team_member_map()[subject.winning_team_id]
            try:
                with session_scope() as session:
                    winning_users = session.query(User).filter(User.id.in_(winning_ids))
                    for user in winning_users:
                        user.number_game_wins += 1

            except DBAPIError as dp_api_err:
                logging.error(dp_api_err)
            except DisconnectionError as dis_err:
                logging.error(dis_err)
            except SQLAlchemyError as sql_err:
                logging.error(sql_err)
            except IndexError as index_err:
                logging.error(index_err)

    async def on_abort(self, subject: NumberCounterBot) -> None:
        pass
