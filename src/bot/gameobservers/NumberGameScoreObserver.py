from sqlalchemy.exc import DBAPIError, DisconnectionError, SQLAlchemyError
import logging

from src.bot.gameobservers.Observer import Observer
from src.bot.botstates.NumberCounterBot import NumberCounterBot
from src.bot.db.schema import session_scope, User

log = logging.getLogger(__name__)


class NumberGameScoreObserver(Observer):
    def __init__(self):
        pass

    async def update(self, subject: NumberCounterBot) -> None:
        if subject.won:
            winning_ids = subject.get_team_member_map()[subject.winning_team_id]
            try:
                with session_scope() as session:
                    winning_users = session.query(User).filter(User.id.in_(winning_ids))
                    for user in winning_users:
                        user.number_game_wins += 1

            except DBAPIError as dp_api_err:
                log.error(dp_api_err)
            except DisconnectionError as dis_err:
                log.error(dis_err)
            except SQLAlchemyError as sql_err:
                log.error(sql_err)
            except IndexError as index_err:
                log.error(index_err)
