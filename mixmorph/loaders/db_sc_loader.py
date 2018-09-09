from typing import List

from mixmorph import Statechart
from mixmorph.loaders import StatechartLoader


class PostgresScLoader(StatechartLoader):
    schema = 'postgres'

    async def load(self, **kwargs) -> List[Statechart]:
        raise NotImplementedError()
