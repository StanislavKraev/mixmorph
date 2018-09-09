from mixmorph.loaders import SCFileLoader
from mixmorph.loaders.context_loader_impl import PostgresContextLoader
from mixmorph.loaders.db_sc_loader import PostgresScLoader


class Mixmorph:

    def __init__(self):
        self._charts = {}
        self._sc_loaders = {
            SCFileLoader.schema: SCFileLoader,
            PostgresScLoader.schema: PostgresScLoader
        }
        self._c_loaders = {
            PostgresContextLoader.schema: PostgresContextLoader
        }

    def register(self, statechart_id: str, statechart_loader, context_loader):
        if statechart_id in self._charts:
            raise KeyError()

        if isinstance(statechart_loader, str):      # URI
            statechart_inst = self._make_statechart_loader(statechart_loader)
        else:
            statechart_inst = statechart_loader

        if isinstance(context_loader, str):         # URI
            context_loader_inst = self._make_context_loader(context_loader)
        else:
            context_loader_inst = context_loader

        self._charts[statechart_id] = statechart_inst, context_loader_inst

    def create(self, statechart_id) -> bool:
        pass

    async def process(self, statechart, context_id, event):
        print(statechart, context_id, event)
        uri_info = self._parse_uri(statechart)
        if uri_info.schema not in self._sc_loaders:
            raise Exception(f'Unknown statechart type {uri_info.schema}')

        loader = self._sc_loaders[uri_info.schema]
        # todo

    def send(self):
        msg = Message(
            target_address,
            event,
            data
        )


    def _make_statechart_loader(self, loader_uri):
        uri_info = self._parse_uri(loader_uri)
        loader_cls = self._sc_loaders.get(uri_info.schema)
        assert loader_cls

        return loader_cls(*uri_info)

    def _make_context_loader(self, loader_uri):
        uri_info = self._parse_uri(loader_uri)
        loader_cls = self._c_loaders.get(uri_info.schema)
        assert loader_cls

        return loader_cls(*uri_info)

    def _parse_uri(self, uri):
        pass