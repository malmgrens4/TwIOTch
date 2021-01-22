import logging

from src.bot.botstates import BotState

log = logging.getLogger(__name__)


class Context:

    _state = None

    def __init__(self, state: BotState) -> None:
        self.transition_to(state)

    def transition_to(self, state: BotState):
        log.debug(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    async def handle_event_message(self, ctx):
        await self._state.handle_event_message(ctx)

    async def handle_join(self, ctx):
        await self._state.handle_join(ctx)