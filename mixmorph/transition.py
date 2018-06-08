from typing import Optional

from mixmorph.state import State
from mixmorph.event import Event


class Transition:
    def __init__(self, event: Event, target: State = None):
        self._event = event
        self._target = target

    @property
    def event(self) -> Event:
        return self._event

    @property
    def target(self) -> Optional[State]:
        return self._target
