import sqlite3

default_db_path = "config.db"

class Query(object):
    def __init__(self, query, bindings = tuple()):
        self.query = query
        self.bindings = bindings

class db_conn_handler:
    def make_connection(db_path):
        return sqlite3.connect(db_path)
    
    def close_connection(db_conn):
        db_conn.close()

class db_errors:
    class FetchNoResult(Exception):
        """This exception should be raised when nothing came back from a fetch query."""
        pass

class db_handler:
    def execute(cur, query):
        cur.execute(query.query, query.bindings)

    def execute_query(query):
        db_conn = db_conn_handler.make_connection(default_db_path)
        with db_conn:
            cur = db_conn.cursor()
            db_handler.execute(cur, query)
        db_conn_handler.close_connection(db_conn)

    def fetch_query(query):
        db_conn = db_conn_handler.make_connection(default_db_path)
        with db_conn:
            cur = db_conn.cursor()
            db_handler.execute(cur, query)
            result = cur.fetchall()
        db_conn_handler.close_connection(db_conn)
        if result:
            return result
        raise db_errors.FetchNoResult("No result came back from the fetch! (Maybe guild does not exist?)")
    
