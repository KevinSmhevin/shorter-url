"""Database migration script to add user_id column to urls table."""

from sqlalchemy import text
from app.database import engine, Base
from app.models.user import User
from app.models.url import URL
from app.models.analytics import Analytics

def migrate_database():
    """Add user_id column to urls table if it doesn't exist."""
    with engine.connect() as conn:
        # Check if user_id column exists
        result = conn.execute(text("""
            SELECT COUNT(*) as count 
            FROM pragma_table_info('urls') 
            WHERE name='user_id'
        """))
        column_exists = result.scalar() > 0
        
        if not column_exists:
            print("Adding user_id column to urls table...")
            # Add user_id column
            conn.execute(text("ALTER TABLE urls ADD COLUMN user_id INTEGER"))
            # Add foreign key constraint (SQLite doesn't support adding FK after table creation easily)
            # But we can at least add the column
            conn.commit()
            print("✓ user_id column added successfully")
        else:
            print("✓ user_id column already exists")
        
        # Check if users table exists, if not create all tables
        result = conn.execute(text("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='users'
        """))
        users_table_exists = result.first() is not None
        
        if not users_table_exists:
            print("Creating users table...")
            Base.metadata.create_all(bind=engine)
            print("✓ All tables created successfully")
        else:
            print("✓ Users table already exists")

if __name__ == "__main__":
    migrate_database()
    print("\nMigration complete!")

