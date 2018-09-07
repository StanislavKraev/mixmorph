import os

from mixmorph import State, Statechart, Transition, Event, StatechartContext
from mixmorph.loaders import StatechartNotExist, InvalidStatechartXML, StatechartLoader


def _load_state_element(el):
    state_id = el.attrib['id']
    state = State(state_id)

    transitions = {}
    for transition_element in el.findall('transition'):
        event_id = transition_element.attrib['event']
        if event_id in transitions:
            raise InvalidStatechartXML()

        target_state_id = transition_element.attrib.get('target')
        transition = Transition(
            event_id=event_id,
            target_id=target_state_id
        )
        transitions[event_id] = transition

    return state, transitions


class SCFileLoader(StatechartLoader):
    def __init__(self):
        self._sc_cache = {}

    async def load(self, path) -> Statechart:
        if path in self._sc_cache:
            return self._sc_cache[path]

        if not os.path.exists(path):
            raise StatechartNotExist(path)

        import xml.etree.ElementTree as ET
        try:
            tree = ET.parse(path)
        except Exception as e:
            raise InvalidStatechartXML()

        root = tree.getroot()

        if root.tag != "scxml":
            raise InvalidStatechartXML()

        if 'initial' in root.attrib:
            initial_state_id = root.attrib['initial']
        else:
            raise InvalidStatechartXML()

        states = {
        }
        initial_state = None

        transitions = {}

        for state_element in root.findall('state'):
            state_id = state_element.attrib['id']
            if not state_id:
                raise InvalidStatechartXML()
            if state_id in states:
                raise InvalidStatechartXML()
            state, state_transitions = _load_state_element(state_element)
            states[state_id] = state

            transitions[state_id] = list(state_transitions.values())

            if state.id == initial_state_id:
                initial_state = state

        if not initial_state:
            raise InvalidStatechartXML()

        statechart = Statechart()
        context = StatechartContext()
        context.state = initial_state
        statechart.context = context

        self._sc_cache[path] = statechart
        return statechart
