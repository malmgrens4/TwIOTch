from botstates.BotState import BotState


class Context:

    _state = None

    def __init__(self, state: BotState) -> None:
        self.transition_to(state)

    def transition_to(self, state: BotState):
        print(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def handle_event_message(self, ctx):
        self._state.handle_event_message(ctx)

    def handle_join(self, ctx):
        self._state.handle_join(ctx)
