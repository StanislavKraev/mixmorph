

class State:
    def __init__(self, state_id: str):
        self._id = state_id

    @property
    def id(self):
        return self._id

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return other.id == self.id

    def __repr__(self):
        return f"State('{self._id}') [id={id(self)}]"
