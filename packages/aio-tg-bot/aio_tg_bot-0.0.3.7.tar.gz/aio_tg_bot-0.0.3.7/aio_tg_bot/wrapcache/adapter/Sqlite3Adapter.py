import time
import sqlite3

from .BaseAdapter import BaseAdapter
from .CacheException import CacheExpiredException, DBNotSetException


class Sqlite3Adapter(BaseAdapter):
    path = "wrapcache.sqlite3"
    table_name = "wrapcache"

    def __init__(self, path=None, table_name=None, timeout=-1):
        if path is None:
            path = Sqlite3Adapter.path
        if table_name is None:
            table_name = Sqlite3Adapter.table_name

        self.path = path
        self._create_sql_querys(table_name)
        self._sql_execute(self._create_sql)

        super(Sqlite3Adapter, self).__init__(timeout=timeout)

    def get(self, key, check_timeout=True):
        value = self._sql_execute(self._get_sql, values=(key,))

        if check_timeout and time.time() - self._get_value_or(value, "time", 0) > 0:
            self.remove(key)
            raise CacheExpiredException(key)
        elif check_timeout is False and 0 == len(value):
            value = None
        else:
            value = value[-1][0]

        return value

    def set(self, key, value):
        self._sql_execute(self._set_sql, values=(key, value, time.time() + self.timeout))
        return True

    def remove(self, key):
        value = self.get(key, check_timeout=False)
        self._sql_execute(self._del_sql, values=(key,))
        return value

    def flush(self):
        self._sql_execute(self._clear_table_sql)
        return True

    def _create_sql_querys(self, table_name):
        self._create_sql = "CREATE TABLE IF NOT EXISTS {} (key TEXT, val BLOB, time FLOAT)".format(table_name)
        self._get_sql = "SELECT val, time FROM {} WHERE key = (?)".format(table_name)
        self._del_sql = "DELETE FROM {} WHERE key = (?)".format(table_name)
        self._set_sql = "INSERT OR REPLACE INTO {} (key, val, time) VALUES (?, ?, ?)".format(table_name)
        self._clear_table_sql = "DELETE FROM {}".format(table_name)

    def _sql_execute(self, sql_query, values=()):
        con = sqlite3.connect(self.path)
        cursor = con.cursor()
        cursor.execute(sql_query, values)
        response = cursor.fetchall()
        con.commit()
        con.close()
        return response

    @staticmethod
    def _get_value_or(data, name, value):
        if 0 == len(data):
            response = value
        else:
            if "time" == name:
                number = 1
            elif "value" == name:
                number = 2
            response = data[-1][number]

        return response
