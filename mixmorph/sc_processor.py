import asyncio

from mixmorph import Event, Statechart


class SCProcessor:

    async def on(self, sc: Statechart, context, event: Event):

        transitions = sc.transitions(*context.state)
        print(f"{len(transitions)} transitions found in {context.state}")

        processed = False
        for transition in transitions:
            if transition.event == event.id:
                processed = True
                if transition.targets:
                    # if context.state.on_exit:
                    #     await asyncio.ensure_future(context.state.on_exit(sc))
                    context.state = transition.targets
                    print(f"now state: {context.state}")
                    # if context.state.on_enter:
                    #     await asyncio.ensure_future(context.state.on_enter(sc))
                if transition.action:
                    asyncio.ensure_future(transition.action(sc))
        if not processed:
            print(f"unprocessable event {event} in state {context.state}")
