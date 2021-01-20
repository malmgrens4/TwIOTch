from __future__ import annotations
from src.bot.gameobservers.Observer import Observer
from src.bot.botstates.NumberCounterBot import NumberCounterBot


class NumberGameChatObserver(Observer):
    def __init__(self):
        pass

    async def update(self, subject: NumberCounterBot) -> None:
        if subject.won:
            winning_ids = subject.get_team_member_map()[subject.winning_team_id]
            await subject.msg.channel.send("Team %s wins!" % subject.winning_team_id)
            await subject.msg.channel.send("The following players win: %s" % winning_ids)
