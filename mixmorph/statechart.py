

class Statechart:

    def __init__(self, states, initial_state):
        self._states = states
        self._initial_state = initial_state

    @property
    def initial_state(self):
        return self._initial_state
