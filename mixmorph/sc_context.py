from typing import List


class StatechartContext:

    def __init__(self):
        self._state = []
        self._id = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state: List[str]):
        self._state = new_state
