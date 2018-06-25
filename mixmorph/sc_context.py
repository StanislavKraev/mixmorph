from mixmorph import State


class StatechartContext:

    def __init__(self):
        self._state = None
        self._id = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = State(new_state) if isinstance(new_state, str) else new_state
