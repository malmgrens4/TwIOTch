from .BotState import BotState


class DefaultBot(BotState):

    def handle_event_message(self, ctx) -> None:
        pass

    def handle_join(self, ctx) -> None:
        pass
