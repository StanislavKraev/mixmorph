from typing import List, Dict

from mixmorph import State, Transition


class Statechart:

    def __init__(self, states: dict, initial_state: State, state_transitions: Dict[str, List[Transition]]):
        self._states = states
        self._initial_state = initial_state
        self._state_transitions = state_transitions

    @property
    def initial_state(self):
        return self._initial_state

    def transitions(self, _state_id: str) -> List[Transition]:
        return self._state_transitions.get(_state_id, [])
