from typing import List, Dict

from mixmorph import State, Transition, StatechartContext


class Statechart:

    def __init__(self, states: dict, initial_state: State, state_transitions: Dict[str, List[Transition]]):
        self._states = states
        self._initial_state = initial_state
        self._state_transitions = state_transitions
        self._context: StatechartContext = None

    @property
    def initial_state(self):
        return self._initial_state

    def transitions(self, _state_id: str) -> List[Transition]:
        return self._state_transitions.get(_state_id, [])

    @property
    def context(self) -> StatechartContext:
        return self._context

    @context.setter
    def context(self, new_context: StatechartContext):
        self._context = new_context

    @property
    def state(self):
        return self._context.state

    @state.setter
    def state(self, new_state):
        self._context.state = new_state