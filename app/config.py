# Import the settings base class used to read environment variables.
from pydantic_settings import BaseSettings, SettingsConfigDict


# Define the application settings in one central location.
class Settings(BaseSettings):
    # Store the secret used to sign secure session cookies.
    secret_key: str = "change-this-secret-in-production"
    # Store the database connection string.
    database_url: str = "sqlite:///./aamac.db"
    # Store the initial administrator username.
    admin_username: str = "admin"
    # Store the initial administrator password.
    admin_password: str = "ChangeMe123!"
    # Store the deployment environment name.
    app_env: str = "development"
    # Store the host used by the development server.
    host: str = "127.0.0.1"
    # Store the port used by the development server.
    port: int = 8000
    # Tell Pydantic Settings to load values from a .env file when available.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Create one reusable settings object for the application.
settings = Settings()
