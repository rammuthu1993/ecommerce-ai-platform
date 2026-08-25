from app.database.connection import initialize_database
from app.web.server import start_server
from app.config.settings import settings
from app.database.seed import seed_database

def main():
    print("Starting Ecommerce Application...")
    print(f"Environment: {settings.environment}")
    print(f"Database Engine: {settings.db_type} ({settings.postgres_db if settings.db_type == 'postgres' else settings.database})")

    initialize_database()
    seed_database()

    start_server()

if __name__ == "__main__":
    main()