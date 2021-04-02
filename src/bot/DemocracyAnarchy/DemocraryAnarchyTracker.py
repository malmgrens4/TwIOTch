from asyncio import sleep
from typing import Dict, Callable


class AnarchyDemocracyTracker:
    # weight of anarchy
    # weight of democracy
    def __init__(self, callback: Callable[[], None], interval:int = 1, anarchy: int = .5, democracy: int = 5):
        self.anarchy = .5
        self.democracy = .5
        self.callback = callback

    async def start(self):
        # loop through
        # separate loop that executes this bad boy???
        await sleep(1)
        self.callback()


    @property
    def anarchy(self):
        return self.anarchy

    @anarchy.setter
    def anarchy(self, anarchy):
        self._anarchy = anarchy

    @property
    def democracy(self):
        return self.democracy

    @democracy.setter
    def democracy(self, democracy):
        self._democracy = democracy
