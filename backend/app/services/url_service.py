"""Service layer for URL shortening business logic."""

from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from app.repositories.url_repository import URLRepository
from app.core.security import generate_short_code, validate_url
from app.core.exceptions import (
    InvalidURLError,
    ShortCodeGenerationError,
    URLNotFoundError,
)
from app.config import settings
from app.models.user import User


class URLService:
    """Service class for URL shortening operations."""

    def __init__(self, db: Session):
        """
        Initialize service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.url_repository = URLRepository(db)
        self.db = db

    def create_short_url(
        self,
        original_url: str,
        custom_code: Optional[str] = None,
        expires_in_days: Optional[int] = None,
        user: Optional[User] = None,
    ) -> dict:
        """
        Create a shortened URL.
        
        Args:
            original_url: The original URL to shorten
            custom_code: Optional custom short code
            expires_in_days: Optional expiration in days
        
        Returns:
            Dictionary with URL information
        
        Raises:
            InvalidURLError: If URL is invalid
            ShortCodeGenerationError: If short code generation fails
        """
        # Validate and normalize URL
        normalized_url = validate_url(original_url)
        
        # Determine short code
        if custom_code:
            # Validate custom code doesn't exist
            if self.url_repository.check_short_code_exists(custom_code):
                raise ShortCodeGenerationError(f"Short code '{custom_code}' already exists")
            short_code = custom_code
        else:
            # Generate unique short code
            max_attempts = 10
            for _ in range(max_attempts):
                short_code = generate_short_code()
                if not self.url_repository.check_short_code_exists(short_code):
                    break
            else:
                raise ShortCodeGenerationError("Failed to generate unique short code")
        
        # Calculate expiration
        expires_at = None
        if expires_in_days:
            expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
        
        # Create URL record (associate with user if authenticated)
        url = self.url_repository.create(
            short_code=short_code,
            original_url=normalized_url,
            expires_at=expires_at,
            user_id=user.id if user else None,
        )
        
        return {
            "id": url.id,
            "short_code": url.short_code,
            "original_url": url.original_url,
            "short_url": f"{settings.BASE_URL}/{url.short_code}",
            "created_at": url.created_at,
            "expires_at": url.expires_at,
            "is_active": url.is_active,
            "click_count": url.click_count,
        }

    def get_original_url(self, short_code: str) -> str:
        """
        Get original URL by short code.
        
        Args:
            short_code: The short code to look up
        
        Returns:
            Original URL string
        
        Raises:
            URLNotFoundError: If URL is not found or expired
        """
        url = self.url_repository.get_by_short_code(short_code)
        
        if not url:
            raise URLNotFoundError(f"Short code '{short_code}' not found or expired")
        
        return url.original_url

    def get_url_stats(self, short_code: str) -> dict:
        """
        Get statistics for a shortened URL.
        
        Args:
            short_code: The short code to get stats for
        
        Returns:
            Dictionary with URL statistics
        
        Raises:
            URLNotFoundError: If URL is not found
        """
        url = self.url_repository.get_by_short_code(short_code, include_inactive=True)
        
        if not url:
            raise URLNotFoundError(f"Short code '{short_code}' not found")
        
        return {
            "id": url.id,
            "short_code": url.short_code,
            "original_url": url.original_url,
            "short_url": f"{settings.BASE_URL}/{url.short_code}",
            "created_at": url.created_at,
            "expires_at": url.expires_at,
            "is_active": url.is_active,
            "total_clicks": url.click_count,
        }

    def list_urls(self, page: int = 1, page_size: int = 20, user: Optional[User] = None) -> dict:
        """
        List URLs with pagination.
        If user is provided, only returns URLs owned by that user.
        
        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            user: Optional user to filter URLs by
        
        Returns:
            Dictionary with paginated URL list
        """
        user_id = user.id if user else None
        urls, total = self.url_repository.list_urls(page=page, page_size=page_size, user_id=user_id)
        
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0
        
        url_responses = [
            {
                "id": url.id,
                "short_code": url.short_code,
                "original_url": url.original_url,
                "short_url": f"{settings.BASE_URL}/{url.short_code}",
                "created_at": url.created_at,
                "expires_at": url.expires_at,
                "is_active": url.is_active,
                "click_count": url.click_count,
            }
            for url in urls
        ]
        
        return {
            "urls": url_responses,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    def deactivate_url(self, short_code: str) -> None:
        """
        Deactivate a shortened URL.
        
        Args:
            short_code: The short code to deactivate
        
        Raises:
            URLNotFoundError: If URL is not found
        """
        url = self.url_repository.get_by_short_code(short_code, include_inactive=True)
        
        if not url:
            raise URLNotFoundError(f"Short code '{short_code}' not found")
        
        self.url_repository.deactivate(url.id)

