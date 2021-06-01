from __future__ import annotations
from sqlalchemy.exc import DBAPIError, DisconnectionError, SQLAlchemyError
import logging

from src.bot.gameobservers.Observer import Observer
from src.bot.botstates.TeamGameHandler import TeamGameHandler
from src.bot.db.schema import session_scope, User, Team


class WinGameChatObserver(Observer):
    def __init__(self):
        pass

    async def update(self, subject: TeamGameHandler) -> None:
        if subject.won and len(subject.team_data.get_team_member_map().values()):
            logging.debug("Creating win display.")
            if subject.winning_team_id is not None:
                winning_team_ids = [subject.winning_team_id]
            else:
                winning_team_ids = subject.winning_team_ids

            winning_ids = []
            for team_id in winning_team_ids:
                for winner_id in subject.team_data.get_team_member_map()[team_id]:
                    winning_ids.append(winner_id)

            if len(winning_ids) == 0:
                return
            try:
                winning_user_names = self.get_usernames(winning_ids)
                winning_team_names = self.get_team_names(winning_team_ids)
            except DBAPIError as dp_api_err:
                logging.error(dp_api_err)
            except DisconnectionError as dis_err:
                logging.error(dis_err)
            except SQLAlchemyError as sql_err:
                logging.error(sql_err)
            except IndexError as index_err:
                logging.error(index_err)
            try:
                await subject.send_message(self.format_winner_list(winning_team_names))
                await subject.send_message(self.format_winner_list(winning_user_names))
            except Exception as err:
                logging.error(err)

    async def on_abort(self, subject: TeamGameHandler) -> None:
        await subject.send_message("No Contest! Game ended early.")

    @staticmethod
    def format_winner_list(winning_ids: [str]):
        if len(winning_ids) == 1:
            win_announcement = winning_ids[0] + " wins!"
        elif len(winning_ids) == 2:
            win_announcement = f"{winning_ids[0]} and {winning_ids[1]} win!"
        else:
            win_announcement = ", ".join(winning_ids[0::-1]) + ", and " + str(winning_ids[-1]) + " win!"

        return win_announcement

    @staticmethod
    def get_usernames(winning_ids: [str]) -> [str]:
        with session_scope() as session:
            # TODO see if there's a better way to flatten this.
            winning_user_names = \
                [col[0] for col in session.query(User.name)
                    .filter(User.id.in_(winning_ids)).all()]
        return winning_user_names

    @staticmethod
    def get_team_names(winning_team_ids: [str]) -> str:
        with session_scope() as session:
            winning_team_names = [col[0] for col in session.query(Team.name)
                .filter(Team.id.in_([team_id + 1 for team_id in winning_team_ids])).all()]
        return winning_team_names
