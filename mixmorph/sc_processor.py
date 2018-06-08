from mixmorph import Event
from mixmorph.loaders import StatechartLoader


class SCProcessor:

    def __init__(self, loader: StatechartLoader):
        self._loader = loader

    def on(self, event: Event):
        statecharts = self._loader.load(event.id)

        for sc in statecharts:
            transitions = sc.transitions(sc.state.id)
            for transition in transitions:
                if transition.event == event:
                    if transition.target:
                        sc.state = transition.target

