from unittest.mock import MagicMock

from twitchio.dataclasses import Context
from twitchio.dataclasses import User

from ..Context import Context as BotStateContext
from ..NumberCounterBot import NumberCounterBot


def test_team_assignment():
    """
        when a new user joins
        then assign them to the team with the least number of users
        in the event of a tie min function uses the first in sequence
    """
    user1_id = 1
    user2_id = 2
    # 2 teams, 2 people join
    numberCounter = NumberCounterBot(num_teams=2, target_number=20)

    mockUserJoinContext = MagicMock()
    mockUserJoinContext.author.id = user1_id

    numberCounter.handle_join(mockUserJoinContext)
    assert numberCounter.teams[user1_id] == 0
    assert len(numberCounter.teams.values()) == 1

    """
        when a second user joins
        then assign them to the other team (as it has the least users)
    """
    mockUserJoinContext.author.id = user2_id
    numberCounter.handle_join(mockUserJoinContext)
    assert numberCounter.teams[user2_id] == 1
    assert len(numberCounter.teams.values()) == 2
