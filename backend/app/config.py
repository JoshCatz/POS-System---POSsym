from pydantic_settings import BaseSettings, SettingsConfigDict


# Settings defines the environment variables our application expects.
# BaseSettings automatically loads values from the environment and/or a .env file.
class Settings(BaseSettings):
    # Database connection string used by SQLAlchemy to connect to PostgreSQL.
    DATABASE_URL: str

    # Tells Pydantic where to load local environment variables from.
    # In development, this lets us keep secrets/config values in a local .env file.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        )

    # Secret key used to sign and verify JWT authentication tokens.
    jwt_secret_key: str

    # Algorithm used when encoding and decoding JWT tokens.
    # HS256 is a common symmetric signing algorithm for JWTs.
    jwt_algorithm: str = "HS256"

    # How long a JWT should remain valid, measured in minutes.
    # 60 minutes = 1 hour.
    jwt_expire_minutes: int = 60

    # Secret key used when creating secure lookup hashes for employee PINs.
    # This helps avoid storing or searching raw PIN values directly.
    pin_lookup_secret_key: str


# Creates one shared settings object for the application to import and use.
# If a required environment variable is missing, app startup will fail early.
settings = Settings()

