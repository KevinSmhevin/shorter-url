"""Database configuration and session management."""

import logging
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings

logger = logging.getLogger(__name__)

# Create database engine
# For SQLite, we need to add check_same_thread=False
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=settings.DATABASE_ECHO,
    )
else:
    # PostgreSQL or other databases
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DATABASE_ECHO,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=10,
        max_overflow=20,
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db() -> Session:
    """
    Dependency function to get database session.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database by creating all tables."""
    # Import all models to ensure they're registered
    from app.models import User, URL, Analytics  # noqa: F401
    
    Base.metadata.create_all(bind=engine)
    
    # For SQLite, handle migration of existing tables
    if engine.url.drivername == "sqlite":
        try:
            with engine.begin() as conn:
                # Check if urls table exists
                result = conn.execute(
                    text("SELECT name FROM sqlite_master WHERE type='table' AND name='urls'")
                )
                urls_table_exists = result.first() is not None
                
                if urls_table_exists:
                    # Check if user_id column exists in urls table
                    result = conn.execute(
                        text("SELECT COUNT(*) FROM pragma_table_info('urls') WHERE name='user_id'")
                    )
                    column_exists = result.scalar() > 0
                    
                    if not column_exists:
                        # Add user_id column to existing urls table
                        conn.execute(text("ALTER TABLE urls ADD COLUMN user_id INTEGER"))
        except Exception as e:
            logger.warning(f"Could not migrate database: {e}")

