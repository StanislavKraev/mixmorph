import os

from mixmorph import State, Statechart
from mixmorph.loaders import StatechartNotExist, InvalidStatechartXML


def _state_from_element(el):
    state_id = el.attrib['id']
    state = State(state_id)
    return state


def load_from_file(path: str) -> Statechart:
    if not os.path.exists(path):
        raise StatechartNotExist(path)

    import xml.etree.ElementTree as ET
    try:
        tree = ET.parse(path)
    except Exception:
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

    for state_element in root.findall('state'):
        state_id = state_element.attrib['id']
        if not state_id:
            raise InvalidStatechartXML()
        if state_id in states:
            raise InvalidStatechartXML()
        state = _state_from_element(state_element)
        states[state_id] = state

        if state.id == initial_state_id:
            initial_state = state

    if not initial_state:
        raise InvalidStatechartXML()

    statechart = Statechart(
        states,
        initial_state
    )
    return statechart
