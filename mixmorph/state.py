

class State:
    def __init__(self, state_id: str):
        self._state_id = state_id
        self._on_enter = None
        self._on_exit = None

    @property
    def id(self):
        return self._state_id

    @property
    def on_enter(self):
        return self._on_enter

    @property
    def on_exit(self):
        return self._on_exit

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return other.id == self.id

    def __repr__(self):
        return f"State('{self._state_id}') [id={id(self)}]"

