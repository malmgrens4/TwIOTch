from unittest.mock import AsyncMock

import pytest

from src.bot.RoundsQueue import RoundsQueue, Round


class TestRoundQueue:
    @staticmethod
    def mock_round(on_round_start=None, on_round_end=None):
        if on_round_start is None:
            on_round_start = AsyncMock()
        if on_round_end is None:
            on_round_end = AsyncMock()

        return Round(on_round_start=on_round_start, on_round_end=on_round_end, name='test_round'), on_round_start, on_round_end

    @pytest.mark.asyncio
    async def test_round_function_order(self):
        """
        when there are two rounds ensure
        then their on_round_start and on_round_end functions
        are called in the correct order
        """
        round_one, one_start, one_end = self.mock_round()
        round_two, two_start, two_end = self.mock_round()

        rounds_queue = RoundsQueue(time_between_rounds=0, rounds=[])
        rounds_queue.add_round(round_one)
        rounds_queue.add_round(round_two)

        await rounds_queue.start()
        one_start.assert_called_once()
        len(rounds_queue.rounds) == 1

        await rounds_queue.end_round()
        one_end.assert_called_once()
        two_start.assert_called_once()

        await rounds_queue.end_round()
        two_end.assert_called_once()
        len(rounds_queue.rounds) == 0
