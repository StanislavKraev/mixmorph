import warnings

import syncer

from mixmorph import Statechart, Event, StatechartContext
from mixmorph.server.mm_server import StatechartProcessor


async def on_enter_a(sc):
    print("on enter a")


async def on_enter_b(sc):
    print("on enter b")


async def on_enter_c(sc):
    print("on enter c")


async def on_exit_a(sc):
    print("on exit a")


async def on_exit_b(sc):
    print("on exit b")


async def on_exit_c(sc):
    print("on exit c")


async def some_action(sc):
    print("some action!")


def create_sc():
    statechart = Statechart()

    statechart.add_state("a", on_enter=on_enter_a, on_exit=on_exit_a)
    statechart.add_state("b", on_enter=on_enter_b, on_exit=on_exit_b)
    statechart.add_state("c", on_enter=on_enter_c, on_exit=on_exit_c)

    statechart.add_transition("a", "alpha", target="b")
    statechart.add_transition("b", "beta", target="c")
    statechart.add_transition("c", "gamma", action=some_action)

    statechart.initial_state = "a"

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
