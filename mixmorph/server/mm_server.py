import asyncio
from asyncio.futures import InvalidStateError

import asynqp

from mixmorph import SCProcessor, Event
from mixmorph.server.context_loader import SCContextLoader
from mixmorph.server.errors import UnprocessableEvent, ContextNotFound
from mixmorph.server.statechart_loader import SCLoader

CHANNELS = []
CONNECTION = None
CONSUMER = None
PRODUCER = None

GENERAL_ROUTING = 'mm-general-queue'


async def setup_connection(loop):
    connection = await asynqp.connect(
        'localhost',
        5672,
        username='guest',
        password='guest'
    )
    return connection


async def setup_exchange_and_queue(connection):
    channel = await connection.open_channel()
    exchange = await channel.declare_exchange('general.exchange', 'direct')
    queue = await channel.declare_queue('mm.queue')
    CHANNELS.append(channel)

    await queue.bind(exchange, GENERAL_ROUTING)
    return exchange, queue


sc_loader = SCLoader()
sc_context_loader = SCContextLoader()

locks = {}


def get_sc_context_lock(statechart_id: str, context_id: str):
    k = f"{statechart_id}/{context_id}"
    lock = locks.setdefault(k, asyncio.Lock())
    return lock


class StatechartProcessor:
    def __init__(self, statechart, context):
        self._sc = statechart
        self._context = context

    async def on(self, event):
        p = SCProcessor()
        await p.on(self._sc, self._context, event)

    @property
    def context(self):
        return


async def process_message(msg):
    msg_data = msg.json()
    sc_id = msg_data['scid']
    context_id = msg_data['cid']
    event = Event(msg_data['event'])

    sc = await sc_loader.load(sc_id)
    if not sc:
        raise UnprocessableEvent(sc_id, event)
    context = await sc_context_loader.load(sc_id, context_id)
    if not context:
        raise ContextNotFound(sc_id, context_id)

    context_lock = get_sc_context_lock(sc_id, context_id)
    async with context_lock:
        sc_processor = StatechartProcessor(sc, context)
        await sc_processor.on(event)
    await sc_context_loader.save(sc_id, sc_processor.context)


async def setup_consumer(connection, loop):
    def callback(msg):
        try:
            loop.create_task(process_message(msg))
        except Exception as ex:
            print(ex)
        finally:
            msg.ack()

    _, queue = await setup_exchange_and_queue(connection)
    consumer = await queue.consume(callback)
    return consumer


async def setup_producer(connection):
    exchange, _ = await setup_exchange_and_queue(connection)

    count = 0
    while True:
        msg = asynqp.Message({
            'scid': "hardcode",      # statechart id
            'cid': "1",             # context object id
            'event': "alpha"
        })
        exchange.publish(msg, GENERAL_ROUTING)

        msg = asynqp.Message({
            'scid': "hardcode",   # statechart id
            'cid': "2",             # context object id
            'event': "beta"
        })
        exchange.publish(msg, GENERAL_ROUTING)

        msg = asynqp.Message({
            'scid': "hardcode",     # statechart id
            'cid': "3",             # context object id
            'event': "gamma"
        })
        exchange.publish(msg, GENERAL_ROUTING)
        await asyncio.sleep(1)
        # yield
        count += 1


async def start(loop):
    global CONNECTION
    global CONSUMER
    global PRODUCER
    try:
        CONNECTION = await setup_connection(loop)
        CONSUMER = await setup_consumer(CONNECTION, loop)
        PRODUCER = loop.create_task(setup_producer(CONNECTION))

    except Exception:
        print('failed to connect, trying again.')
        await asyncio.sleep(1)
        loop.create_task(start(loop))


async def stop():
    """
    Cleans up connections, channels, consumers and producers
    when the connection is closed.
    """
    global CHANNELS
    global CONNECTION
    global PRODUCER
    global CONSUMER

    await CONSUMER.cancel()  # this is a coroutine
    PRODUCER.cancel()  # this is not

    for channel in CHANNELS:
        await channel.close()
    CHANNELS = []

    if CONNECTION is not None:
        try:
            await CONNECTION.close()
        except InvalidStateError:
            pass  # could be automatically closed, so this is expected
        CONNECTION = None


def connection_lost_handler(loop, context):
    """
    Here we setup a custom exception handler to listen for
    ConnectionErrors.
    """
    exception = context.get('exception')
    if isinstance(exception, asynqp.exceptions.ChannelClosed):
        print('Connection lost -- trying to reconnect')
        # close everything before reconnecting
        close_task = loop.create_task(stop())
        asyncio.wait_for(close_task, None)
        # reconnect
        loop.create_task(start(loop))
    else:
        # default behaviour
        loop.default_exception_handler(context)


def main():
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(connection_lost_handler)
    loop.create_task(start(loop))
    loop.run_forever()


if __name__ == "__main__":
    main()
