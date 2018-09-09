from mixmorph import StatechartContext


class SCContextLoader:
    def __init__(self):
        self.hc_context = {
            '3': ['s1', 's3'],
            '2': ['s2', 's3'],
            '1': 's5'
        }

    async def load(self, statechart_id: str, context_id: str):
        if statechart_id == 'hardcode':
            c = self.hc_context.get(context_id)
            if c:
                states = c if isinstance(c, list) else [c]
                c_obj = StatechartContext()
                c_obj.state = states
                return c_obj
            return
        loader = StatechartContextLoader()
        await loader.init()
        return await loader.load(context_id)

    async def save(self, statechart_id: str, context):
        pass
