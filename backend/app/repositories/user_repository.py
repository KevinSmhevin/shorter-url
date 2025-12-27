"""Repository for user data access operations."""

from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.exceptions import DatabaseError


class UserRepository:
    """Repository class for user database operations."""

    def __init__(self, db: Session):
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def create(self, email: str, username: str, hashed_password: str) -> User:
        """
        Create a new user.
        
        Args:
            email: User email
            username: Username
            hashed_password: Hashed password
        
        Returns:
            User: Created user object
        
        Raises:
            DatabaseError: If creation fails
        """
        try:
            user = User(
                email=email,
                username=username,
                hashed_password=hashed_password,
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to create user: {str(e)}") from e

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Args:
            email: User email
        
        Returns:
            User if found, None otherwise
        """
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Args:
            username: Username
        
        Returns:
            User if found, None otherwise
        """
        return self.db.query(User).filter(User.username == username).first()

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
        
        Returns:
            User if found, None otherwise
        """
        return self.db.query(User).filter(User.id == user_id).first()




