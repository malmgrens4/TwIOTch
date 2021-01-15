from unittest.mock import MagicMock

from src.bot.botstates.Context import Context as BotStateContext
from src.bot.botstates.NumberCounterBot import NumberCounterBot


def test_team_assignment():
    """
        when a new user joins
        then assign them to the team with the least number of users
        in the event of a tie min function uses the first in sequence
    """
    user1_id = 1
    user2_id = 2
    number_counter = NumberCounterBot(num_teams=2, target_number=20)

    mock_user_join_context = MagicMock()
    mock_user_join_context.author.id = user1_id

    number_counter.handle_join(mock_user_join_context)
    assert number_counter.teams[user1_id] == 0
    assert len(number_counter.teams.values()) == 1

    """
        when a second user joins
        then assign them to the other team (as it has the least users)
    """
    mock_user_join_context.author.id = user2_id
    number_counter.handle_join(mock_user_join_context)
    assert number_counter.teams[user2_id] == 1
    assert len(number_counter.teams.values()) == 2


    """
        when 100 users join 
        then assign players to each team evenly
    """

    def simulate_x_joins(x: int):
        for i in range(x):
            mock_user_join_context.author.id = i
            number_counter.handle_join(mock_user_join_context)

    def get_team_counts():
        team_counts: dict[int, int] = {}
        for team_id in number_counter.teams.values():
            team_counts[team_id] = team_counts.setdefault(team_id, 0) + 1
        return team_counts

    number_counter = NumberCounterBot(num_teams=2, target_number=20)
    simulate_x_joins(100)
    test_team_counts = get_team_counts()
    assert test_team_counts[0] == 50
    assert test_team_counts[1] == 50

    number_counter = NumberCounterBot(num_teams=3, target_number=20)
    simulate_x_joins(100)
    test_team_counts = get_team_counts()
    assert test_team_counts[0] == 34
    assert test_team_counts[1] == 33
    assert test_team_counts[2] == 33

    number_counter = NumberCounterBot(num_teams=4, target_number=20)
    simulate_x_joins(100)
    test_team_counts = get_team_counts()
    assert test_team_counts[0] == 25
    assert test_team_counts[1] == 25
    assert test_team_counts[2] == 25
    assert test_team_counts[3] == 25

    number_counter = NumberCounterBot(num_teams=100, target_number=20)
    simulate_x_joins(100)
    test_team_counts = get_team_counts()
    for i in range(100):
        assert test_team_counts[i] == 1


def test_event_message_handling():
    """
        when the number counter game has started
        then insert the number into the user's team's number's list
    """
    number_counter = NumberCounterBot(num_teams=2, target_number=20)
    mock_message_context = MagicMock()
    mock_message_context.author.id = 1
    mock_message_context.message.clean_content = "1"
    number_counter.handle_event_message(mock_message_context)
    number_counter.team_numbers[0] == [1]

    """
        when 4 teams are competing cycle through 1-target_number - 1 for each team
        then 1 team completes all numbers and the win method should be called with 
             their number
    """
    target_number = 20
    num_teams = 4
    number_counter = NumberCounterBot(num_teams=num_teams, target_number=target_number)
    mock_message_context = MagicMock()
    number_counter.teams = {0: 0, 1: 1, 2: 2, 3: 3}
    number_counter.win = MagicMock()
    bot_state = BotStateContext(number_counter)
    for i in range(target_number):
        for author_id in range(num_teams):
            mock_message_context.author.id = author_id
            mock_message_context.message.clean_content = str(i)
            bot_state.handle_event_message(mock_message_context)

    mock_message_context.send.assert_not_called()
    mock_message_context.author.id = 1
    mock_message_context.message.clean_content = str(target_number)
    bot_state.handle_event_message(mock_message_context)
    number_counter.win.assert_called_once_with(1, mock_message_context)

    """
        when duplicates are sent 
        then win is not called
    """
    number_counter = NumberCounterBot(num_teams=2, target_number=2)
    number_counter.teams = {0: 0, 1: 1}

    mock_message_context = MagicMock()
    mock_message_context.author.id = 0

    number_counter.win = MagicMock()
    bot_state = BotStateContext(number_counter)
    for i in range(50):
        mock_message_context.message.clean_content = "1"
        bot_state.handle_join(mock_message_context)

    number_counter.win.assert_not_called()
