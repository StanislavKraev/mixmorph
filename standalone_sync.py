import warnings

import syncer

from mixmorph import Statechart, State, Event, StatechartContext
from mixmorph.server.mm_server import StatechartProcessor


def on_enter_a(sc):
    pass


def on_enter_b(sc):
    pass


def on_enter_c(sc):
    pass


def some_action(sc):
    pass


def create_sc():
    statechart = Statechart()

    s1 = State("a")
    s2 = State("b")
    s3 = State("c")

    statechart.add_state(s1)
    statechart.add_state(s2)
    statechart.add_state(s3)

    statechart.add_transition(s1, Event("alpha"), target=s2)
    statechart.add_transition(s2, Event("beta"), target=s3)
    statechart.add_transition(s2, Event("gamma"), action=some_action)

    statechart.initial_state = s1

    return statechart


def main():
    sc = create_sc()
    context = StatechartContext()
    context.state = sc.initial_state

    _s = syncer.sync

    processor = StatechartProcessor(sc, context)
    _s(processor.on(Event("alpha")))
    _s(processor.on(Event("alpha")))
    _s(processor.on(Event("beta")))
    _s(processor.on(Event("gamma")))


if __name__ == "__main__":
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        main()
