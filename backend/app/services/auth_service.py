"""Service layer for authentication business logic."""

from datetime import timedelta
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.core.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_user_by_username,
    get_user_by_email,
)


class AuthService:
    """Service class for authentication operations."""

    def __init__(self, db: Session):
        """
        Initialize service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.user_repository = UserRepository(db)
        self.db = db

    def register_user(self, email: str, username: str, password: str) -> dict:
        """
        Register a new user.
        
        Args:
            email: User email
            username: Username
            password: Plain text password (truncation handled in hashing function)
        
        Returns:
            Dictionary with user information and access token
        
        Raises:
            ValueError: If email or username already exists
        """
        # Check if email exists
        if self.user_repository.get_by_email(email):
            raise ValueError("Email already registered")
        
        # Check if username exists
        if self.user_repository.get_by_username(username):
            raise ValueError("Username already taken")
        
        # Hash password (truncation to 72 bytes handled internally by get_password_hash)
        hashed_password = get_password_hash(password)
        
        # Create user
        user = self.user_repository.create(
            email=email,
            username=username,
            hashed_password=hashed_password,
        )
        
        # Create access token
        # JWT 'sub' claim must be a string, not an integer
        access_token = create_access_token(
            data={"sub": str(user.id), "username": user.username},
            expires_delta=timedelta(hours=24),
        )
        
        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat(),
            },
            "access_token": access_token,
            "token_type": "bearer",
        }

    def login_user(self, username: str, password: str) -> dict:
        """
        Authenticate and login a user.
        
        Args:
            username: Username
            password: Plain text password (truncation handled in authenticate_user)
        
        Returns:
            Dictionary with user information and access token
        
        Raises:
            ValueError: If credentials are invalid
        """
        # Authenticate user (password truncation handled internally by authenticate_user)
        user = authenticate_user(self.db, username, password)
        
        if not user:
            raise ValueError("Invalid username or password")
        
        # Create access token
        # JWT 'sub' claim must be a string, not an integer
        access_token = create_access_token(
            data={"sub": str(user.id), "username": user.username},
            expires_delta=timedelta(hours=24),
        )
        
        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat(),
            },
            "access_token": access_token,
            "token_type": "bearer",
        }

