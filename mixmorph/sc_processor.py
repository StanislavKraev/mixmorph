import asyncio
import functools

from mixmorph import Event


class SCProcessor:

    async def on(self, sc, context, event: Event):

        # context = StatechartContext()
        # context.state = "a"
        # self._context_loader.save(context)

        transitions = sc.transitions(context.state.id)
        print(f"{len(transitions)} transitions found in {context.state}")

        processed = False
        for transition in transitions:
            if transition.event == event:
                processed = True
                if transition.target:
                    context.state = transition.target
                    print(f"now state: {context.state}")
                if transition.action:
                    asyncio.ensure_future(transition.action(sc))
        if not processed:
            print(f"unprocessable event {event} in state {context.state}")