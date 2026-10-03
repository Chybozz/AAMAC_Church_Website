# Import SQLAlchemy engine and ORM primitives.
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Import the configured database URL.
from .config import settings


# Define the application's declarative ORM base class.
class Base(DeclarativeBase):
    # Keep the base intentionally simple so all models can inherit from it.
    pass


# Configure SQLite to permit FastAPI's request threads to use the same connection safely.
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}


# Create the SQLAlchemy database engine.
engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    pool_pre_ping=True,
)


# Create the request-scoped database session factory.
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Provide a database session to route handlers and close it after each request.
def get_db():
    # Open one database session for the current request.
    db = SessionLocal()
    # Enter a guarded block so the session is always closed.
    try:
        # Yield the active session to FastAPI.
        yield db
    # Always close the session after the request finishes.
    finally:
        # Release the database connection.
        db.close()
