import os
import pytest
from unittest.mock import MagicMock, patch, AsyncMock, DEFAULT
from src.bot.TeamData import TeamData
from src.bot.commandhandlers.trivia import start_trivia
from src.bot.commandhandlers.number_game import start_number_game


class TestTrivia:
    @staticmethod
    def return_trivia_data(self, category: str = None):
        question = MagicMock()
        question.question = "How in God's name is Howie Mandel so popular?"
        option = MagicMock()
        option.option = "There is no God."
        return (question, [option])

    @pytest.mark.asyncio
    async def test_trivia_start(self):
        """Verify that start_trivia_bot is called"""
        mocked_objects = {'WinGameChatObserver': DEFAULT,
                          'TriviaChatObserver': DEFAULT,
                          'TriviaDBObserver': DEFAULT,
                          'TriviaAnswerTimerObserver': AsyncMock,
                          'TriviaBot': DEFAULT}
        with patch.multiple('src.bot.commandhandlers.trivia',
                            **mocked_objects,
                            get_random_trivia=self.return_trivia_data) as values:

            trivia_bot_mock = AsyncMock()
            trivia_bot_mock.attach = MagicMock()
            values['TriviaBot'].return_value = trivia_bot_mock
            message = AsyncMock()
            message.content = "!start_trivia"
            message.author.is_mod = True

            send_message_mock = AsyncMock()
            botState = AsyncMock()
            botState.transition_to = MagicMock()

            team_data = TeamData()
            team_data.teams = {1: 0}

            await start_trivia(send_message=send_message_mock, category=None, team_data=team_data, botState=botState)
            botState.transition_to.assert_called_once()
            values['TriviaBot'].return_value.game_start.assert_called_once()

    @pytest.mark.asyncio
    async def test_trivia_no_matching_category(self):
        with patch.multiple('src.bot.commandhandlers.trivia', get_random_trivia=lambda x: None):
            send_message_mock = AsyncMock()
            botState = AsyncMock()
            botState.transition_to = MagicMock()

            team_data = TeamData()
            team_data.teams = {1: 0}

            await start_trivia(send_message=send_message_mock, category=None,
                               team_data=team_data, botState=botState)

            botState.transition_to.assert_not_called()
            send_message_mock.assert_called_with("Failed to find any trivia questions. Try another category.")


class TestNumberGame:
    @pytest.mark.asyncio
    async def test_start_number_game(self):
        """tests number game starts with valid start input"""
        send_message_mock = AsyncMock()
        target_number = 20
        team_data = TeamData(2)

        botState = AsyncMock()
        botState.transition_to = MagicMock()

        mocked_objects = {}
        mocked_objects['WinGameChatObserver'] = AsyncMock
        mocked_objects['NumberGameScoreObserver'] = DEFAULT
        mocked_objects['NumberCounterBot'] = DEFAULT
        with patch.multiple('src.bot.commandhandlers.number_game', **mocked_objects) as values:
            number_counter_bot_mock = AsyncMock()
            number_counter_bot_mock.attach = MagicMock()
            values['NumberCounterBot'].return_value = number_counter_bot_mock

            await start_number_game(send_message=send_message_mock, team_data=team_data,
                                    botState=botState, target_number=target_number)

            values['NumberCounterBot'].return_value.game_start.assert_called_once()
