import os
from pathlib import Path

import pytest

from mixmorph import SCProcessor
from mixmorph.loaders import SCFileLoader


@pytest.fixture
def sc_file_loader(cases_path):
    return SCFileLoader(str(Path(cases_path) / "simple1.scxml"))


@pytest.fixture
def sc_processor(sc_file_loader):
    processor = SCProcessor(sc_file_loader)
    return processor


@pytest.fixture
def cases_path():
    return os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), "../cases/")))
