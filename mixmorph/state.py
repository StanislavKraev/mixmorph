

class State:
    def __init__(self, state_id: str, on_enter=None, on_exit=None):
        self._id = state_id
        self._on_enter=on_enter
        self._on_exit = on_exit

    @property
    def id(self):
        return self._id

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
        return f"State('{self._id}') [id={id(self)}]"
