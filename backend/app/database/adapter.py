import os
from app.config.settings import settings

class DatabaseAdapter:

    def __init__(self, db_type=None):
        self.db_type = db_type or settings.db_type

    def format_query(self, query: str, connection=None) -> str:
        """
        Translates SQL queries between SQLite (?) and PostgreSQL (%s) syntax depending on target engine.
        """
        is_postgres = (self.db_type == "postgres")
        if connection and not hasattr(connection, "row_factory"):
            is_postgres = True

        if is_postgres:
            return query.replace("?", "%s")
        return query

    def get_auto_increment_type(self) -> str:
        if self.db_type == "postgres":
            return "SERIAL PRIMARY KEY"
        return "INTEGER PRIMARY KEY AUTOINCREMENT"

    def execute(self, connection, query: str, params=()):
        formatted_sql = self.format_query(query, connection=connection)
        return connection.execute(formatted_sql, params)

db_adapter = DatabaseAdapter()
