from typing import Optional, List

from mixmorph import Statechart


class StatechartLoader:

    def load(self, event: Optional[str] = None) -> List[Statechart]:
        raise NotImplementedError()
