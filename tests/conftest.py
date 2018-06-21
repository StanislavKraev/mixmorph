import os
from pathlib import Path

import pytest

from mixmorph import SCProcessor
from mixmorph.loaders import SCFileLoader


@pytest.fixture()
def simple_file_statechart():
    loader = SCFileLoader(str(Path(cases_path) / "simple1.scxml"))

    return loader.load()[0]


@pytest.fixture()
def activities_statechart():
    loader = SCFileLoader(str(Path(cases_path) / "activities.scxml"))

    return loader.load()[0]


@pytest.fixture
def sc_processor(sc_file_loader):
    processor = SCProcessor(sc_file_loader)
    return processor


@pytest.fixture(scope="session")
def cases_path():
    return os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), "../cases/")))
