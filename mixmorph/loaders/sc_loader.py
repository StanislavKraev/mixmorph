from typing import Optional, List

from mixmorph import Statechart


class StatechartLoader:

    def load(self, **kwargs) -> List[Statechart]:
        raise NotImplementedError()
