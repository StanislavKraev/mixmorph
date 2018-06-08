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
