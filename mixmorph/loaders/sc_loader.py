from typing import Optional, List

from mixmorph import Statechart


class StatechartLoader:

    async def load(self, **kwargs) -> List[Statechart]:
        raise NotImplementedError()
