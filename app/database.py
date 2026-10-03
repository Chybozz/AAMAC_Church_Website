# Import SQLAlchemy's engine creator.
from sqlalchemy import create_engine

# Import the base class used by all database models.
from sqlalchemy.orm import DeclarativeBase

# Import SQLAlchemy's session factory.
from sqlalchemy.orm import sessionmaker

# Import the application's environment settings.
from .config import settings


# Define the base class that all database models inherit from.
class Base(DeclarativeBase):
    # No additional configuration is required here.
    pass


# Store the database URL configured through Vercel/Neon.
database_url = settings.database_url


# SQLAlchemy uses the PostgreSQL driver named in the URL.
# If Neon provides "postgresql://" or "postgres://",
# explicitly change it to "postgresql+psycopg://".
#
# This tells SQLAlchemy to use the installed "psycopg" package
# instead of looking for the older "psycopg2" package.
if database_url.startswith("postgres://"):
    # Convert the older PostgreSQL URL format to the psycopg driver format.
    database_url = database_url.replace(
        "postgres://",
        "postgresql+psycopg://",
        1,
    )

elif database_url.startswith("postgresql://"):
    # Add the psycopg driver explicitly to the PostgreSQL URL.
    database_url = database_url.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1,
    )


# SQLite requires this connection option because the same connection
# may be accessed from different threads.
#
# PostgreSQL/Neon does not require this option.
connect_args = (
    {"check_same_thread": False}
    if database_url.startswith("sqlite")
    else {}
)


# Create the SQLAlchemy database engine.
engine = create_engine(
    # Use the corrected database URL.
    database_url,

    # Pass SQLite-specific connection settings when SQLite is used.
    connect_args=connect_args,

    # Automatically test connections before using them.
    pool_pre_ping=True,
)


# Create the database session factory used by the application.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# Provide a database session to FastAPI routes.
def get_db():
    # Open a new database session.
    db = SessionLocal()

    try:
        # Give the session to the route that requested it.
        yield db

    finally:
        # Always close the session after the request finishes.
        db.close()