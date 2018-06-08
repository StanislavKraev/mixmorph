

class StatechartContext:

    def __init__(self):
        self._state = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state
