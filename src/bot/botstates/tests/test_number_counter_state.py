from unittest.mock import MagicMock

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


    """
        when 100 users join 
        then assign players to each team evenly
    """

    def simulate_x_joins(x: int):
        for i in range(x):
            mockUserJoinContext.author.id = i
            numberCounter.handle_join(mockUserJoinContext)

    def get_team_counts():
        team_counts: dict[int, int] = {}
        for team_id in numberCounter.teams.values():
            team_counts[team_id] = team_counts.setdefault(team_id, 0) + 1
        return team_counts

    numberCounter = NumberCounterBot(num_teams=2, target_number=20)
    simulate_x_joins(100)
    test_team_counts = get_team_counts()
    assert test_team_counts[0] == 50
    assert test_team_counts[1] == 50

    numberCounter = NumberCounterBot(num_teams=3, target_number=20)
    simulate_x_joins(100)
    test_team_counts = get_team_counts()
    assert test_team_counts[0] == 34
    assert test_team_counts[1] == 33
    assert test_team_counts[2] == 33

    numberCounter = NumberCounterBot(num_teams=4, target_number=20)
    simulate_x_joins(100)
    test_team_counts = get_team_counts()
    assert test_team_counts[0] == 25
    assert test_team_counts[1] == 25
    assert test_team_counts[2] == 25
    assert test_team_counts[3] == 25

    numberCounter = NumberCounterBot(num_teams=100, target_number=20)
    simulate_x_joins(100)
    test_team_counts = get_team_counts()
    for i in range(100):
        assert test_team_counts[i] == 1


def test_event_message_handling():
    """
        when the number counter game has started
        then insert the number into the user's team's number's list
    """
    numberCounter = NumberCounterBot(num_teams=2, target_number=20)
    mockMessageContext = MagicMock()
    mockMessageContext.author.id = 1
    mockMessageContext.message.clean_content = "1"
    numberCounter.handle_event_message(mockMessageContext)
    numberCounter.team_numbers[0] == [1]

    """
        when 4 teams are competing cycle through 1-target_number - 1 for each team
        then 1 team completes all numbers and the win method should be called with 
             their number
    """
    target_number = 20
    num_teams = 4
    numberCounter = NumberCounterBot(num_teams=num_teams, target_number=target_number)
    mockMessageContext = MagicMock()
    numberCounter.teams = {0: 0, 1: 1, 2: 2, 3: 3}
    numberCounter.win = MagicMock()
    botState = BotStateContext(numberCounter)
    for i in range(target_number):
        for author_id in range(num_teams):
            mockMessageContext.author.id = author_id
            mockMessageContext.message.clean_content = str(i)
            botState.handle_event_message(mockMessageContext)


    mockMessageContext.send.assert_not_called()
    mockMessageContext.author.id = 1
    mockMessageContext.message.clean_content = str(target_number)
    botState.handle_event_message(mockMessageContext)
    numberCounter.win.assert_called_once_with(1, mockMessageContext)

    """
        when duplicates are sent 
        then win is not called
    """
    numberCounter = NumberCounterBot(num_teams=2, target_number=2)
    numberCounter.teams = {0: 0, 1: 1}

    mockMessageContext = MagicMock()
    mockMessageContext.author.id = 0

    numberCounter.win = MagicMock()
    botState = BotStateContext(numberCounter)
    for i in range(50):
        mockMessageContext.message.clean_content = "1"
        botState.handle_join(mockMessageContext)

    numberCounter.win.assert_not_called()