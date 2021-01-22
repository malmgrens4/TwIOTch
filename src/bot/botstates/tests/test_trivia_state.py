from unittest.mock import AsyncMock

import pytest

from src.bot.botstates.TriviaBot import TriviaBot


@pytest.mark.asyncio
async def test_trivia_answers():
    """
    when two users submit their answers
    then the team answers have both user's and their answers
    """

    user1_id = 1
    user2_id = 2
    trivia_bot = TriviaBot(2, "Test question?", {'a': 'Option A', 'b': 'Option B'}, ['a'])

    trivia_bot.teams = {user1_id: 0, user2_id: 1}
    mock_message = AsyncMock()

    mock_message.author.id = user1_id
    mock_message.content = "a"

    await trivia_bot.game_start()

    await trivia_bot.handle_event_message(mock_message)

    assert trivia_bot.team_answers == [{user1_id: "a"}, {}]


@pytest.mark.asyncio
async def test_all_users_answered():
    user1_id = 1
    user2_id = 2
    trivia_bot = TriviaBot(2, "Test question?", {'a': 'Option A', 'b': 'Option B'}, ['a'])
    trivia_bot.end_game = AsyncMock()

    trivia_bot.teams = {user1_id: 0, user2_id: 1}
    mock_message = AsyncMock()

    mock_message.author.id = user1_id
    mock_message.content = "a"

    await trivia_bot.game_start()

    await trivia_bot.handle_event_message(mock_message)

    mock_message.author.id = user2_id
    mock_message.content = "b"

    await trivia_bot.handle_event_message(mock_message)

    trivia_bot.end_game.assert_called_once()


@pytest.mark.asyncio
async def test_invalid_trivia_answer():
    """
        when two users submit their answers
        then the team answers have both user's and their answers
    """

    user1_id = 1
    user2_id = 2
    trivia_bot = TriviaBot(2, "Test question?", {'a': 'Option A', 'b': 'Option B'}, ['a'])

    trivia_bot.teams = {user1_id: 0, user2_id: 1}
    mock_message = AsyncMock()

    mock_message.author.id = user1_id
    mock_message.content = "og pogchamp"

    await trivia_bot.game_start()

    await trivia_bot.handle_event_message(mock_message)

    assert trivia_bot.team_answers == [{}, {}]


@pytest.mark.asyncio
async def test_team_win():
    user1_id = 1
    user2_id = 2
    trivia_bot = TriviaBot(2, "Test question?", {'a': 'Option A', 'b': 'Option B'}, ['a'])
    trivia_bot.win = AsyncMock()

    trivia_bot.teams = {user1_id: 0, user2_id: 1}
    mock_message = AsyncMock()

    mock_message.author.id = user1_id
    mock_message.content = "a"

    await trivia_bot.game_start()

    await trivia_bot.handle_event_message(mock_message)

    mock_message.author.id = user2_id
    mock_message.content = "b"

    await trivia_bot.handle_event_message(mock_message)

    assert trivia_bot.get_tally() == [1, 0]

    trivia_bot.win.assert_called_once_with([0])


@pytest.mark.asyncio
async def test_early_end():
    user1_id = 1
    user2_id = 2
    trivia_bot = TriviaBot(2, "Test question?", {'a': 'Option A', 'b': 'Option B'}, ['a'])
    trivia_bot.win = AsyncMock()

    trivia_bot.teams = {user1_id: 0, user2_id: 1}
    mock_message = AsyncMock()

    mock_message.author.id = user1_id
    mock_message.content = "b"

    await trivia_bot.game_start()

    await trivia_bot.handle_event_message(mock_message)

    await trivia_bot.end_game()

    trivia_bot.win.assert_called_once_with([0, 1])


@pytest.mark.asyncio
async def test_second_answer_ignored():
    user1_id = 1
    user2_id = 2
    trivia_bot = TriviaBot(2, "Test question?", {'a': 'Option A', 'b': 'Option B'}, ['a'])
    trivia_bot.win = AsyncMock()

    trivia_bot.teams = {user1_id: 0, user2_id: 1}
    mock_message = AsyncMock()

    await trivia_bot.game_start()

    mock_message.author.id = user1_id
    mock_message.content = "b"

    await trivia_bot.handle_event_message(mock_message)

    mock_message.author.id = user1_id
    mock_message.content = "a"

    await trivia_bot.handle_event_message(mock_message)
    assert trivia_bot.team_answers == [{user1_id: "b"}, {}]
