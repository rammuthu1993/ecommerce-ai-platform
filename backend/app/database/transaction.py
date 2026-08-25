import sqlite3
from contextlib import contextmanager
from .connection import get_connection

@contextmanager
def db_transaction(connection=None):
    """
    Context manager for database transactions.
    If a connection is passed in, uses that connection without closing it.
    If no connection is passed in, opens a new connection, commits on success,
    rolls back on exception, and closes the connection.
    """
    owns_connection = False
    if connection is None:
        connection = get_connection()
        owns_connection = True

    try:
        yield connection
        if owns_connection:
            connection.commit()
    except Exception:
        if owns_connection:
            connection.rollback()
        raise
    finally:
        if owns_connection:
            connection.close()
