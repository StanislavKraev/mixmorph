from pathlib import Path
import pytest

from mixmorph import SCProcessor, Event


@pytest.fixture
def sc_processor_simple(sc_processor: SCProcessor, cases_path):
    sc_processor.load_from_file(str(Path(cases_path) / "simple1.scxml"))
    return sc_processor


def test_should_transit_from_a_to_b_when_event_triggered(sc_processor_simple):
    sc_processor_simple.on(Event())
