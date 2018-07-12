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
        return self.get_state(self._initial_state)

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

    def get_state(self, state_id: str) -> State:
        return self._states.get(state_id)

    def add_state(self, state_id: str, on_enter=None, on_exit=None):
        self._states[state_id] = State(
            state_id,
            on_enter=on_enter,
            on_exit=on_exit
        )

    def add_transition(self, state_id: str, event_id: str, target: Optional[str] = None, action=None):
        self._state_transitions.setdefault(state_id, []).append(Transition(event_id, target, action=action))
