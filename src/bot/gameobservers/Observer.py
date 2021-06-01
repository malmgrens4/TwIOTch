from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.bot.gameobservers.Subject import Subject


class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """
        Receive update from subject.
        """
        pass

    @abstractmethod
    def on_abort(self, subject: Subject) -> None:
        """
        In the event a round is cancelled while it's occurring
        This method will be called to cancel any scheduled tasks
        or make necessary announcements
        """
