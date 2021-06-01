from collections import Callable
from src.bot.gameobservers.Subject import Subject


async def cancel(send_message: Callable[[str]], subject: Subject):
    for observer in subject.observers:
        await observer.on_abort(subject)
