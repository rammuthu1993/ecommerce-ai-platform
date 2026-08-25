import os

class Settings:

    def __init__(self):
        self.host = os.getenv("APP_HOST", "localhost")
        self.port = int(os.getenv("APP_PORT", "8000"))
        
        # Database Path / Name
        self.database = os.getenv("DATABASE_PATH", "ecommerce.db")
        
        # PostgreSQL Settings
        self.postgres_host = os.getenv("POSTGRES_HOST", "localhost")
        self.postgres_port = int(os.getenv("POSTGRES_PORT", "5432"))
        self.postgres_db = os.getenv("POSTGRES_DB", "ecommerce_db")
        self.postgres_user = os.getenv("POSTGRES_USER", "postgres")
        self.postgres_password = os.getenv("POSTGRES_PASSWORD", "Muthu@1512")
        self.database_url = os.getenv("DATABASE_URL")
        
        self.environment = os.getenv("APP_ENV", "development")
        self.cors_origins = os.getenv("CORS_ORIGINS", "*")
        self.max_request_size = int(os.getenv("MAX_REQUEST_SIZE", "1048576")) # 1 MB
        self.rate_limit_per_minute = int(os.getenv("RATE_LIMIT_PER_MINUTE", "120"))

    @property
    def db_type(self) -> str:
        explicit_type = os.getenv("DATABASE_TYPE")
        if explicit_type:
            return explicit_type.lower()
        if "test" in self.database or self.database.endswith(".db"):
            return "sqlite" if "test" in self.database else "postgres"
        return "postgres"

settings = Settings()