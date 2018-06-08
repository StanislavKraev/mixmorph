from mixmorph import Event
from mixmorph.loaders import StatechartAlreadyInitialized
from mixmorph.loaders.file_loader import load_from_file


class SCProcessor:

    def __init__(self):
        self._state = None
        self._statechart = None

    def load_from_file(self, path: str):
        if self._statechart:
            raise StatechartAlreadyInitialized()

        self._statechart = load_from_file(path)
        self._state = self._statechart.initial_state

    def on(self, event: Event):
        transitions = self._statechart.transitions(self._state.id)
        for transition in transitions:
            if transition.event == event:
                if transition.target:
                    self._state = transition.target

    @property
    def state(self):
        return self._state
