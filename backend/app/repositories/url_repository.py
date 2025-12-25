"""Repository for URL data access operations."""

from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from app.models.url import URL
from app.core.exceptions import URLNotFoundError, DatabaseError


class URLRepository:
    """Repository class for URL database operations."""

    def __init__(self, db: Session):
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def create(self, short_code: str, original_url: str, expires_at: Optional[datetime] = None, user_id: Optional[int] = None) -> URL:
        """
        Create a new URL record.
        
        Args:
            short_code: The short code for the URL
            original_url: The original URL to shorten
            expires_at: Optional expiration datetime
        
        Returns:
            URL: Created URL object
        
        Raises:
            DatabaseError: If creation fails
        """
        try:
            url = URL(
                short_code=short_code,
                original_url=original_url,
                expires_at=expires_at,
                user_id=user_id,
            )
            self.db.add(url)
            self.db.commit()
            self.db.refresh(url)
            return url
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to create URL: {str(e)}") from e

    def get_by_short_code(self, short_code: str, include_inactive: bool = False) -> Optional[URL]:
        """
        Get URL by short code.
        
        Args:
            short_code: The short code to look up
            include_inactive: Whether to include inactive URLs
        
        Returns:
            URL if found, None otherwise
        """
        query = self.db.query(URL).filter(URL.short_code == short_code)
        
        if not include_inactive:
            query = query.filter(URL.is_active == True)
        
        url = query.first()
        
        # Check expiration
        if url and url.expires_at and url.expires_at < datetime.utcnow():
            return None
        
        return url

    def get_by_id(self, url_id: int) -> Optional[URL]:
        """
        Get URL by ID.
        
        Args:
            url_id: The URL ID
        
        Returns:
            URL if found, None otherwise
        """
        return self.db.query(URL).filter(URL.id == url_id).first()

    def check_short_code_exists(self, short_code: str) -> bool:
        """
        Check if a short code already exists.
        
        Args:
            short_code: The short code to check
        
        Returns:
            True if exists, False otherwise
        """
        return self.db.query(URL).filter(URL.short_code == short_code).first() is not None

    def increment_click_count(self, url_id: int) -> None:
        """
        Increment the click count for a URL.
        
        Args:
            url_id: The URL ID
        
        Raises:
            DatabaseError: If update fails
        """
        try:
            url = self.get_by_id(url_id)
            if url:
                url.click_count += 1
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to increment click count: {str(e)}") from e

    def deactivate(self, url_id: int) -> None:
        """
        Deactivate a URL.
        
        Args:
            url_id: The URL ID
        
        Raises:
            DatabaseError: If update fails
        """
        try:
            url = self.get_by_id(url_id)
            if url:
                url.is_active = False
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to deactivate URL: {str(e)}") from e

    def list_urls(
        self,
        page: int = 1,
        page_size: int = 20,
        include_inactive: bool = False,
        user_id: Optional[int] = None,
    ) -> tuple[list[URL], int]:
        """
        List URLs with pagination.
        
        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            include_inactive: Whether to include inactive URLs
        
        Returns:
            Tuple of (list of URLs, total count)
        """
        query = self.db.query(URL)
        
        if user_id is not None:
            query = query.filter(URL.user_id == user_id)
        
        if not include_inactive:
            query = query.filter(URL.is_active == True)
        
        total = query.count()
        
        offset = (page - 1) * page_size
        urls = query.order_by(URL.created_at.desc()).offset(offset).limit(page_size).all()
        
        return urls, total

    def delete_expired(self) -> int:
        """
        Delete expired URLs.
        
        Returns:
            Number of URLs deleted
        """
        try:
            count = self.db.query(URL).filter(
                and_(
                    URL.expires_at.isnot(None),
                    URL.expires_at < datetime.utcnow(),
                )
            ).delete(synchronize_session=False)
            self.db.commit()
            return count
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to delete expired URLs: {str(e)}") from e

