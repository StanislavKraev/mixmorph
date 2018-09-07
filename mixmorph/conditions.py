
class StatechartCondition:
    pass


class IsInStateCondition:
    def __init__(self, *state_ids):
        if not state_ids:
            raise ValueError()
        self._state_ids = state_ids


def in_(*state_ids):
    return IsInStateCondition(*state_ids)
