from app.database.connection import get_connection

class MigrationRunner:

    def __init__(self, connection=None):
        self.connection = connection

    def get_applied_migrations(self, conn):
        rows = conn.execute("SELECT version FROM schema_migrations ORDER BY version ASC").fetchall()
        return set(row["version"] for row in rows)

    def run_migrations(self, migrations: list):
        """
        migrations is a list of tuples: (version, name, sql_statement)
        """
        close_conn = False
        conn = self.connection
        if conn is None:
            conn = get_connection()
            close_conn = True

        try:
            applied = self.get_applied_migrations(conn)
            for version, name, sql_statement in sorted(migrations, key=lambda x: x[0]):
                if version not in applied:
                    conn.executescript(sql_statement)
                    conn.execute(
                        "INSERT INTO schema_migrations (version, name) VALUES (?, ?)",
                        (version, name)
                    )
                    conn.commit()
                    print(f"Applied migration v{version}: {name}")
        finally:
            if close_conn:
                conn.close()

migration_runner = MigrationRunner()
