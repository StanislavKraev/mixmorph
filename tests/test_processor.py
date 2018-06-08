from pathlib import Path
import pytest

from mixmorph import SCProcessor, Event
from mixmorph.state import State


@pytest.fixture
def sc_processor_simple(sc_processor: SCProcessor, cases_path):
    sc_processor.load_from_file(str(Path(cases_path) / "simple1.scxml"))
    assert State("a") == sc_processor.state
    return sc_processor


def test_should_transit_from_a_to_b_when_event_alpha_triggered(sc_processor_simple):
    sc_processor_simple.on(Event(event_id="alpha"))
    assert State("b") == sc_processor_simple.state


def test_should_not_transit_from_a_to_b_when_event_beta_triggered(sc_processor_simple):
    sc_processor_simple.on(Event(event_id="beta"))
    assert State("a") == sc_processor_simple.state


def test_should_transit_from_a_to_c_when_events_alpha_beta_triggered(sc_processor_simple):
    sc_processor_simple.on(Event(event_id="alpha"))
    sc_processor_simple.on(Event(event_id="beta"))
    assert State("c") == sc_processor_simple.state
