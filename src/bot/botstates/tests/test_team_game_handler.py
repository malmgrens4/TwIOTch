from unittest.mock import AsyncMock

import pytest

from src.bot.TeamData import TeamData

@pytest.mark.asyncio
async def test_team_data_assignment():
    """
        when a new user joins
        then assign them to the team with the least number of users
        in the event of a tie min function uses the first in sequence
    """
    user1_id = 1
    user2_id = 2
    team_data = TeamData(2)

    mock_user_join_context = AsyncMock()
    mock_user_join_context.author.id = user1_id

    await team_data.handle_join(mock_user_join_context)
    assert team_data.teams[user1_id] == 0
    assert len(team_data.teams.values()) == 1

    """
        when a second user joins
        then assign them to the other team (as it has the least users)
    """

    mock_user_join_context.author.id = user2_id
    await team_data.handle_join(mock_user_join_context)
    assert team_data.teams[user2_id] == 1
    assert len(team_data.teams.values()) == 2


    """
        when 100 users join 
        then assign players to each team evenly
    """

    async def simulate_x_joins(x: int):
        for i in range(x):
            mock_user_join_context.author.id = i
            await team_data.handle_join(mock_user_join_context)

    def get_team_counts():
        team_counts: dict[int, int] = {}
        for team_id in team_data.teams.values():
            team_counts[team_id] = team_counts.setdefault(team_id, 0) + 1
        return team_counts

    await simulate_x_joins(100)
    test_team_counts = get_team_counts()
    assert test_team_counts[0] == 50
    assert test_team_counts[1] == 50

    team_data = TeamData(3)
    await simulate_x_joins(100)
    test_team_counts = get_team_counts()
    assert test_team_counts[0] == 34
    assert test_team_counts[1] == 33
    assert test_team_counts[2] == 33

    team_data = TeamData(4)
    await simulate_x_joins(100)
    test_team_counts = get_team_counts()
    assert test_team_counts[0] == 25
    assert test_team_counts[1] == 25
    assert test_team_counts[2] == 25
    assert test_team_counts[3] == 25

    team_data = TeamData(100)
    await simulate_x_joins(100)
    test_team_counts = get_team_counts()
    for i in range(100):
        assert test_team_counts[i] == 1

