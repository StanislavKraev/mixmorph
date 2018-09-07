from typing import List, Optional

from mixmorph import State, Transition
from mixmorph.conditions import StatechartCondition


class Statechart:

    def __init__(self, sc_id: str = None):
        self._sc_id = sc_id

        self._states = {}
        self._statecharts = {}

        self._initial_state = None
        self._state_transitions = {}

    def add_state(self, state_id: str) -> State:
        state = State(state_id)
        self._states[state_id] = state
        return state

    def add_statechart(self, statechart_id: str):
        sc = Statechart(statechart_id)
        self._statecharts[statechart_id] = sc
        return sc

    def add_transition(
            self,
            source_id: str,
            event_id: str,
            target: Optional[str] = None,
            targets: Optional[List[str]] = None,
            condition: StatechartCondition = None
    ):
        """
        :param source_id: state id or statechart id
        :param event_id:
        :param target: target state or statechart id
        :param targets: list of target state ids or statechart ids
        :param condition: transition condition
        """
        assert target or targets
        transition = Transition(event_id, targets or [target], condition=condition)
        self._state_transitions.setdefault(source_id, []).append(transition)
        return transition

    def transitions(self, *states) -> List[Transition]:
        all_transitions = []
        for s in states:
            all_transitions.extend(self._state_transitions.get(s, []))
        return all_transitions

    def get_state(self, state_id: str) -> State:
        return self._states.get(state_id)
