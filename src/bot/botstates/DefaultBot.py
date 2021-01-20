from twitchio.dataclasses import Context
from src.bot.botstates.BotState import BotState


class DefaultBot(BotState):

    async def handle_event_message(self, ctx: Context) -> None:
        pass

    async def handle_join(self, ctx: Context) -> None:
        pass
