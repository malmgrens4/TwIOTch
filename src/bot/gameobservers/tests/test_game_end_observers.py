import pytest

from unittest import mock
from unittest.mock import AsyncMock, MagicMock
from src.bot.gameobservers.WinGameChatObserver import WinGameChatObserver


class TestNumberGameObservers:
    @pytest.mark.asyncio
    async def test_win_chat_announce_winners(self):
        """test winning messages are called when the game is over"""
        mock_subject = AsyncMock()

        mock_subject.won = True
        mock_subject.winning_team_id = 1

        team_one = "Team 1"
        team_names = ["User 1", "User 2"]

        mock_subject.team_data = MagicMock()
        mock_subject.team_data.get_team_member_map = MagicMock()
        mock_subject.team_data.get_team_member_map.return_value = {1: ['id1', 'id2']}
        winGameChatObserver = WinGameChatObserver()
        winGameChatObserver.get_team_name = MagicMock()
        winGameChatObserver.get_team_name.return_value = team_one
        winGameChatObserver.get_usernames = MagicMock()
        winGameChatObserver.get_usernames.return_value = team_names

        await winGameChatObserver.update(mock_subject)
        mock_subject.send_message.assert_called()
