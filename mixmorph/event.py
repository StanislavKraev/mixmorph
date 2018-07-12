
class Event:
    def __init__(self, event_id):
        self._event_id = event_id

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        return self._event_id == other._event_id

    @property
    def id(self):
        return self._event_id

    def __repr__(self):
        return f"Event({self._event_id})"
