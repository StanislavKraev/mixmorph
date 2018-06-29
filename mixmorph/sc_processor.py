from mixmorph import Event


class SCProcessor:

    async def on(self, sc, context, event: Event):

        # context = StatechartContext()
        # context.state = "a"
        # self._context_loader.save(context)

        transitions = sc.transitions(context.state.id)
        print(f"{len(transitions)} transitions found for event {event.id}")
        for transition in transitions:
            if transition.event == event:
                if transition.target:
                    context.state = transition.target
                    print(f"now state: {context.state}")
            else:
                print(f"unprocessable event {event} in state {context.state}")