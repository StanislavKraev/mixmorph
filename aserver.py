import os

from aiohttp import web
from aiohttp.web_request import Request

from mixmorph import SCProcessor, Event
from mixmorph.context_loader import StatechartContextLoader
from mixmorph.loaders import SCFileLoader


async def post_event(request: Request):
    event = request.query.get('event')
    sc_processor: SCProcessor = request.app['sc_processor']
    await sc_processor.on(Event(event))
    return web.Response(text=f"Event received: {event}")


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


def main():
    file_path = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), "cases/simple1.scxml")))
    app = web.Application()
    app.add_routes([
        web.get('/', handle),
        web.get('/{name}', handle),
        web.get('/send/', post_event)
    ])

    app['sc_processor'] = SCProcessor(loader=SCFileLoader(file_path), context_loader=StatechartContextLoader())
    web.run_app(app)


if __name__ == "__main__":
    main()
