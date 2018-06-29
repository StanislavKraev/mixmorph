
import asyncio
from aiopg.sa import create_engine
import sqlalchemy as sa


from mixmorph import StatechartContext


metadata = sa.MetaData()
tbl = sa.Table(
    'sc_context', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('state', sa.String)
)


class StatechartContextLoader:
    def __init__(self):
        self.engine = None

    async def init(self):
        self.engine = await create_engine(
            user='postgres',
            database='mm',
            host='127.0.0.1',
            password='postgres'
        )

    async def load(self, oid):
        async with self.engine.acquire() as conn:
            for row in await conn.execute("SELECT state FROM sc_context WHERE id=%(id)s", {'id': oid}):
                sc = StatechartContext()
                sc.state = row[0]
                sc._id = oid
                return sc

    async def save(self, context):
        async with self.engine.acquire() as conn:
            await conn.execute('DROP TABLE IF EXISTS tbl')
            await conn.execute("""CREATE TABLE tbl (id serial PRIMARY KEY, val varchar(255))""")

            tx = await conn.begin()
            try:
                if not context._id:
                    await conn.execute("INSERT INTO sc_context (state) VALUES (%(state)s)", {'state': context.state.id})
                    context._id = conn.lastrowid
                else:
                    await conn.execute("UPDATE sc_context SET state=%(state)s WHERE id=%(id)s", {'state': context.state.id, 'id': context._id})
                await tx.commit()
            except Exception:
                await tx.rollback()



