from typing import List, Optional

from mixmorph import State, Transition, Event


class Statechart:

    def __init__(self):
        # , states: dict, initial_state: State, state_transitions: Dict[str, List[Transition]]
        self._states = {}
        self._initial_state = None
        self._state_transitions = {}
        self._state = None

    @property
    def initial_state(self):
        return self._initial_state

    @initial_state.setter
    def initial_state(self, value):
        self._initial_state = value

    def transitions(self, _state_id: str) -> List[Transition]:
        return self._state_transitions.get(_state_id, [])

    @property
    def state(self) -> State:
        return self._state

    @state.setter
    def state(self, new_state: State):
        self._state = new_state

    def add_state(self, state: State):
        self._states[state.id] = state

    def add_transition(self, state: State, event: Event, target: Optional[State] = None, action=None):
        self._state_transitions.setdefault(state.id, []).append(Transition(event, target, action=action))
