from .web.server import start_server
from .database.connection import initialize_database
from .config.settings import settings

if __name__ == "__main__":
    print(
        f"Environment: {settings.environment}"
    )

    print(
        f"Database: {settings.database}"
    )
    initialize_database()
    start_server()
