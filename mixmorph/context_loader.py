
import psycopg2

from mixmorph import StatechartContext


class StatechartContextLoader:
    def __init__(self):
        self.conn = psycopg2.connect("dbname='mm' user='postgres' host='127.0.0.1' password='postgres'")

    def load(self, oid):
        c = self.conn.cursor()
        c.execute("SELECT state FROM sc_context WHERE id=%(id)s", {'id': oid})

        result = c.fetchone()
        if not result:
            raise ValueError(f"Failed to find state context {oid}")

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        c.close()
        sc = StatechartContext()
        sc.state = result[0]
        sc._id = oid
        return sc

    def save(self, context):
        c = self.conn.cursor()

        c.execute("CREATE TABLE IF NOT EXISTS sc_context"
                  "(id SERIAL, state VARCHAR)")

        if not context._id:
            c.execute("INSERT INTO sc_context (state) VALUES (%(state)s)", {'state': context.state.id})
            context._id = c.lastrowid
        else:
            c.execute("UPDATE sc_context SET state=%(state)s WHERE id=%(id)s", {'state': context.state.id, 'id': context._id})
        # Save (commit) the changes
        self.conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        c.close()