from abc import ABC
from abc import abstractmethod

from src.bot.botstates import Context


class BotState(ABC):

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    async def handle_event_message(self, ctx) -> None:
        pass

    @abstractmethod
    async def handle_join(self, ctx) -> None:
        pass
