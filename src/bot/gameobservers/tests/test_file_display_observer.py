import pytest

from unittest import mock
from unittest.mock import AsyncMock, MagicMock


class TestTriviaObservers:
    @pytest.mark.asyncio
    async def test_file_display_observer(self):
        # when the game starts save image is created
        # when game ends
        # -> time between rounds_time/5 is >= 10 -> answer display created and image deleted after rounds_time/5
        # -> else -> no answers display is created and image is deleted
        pass