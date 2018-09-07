import os

from mixmorph.hardcode_sc import HardcodeSC
from mixmorph.loaders import SCFileLoader


class SCLoader:
    def __init__(self):
        self._file_loader = SCFileLoader()

    async def load(self, statechart_id: str):
        if statechart_id == 'hardcode':
            return HardcodeSC()
        file_path = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), f"../../cases/{statechart_id}.scxml")))
        return await self._file_loader.load(file_path)
