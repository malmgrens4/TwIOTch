from twitchio.dataclasses import Message
from src.bot.botstates.BotState import BotState


class DefaultBot(BotState):

    async def handle_event_message(self, msg: Message) -> None:
        pass

    async def handle_join(self, msg: Message) -> None:
        pass

    async def can_join(self, msg: Message) -> bool:
        return True
