from typing import Optional, List


class Transition:
    def __init__(
            self,
            event_id: str,
            target_ids: List[str] = None,
            action=None,
            condition=None
    ):
        self._event = event_id
        self._targets: str = target_ids
        self._action = action
        self._condition = condition

    @property
    def event(self) -> str:
        return self._event

    @property
    def targets(self) -> Optional[List[str]]:
        return self._targets

    @property
    def action(self):
        return self._action

    @property
    def condition(self):
        return self._condition
