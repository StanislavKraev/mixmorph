from mixmorph import Event
from mixmorph.state import State


def test_should_transit_from_a_to_b_when_event_alpha_triggered(sc_processor):
    sc_processor.on(Event(event_id="alpha"))
    assert State("b") == sc_processor.state


def test_should_not_transit_from_a_to_b_when_event_beta_triggered(sc_processor):
    sc_processor.on(Event(event_id="beta"))
    assert State("a") == sc_processor.state


def test_should_transit_from_a_to_c_when_events_alpha_beta_triggered(sc_processor):
    sc_processor.on(Event(event_id="alpha"))
    sc_processor.on(Event(event_id="beta"))
    assert State("c") == sc_processor.state
