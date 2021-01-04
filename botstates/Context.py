from botstates.BotState import State


class Context:

    _state = None

    def __init__(self, state: State) -> None:
        self.transition_to(state)

    def transition_to(self, state: State):
        print(f"Context: Transition to {type(state).__name__}")
        self._state = state
        self._state.context = self

    def handle_event_message(self, ctx):
        self._state.handle_event_message(ctx)