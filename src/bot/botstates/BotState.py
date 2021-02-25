from abc import ABC
from abc import abstractmethod
from twitchio.dataclasses import Message
from src.bot.botstates import Context


class BotState(ABC):

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    async def can_join(self, msg: Message) -> bool:
        pass

    @abstractmethod
    async def handle_event_message(self, msg: Message) -> None:
        pass

    @abstractmethod
    async def handle_join(self, msg: Message) -> None:
        pass
