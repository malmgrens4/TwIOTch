import logging
from twitchio.dataclasses import Message

from src.bot.botstates import BotState


class Context:

    _state = None

    def __init__(self, state: BotState) -> None:
        self.transition_to(state)

    def transition_to(self, state: BotState):
        logging.debug(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    async def handle_event_message(self, msg: Message):
        await self._state.handle_event_message(msg)

    async def handle_join(self, msg: Message):
        await self._state.handle_join(msg)

    async def can_join(self, msg: Message):
        return await self._state.can_join(msg)
