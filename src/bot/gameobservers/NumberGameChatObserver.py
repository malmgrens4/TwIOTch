from __future__ import annotations
from sqlalchemy.exc import DBAPIError, DisconnectionError, SQLAlchemyError
import logging

from src.bot.gameobservers.Observer import Observer
from src.bot.botstates.NumberCounterBot import NumberCounterBot
from src.bot.db.schema import session_scope, User, Team

log = logging.getLogger(__name__)


class NumberGameChatObserver(Observer):
    def __init__(self):
        pass

    async def update(self, subject: NumberCounterBot) -> None:
        if subject.won:
            winning_ids = subject.get_team_member_map()[subject.winning_team_id]
            winning_team_name = None
            winning_user_names = []

            try:
                with session_scope() as session:
                    # TODO see if there's a better way to flatten this.
                    winning_user_names = \
                        [col[0] for col in session.query(User.name)
                            .filter(User.id.in_(winning_ids)).all()]

                    winning_team_name = session.query(Team.name) \
                        .filter(Team.id == subject.winning_team_id + 1).all()[0][0]

            except DBAPIError as dp_api_err:
                log.error(dp_api_err)
            except DisconnectionError as dis_err:
                log.error(dis_err)
            except SQLAlchemyError as sql_err:
                log.error(sql_err)
            except IndexError as index_err:
                log.error(index_err)

            await subject.msg.channel.send("Team %s wins!" % winning_team_name)
            await subject.msg.channel.send("The following players win: %s" % (", ".join(winning_user_names)))
