import os
import pytest

from mixmorph import SCProcessor


@pytest.fixture
def sc_processor():
    processor = SCProcessor()
    return processor


@pytest.fixture
def cases_path():
    return os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), "../cases/")))
