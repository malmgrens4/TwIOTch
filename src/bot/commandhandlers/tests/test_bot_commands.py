import pytest
from unittest.mock import MagicMock, patch, AsyncMock, DEFAULT
from src.bot.TeamData import TeamData
from src.bot.commandhandlers.trivia import start_trivia


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

        mocked_objects = {}
        mocked_objects['TriviaChatObserver'] = DEFAULT
        mocked_objects['TriviaAnswerTimerObserver'] = AsyncMock
        mocked_objects['TriviaBot'] = DEFAULT
        with patch.multiple('src.bot.commandhandlers.trivia', **mocked_objects, get_random_trivia=self.return_trivia_data) as values:
            values['TriviaBot'].return_value = AsyncMock()
            message = AsyncMock()
            message.content = "!start_trivia"
            message.author.is_mod = True

            botState = AsyncMock()

            team_data = TeamData()
            team_data.teams = {1: 0}

            await start_trivia(message, team_data, botState)
            botState.transition_to.assert_called_once()
            values['TriviaBot'].return_value.game_start.assert_called_once()

    @pytest.mark.asyncio
    async def test_trivia_no_matching_category(self):
        with patch.multiple('src.bot.commandhandlers.trivia', get_random_trivia=lambda x: None):
            message = AsyncMock()
            message.content = "!start_trivia"
            message.author.is_mod = True

            botState = AsyncMock()

            team_data = TeamData()
            team_data.teams = {1: 0}

            await start_trivia(message, team_data, botState)
            botState.transition_to.assert_not_called()
            message.channel.send.assert_called_with("Failed to find any trivia questions. Try another category.")


class TestNumberGame