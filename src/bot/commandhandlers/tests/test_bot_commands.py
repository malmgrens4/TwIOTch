import pytest
from unittest.mock import AsyncMock
from src.bot.TeamData import TeamData
from src.bot.commandhandlers.trivia import start_trivia
from src.bot.botstates.BotState import BotState


@pytest.mark.asyncio
async def test_trivia_start():
    """Verify that start_trivia_bot is called"""
    message = AsyncMock()
    message.content = "!start_trivia"
    botState = AsyncMock()
    team_data = TeamData()
    team_data.teams = {1: 0}
    await start_trivia(message, team_data, botState)
