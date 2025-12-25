"""Service layer for analytics business logic."""

from typing import Optional
from sqlalchemy.orm import Session

from app.repositories.url_repository import URLRepository
from app.repositories.analytics_repository import AnalyticsRepository
from app.core.exceptions import URLNotFoundError


class AnalyticsService:
    """Service class for analytics operations."""

    def __init__(self, db: Session):
        """
        Initialize service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.url_repository = URLRepository(db)
        self.analytics_repository = AnalyticsRepository(db)
        self.db = db

    def track_click(
        self,
        short_code: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        referer: Optional[str] = None,
    ) -> None:
        """
        Track a click on a shortened URL.
        
        Args:
            short_code: The short code that was clicked
            ip_address: IP address of the requester
            user_agent: User agent string
            referer: Referer header
        
        Raises:
            URLNotFoundError: If URL is not found
        """
        url = self.url_repository.get_by_short_code(short_code)
        
        if not url:
            raise URLNotFoundError(f"Short code '{short_code}' not found or expired")
        
        # Create analytics record
        self.analytics_repository.create(
            url_id=url.id,
            ip_address=ip_address,
            user_agent=user_agent,
            referer=referer,
        )
        
        # Increment click count
        self.url_repository.increment_click_count(url.id)

    def get_analytics_summary(self, short_code: str) -> dict:
        """
        Get analytics summary for a shortened URL.
        
        Args:
            short_code: The short code to get analytics for
        
        Returns:
            Dictionary with analytics summary
        
        Raises:
            URLNotFoundError: If URL is not found
        """
        url = self.url_repository.get_by_short_code(short_code, include_inactive=True)
        
        if not url:
            raise URLNotFoundError(f"Short code '{short_code}' not found")
        
        clicks_by_date = self.analytics_repository.get_click_count_by_date(url.id)
        unique_ips = self.analytics_repository.get_unique_ip_count(url.id)
        top_referers = self.analytics_repository.get_top_referers(url.id)
        clicks_by_hour = self.analytics_repository.get_clicks_by_hour(url.id)
        
        return {
            "total_clicks": url.click_count,
            "unique_ips": unique_ips,
            "clicks_by_date": clicks_by_date,
            "top_referers": top_referers,
            "clicks_by_hour": clicks_by_hour,
        }

    def get_recent_clicks(self, short_code: str, limit: int = 50) -> list[dict]:
        """
        Get recent click records for a shortened URL.
        
        Args:
            short_code: The short code to get clicks for
            limit: Maximum number of records to return
        
        Returns:
            List of click records
        
        Raises:
            URLNotFoundError: If URL is not found
        """
        url = self.url_repository.get_by_short_code(short_code, include_inactive=True)
        
        if not url:
            raise URLNotFoundError(f"Short code '{short_code}' not found")
        
        analytics = self.analytics_repository.get_by_url_id(url.id, limit=limit)
        
        return [
            {
                "id": a.id,
                "url_id": a.url_id,
                "clicked_at": a.clicked_at,
                "ip_address": a.ip_address,
                "user_agent": a.user_agent,
                "referer": a.referer,
            }
            for a in analytics
        ]

