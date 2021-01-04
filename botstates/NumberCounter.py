from botstates.BotState import BotState
from twitchio.dataclasses import Context


class NumberCounter(BotState):

    def __init__(self, teams, target_number):
        self.teams = teams
        self.team_numbers = [set() for _ in len(teams)]
        self.target_number = target_number

    def handle_event_message(self, ctx: Context) -> None:
        # if it's a number pass it to someone who cares
        # who is keeping track of the current numbers for each team? me?
        # how do we tell what team a member is on - we need a util method
        # check what team the member is on
        # TODO make this O(1) by placing members in a map pointing to team index
        # if the number is unique add it to the set
        # check the goal for each team
        # if a team has reached the required length
        # if 0 < num <= target_number (ints only)
        # create a win event for the given team based off certain criteria
        # transition to the default state

        pass
