import pytest

from unittest.mock import AsyncMock

from src.bot.botstates.Context import Context as BotStateContext
from src.bot.botstates.NumberCounterBot import NumberCounterBot


@pytest.mark.asyncio
async def test_event_message_handling():
    """
        when the game has not started
        then None is returned
    """
    user1_id = 1
    number_counter = NumberCounterBot(num_teams=2, target_number=20)
    # user 1 is on team 0
    number_counter.teams = {1: 0}

    mock_message_context = AsyncMock()
    mock_message_context.author.id = user1_id
    mock_message_context.content = "1"
    await number_counter.handle_event_message(mock_message_context)

    assert len(number_counter.team_numbers[0]) == 0


    """
        when 4 teams are competing cycle through 1-target_number - 1 for each team
        then 1 team completes all numbers and the win method should be called with 
             their number
    """
    target_number = 20
    num_teams = 4
    number_counter = NumberCounterBot(num_teams=num_teams, target_number=target_number)
    await number_counter.game_start()

    mock_message_context = AsyncMock()
    number_counter.teams = {0: 0, 1: 1, 2: 2, 3: 3}
    number_counter.win = AsyncMock()
    bot_state = BotStateContext(number_counter)
    for i in range(target_number):
        for author_id in range(num_teams):
            mock_message_context.author.id = author_id
            mock_message_context.content = str(i)
            await bot_state.handle_event_message(mock_message_context)

    mock_message_context.send.assert_not_called()
    mock_message_context.author.id = 1
    mock_message_context.content = str(target_number)
    await bot_state.handle_event_message(mock_message_context)
    number_counter.win.assert_called_once_with(1)

    """
        when duplicates are sent 
        then win is not called
    """
    number_counter = NumberCounterBot(num_teams=2, target_number=2)
    await number_counter.game_start()
    number_counter.teams = {0: 0, 1: 1}

    mock_message_context = AsyncMock()
    mock_message_context.author.id = 0

    number_counter.win = AsyncMock()
    bot_state = BotStateContext(number_counter)
    for i in range(50):
        mock_message_context.content = "1"
        await bot_state.handle_join(mock_message_context)

    number_counter.win.assert_not_called()
