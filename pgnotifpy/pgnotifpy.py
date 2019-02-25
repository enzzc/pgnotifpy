import select
import json
import psycopg2
import psycopg2.extensions


class Listener:
    def __init__(self, dbname, user, host=None):
        conn = psycopg2.connect(dbname=dbname, user=user, host=host)
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self._conn = conn
        self._table = {}

    def listen(self, action_name):
        def f(func):
            if action_name in self._table:
                self._table[action_name].append(func)
            else:
                self._table[action_name] = [func]
            return func
        return f

    def run(self, channel_name, dispatch_func):
        conn = self._conn
        curs = conn.cursor()
        curs.execute('LISTEN %s;' % channel_name)

        while True:
            if select.select([conn],[],[]) == ([],[],[]):
                pass
            else:
                conn.poll()
                while conn.notifies:
                    notify = conn.notifies.pop(0)
                    payload = notify.payload
                    try:
                        action, message = dispatch_func(payload)
                    except TypeError:
                        continue
                    else:
                        funcs = self._table.get(action, [])
                        for f in funcs:
                            res = f(message)

