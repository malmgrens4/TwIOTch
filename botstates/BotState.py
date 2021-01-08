from abc import ABC
from abc import abstractmethod
from botstates.Context import Context


class BotState(ABC):

    @property
    def context(self) -> Context:
        return self._context

    @context.setter
    def context(self, context: Context) -> None:
        self._context = context

    @abstractmethod
    def handle_event_message(self, ctx) -> None:
        pass

    @abstractmethod
    def handle_join(self, ctx) -> None:
        pass
