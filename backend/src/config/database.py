import sqlite3
import os
from contextlib import contextmanager

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'database', 'tasks.db')

TITLE_MAX_LENGTH = 200


@contextmanager
def get_database_connection():
    """Context manager que establece y cierra la conexion a SQLite de forma segura."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        yield connection
    finally:
        connection.close()


def initialize_database():
    """Crea las tablas necesarias si no existen."""
    schema_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'database', 'schema.sql')
    with get_database_connection() as connection:
        with open(schema_path, 'r') as schema_file:
            connection.executescript(schema_file.read())
