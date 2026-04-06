import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'database', 'tasks.db')


def get_database_connection():
    """Establece y retorna una conexion a la base de datos SQLite."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    """Crea las tablas necesarias si no existen."""
    connection = get_database_connection()
    schema_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'database', 'schema.sql')
    with open(schema_path, 'r') as schema_file:
        connection.executescript(schema_file.read())
    connection.close()
