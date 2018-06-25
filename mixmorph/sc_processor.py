from mixmorph import Event, StatechartContext
from mixmorph.loaders import StatechartLoader


class SCProcessor:

    def __init__(self, loader: StatechartLoader, context_loader):
        self._loader = loader
        self._context_loader = context_loader

    async def on(self, event: Event):
        statecharts = self._loader.load(event.id)
        print(f"{len(statecharts)} statechart(s) loaded")

        # context = StatechartContext()
        # context.state = "a"
        # self._context_loader.save(context)

        context = self._context_loader.load(1)
        for sc in statecharts:
            transitions = sc.transitions(context.state.id)
            print(f"{len(transitions)} transitions found for event {event.id}")
            for transition in transitions:
                if transition.event == event:
                    if transition.target:
                        context.state = transition.target
                        self._context_loader.save(context)
                        print(f"now state: {context.state}")
                else:
                    print(f"unprocessable event {event} in state {context.state}")