from typing import Optional


class Transition:
    def __init__(self, event_id: str, target_id: str = None, action=None):
        self._event = event_id
        self._target: str = target_id
        self._action = action

    @property
    def event(self) -> str:
        return self._event

    @property
    def target(self) -> Optional[str]:
        return self._target

    @property
    def action(self):
        return self._action
