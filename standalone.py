import asyncio

from mixmorph import Event, StatechartContext, Statechart, State
from mixmorph.server.mm_server import StatechartProcessor


async def some_action(sc):
    print("some action!")
    await asyncio.sleep(1.)
    asyncio.get_event_loop().stop()

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
    statechart.add_transition(s3, Event("gamma"), action=some_action)

    statechart.initial_state = s1

    return statechart


async def setup_sc():

    sc = create_sc()
    context = StatechartContext()
    context.state = sc.initial_state

    processor = StatechartProcessor(sc, context)
    asyncio.ensure_future(run_test(processor))


async def run_test(processor: StatechartProcessor):
    await processor.on(Event("alpha"))
    await processor.on(Event("alpha"))
    await processor.on(Event("beta"))
    await processor.on(Event("beta"))
    await processor.on(Event("gamma"))
    await processor.on(Event("alpha"))


def main():
    asyncio.ensure_future(setup_sc())
    loop = asyncio.get_event_loop()
    loop.run_forever()


if __name__ == "__main__":
    main()
