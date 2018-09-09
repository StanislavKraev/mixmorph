import asyncio
from asyncio.futures import InvalidStateError

import asynqp

from mixmorph import Event
from mixmorph.server.errors import UnprocessableEvent, ContextNotFound

locks = {}


def get_sc_context_lock(statechart_id: str, context_id: str):
    k = f"{statechart_id}/{context_id}"
    lock = locks.setdefault(k, asyncio.Lock())
    return lock


class MMServer:

    def __init__(self, mixmorph, queue='mm-general-queue'):
        self._mm = mixmorph

        self._CONSUMER = None
        self._PRODUCER = None
        self._CHANNELS = []
        self._queue = queue

    def run(self):
        self._loop = asyncio.get_event_loop()
        self._loop.set_exception_handler(self.connection_lost_handler)
        self._loop.create_task(self.start())
        self._loop.run_forever()

    async def start(self):
        try:
            connection = await self._setup_connection()
            self._CONSUMER = await self.setup_consumer(connection)
            self._PRODUCER = self._loop.create_task(self._setup_producer(connection))

        except Exception:
            print('failed to connect, trying again.')
            await asyncio.sleep(1)
            self._loop.create_task(self.start())

    async def _setup_producer(self, connection):
        exchange, _ = await self.setup_exchange_and_queue(connection)

        count = 0
        while True:
            msg = asynqp.Message({
                'scid': "hardcode",      # statechart id
                'cid': "1",             # context object id
                'event': "alpha"
            })
            exchange.publish(msg, self._queue)

            msg = asynqp.Message({
                'scid': "hardcode",   # statechart id
                'cid': "2",             # context object id
                'event': "beta"
            })
            exchange.publish(msg, self._queue)

            msg = asynqp.Message({
                'scid': "hardcode",     # statechart id
                'cid': "3",             # context object id
                'event': "gamma"
            })
            exchange.publish(msg, self._queue)
            await asyncio.sleep(1)
            # yield
            count += 1

    def connection_lost_handler(self, context):
        """
        Here we setup a custom exception handler to listen for
        ConnectionErrors.
        """
        exception = context.get('exception')
        if isinstance(exception, asynqp.exceptions.ChannelClosed):
            print('Connection lost -- trying to reconnect')
            # close everything before reconnecting
            close_task = self._loop.create_task(self.stop())
            asyncio.wait_for(close_task, None)
            # reconnect
            self._loop.create_task(self.start())
        else:
            # default behaviour
            self._loop.default_exception_handler(context)

    async def stop(self):
        """
        Cleans up connections, channels, consumers and producers
        when the connection is closed.
        """
        await self._CONSUMER.cancel()  # this is a coroutine
        self._PRODUCER.cancel()  # this is not

        for channel in self._CHANNELS:
            await channel.close()

        self._CHANNELS = []

        # TODO
        # if self._CONNECTION is not None:
        #     try:
        #         await self._CONNECTION.close()
        #     except InvalidStateError:
        #         pass  # could be automatically closed, so this is expected
        #     self._CONNECTION = None

    async def _setup_connection(self):
        connection = await asynqp.connect(
            'localhost',
            5672,
            username='guest',
            password='guest'
        )
        return connection

    async def setup_exchange_and_queue(self, connection):
        channel = await connection.open_channel()
        exchange = await channel.declare_exchange('general.exchange', 'direct')
        queue = await channel.declare_queue('mm.queue')
        self._CHANNELS.append(channel)

        await queue.bind(exchange, self._queue)
        return exchange, queue

    async def setup_consumer(self, connection):
        def callback(msg):
            try:
                self._loop.create_task(self.process_message(msg))
            except Exception as ex:
                print(ex)
            finally:
                msg.ack()

        _, queue = await self.setup_exchange_and_queue(connection)
        consumer = await queue.consume(callback)
        return consumer

    async def process_message(self, msg):
        msg_data = msg.json()
        sc_id = msg_data['scid']
        context_id = msg_data['cid']
        event = Event(msg_data['event'])

        await self._mm.process(sc_id, context_id, event)

        #
        # sc = await sc_loader.load(sc_id)
        # if not sc:
        #     raise UnprocessableEvent(sc_id, event)
        # context = await sc_context_loader.load(sc_id, context_id)
        # if not context:
        #     raise ContextNotFound(sc_id, context_id)
        #
        # context_lock = get_sc_context_lock(sc_id, context_id)
        # async with context_lock:
        #     sc_processor = StatechartProcessor(sc, context)
        #     await sc_processor.on(event)
        # await sc_context_loader.save(sc_id, sc_processor.context)
