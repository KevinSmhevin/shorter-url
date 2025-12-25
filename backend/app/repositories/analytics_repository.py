"""Repository for analytics data access operations."""

from datetime import datetime, date
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct

from app.models.analytics import Analytics
from app.core.exceptions import DatabaseError


class AnalyticsRepository:
    """Repository class for analytics database operations."""

    def __init__(self, db: Session):
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def create(
        self,
        url_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        referer: Optional[str] = None,
    ) -> Analytics:
        """
        Create a new analytics record.
        
        Args:
            url_id: The URL ID
            ip_address: IP address of the requester
            user_agent: User agent string
            referer: Referer header
        
        Returns:
            Analytics: Created analytics object
        
        Raises:
            DatabaseError: If creation fails
        """
        try:
            analytics = Analytics(
                url_id=url_id,
                ip_address=ip_address,
                user_agent=user_agent,
                referer=referer,
            )
            self.db.add(analytics)
            self.db.commit()
            self.db.refresh(analytics)
            return analytics
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to create analytics record: {str(e)}") from e

    def get_by_url_id(self, url_id: int, limit: Optional[int] = None) -> list[Analytics]:
        """
        Get analytics records for a URL.
        
        Args:
            url_id: The URL ID
            limit: Optional limit on number of records
        
        Returns:
            List of analytics records
        """
        query = self.db.query(Analytics).filter(Analytics.url_id == url_id).order_by(
            Analytics.clicked_at.desc()
        )
        
        if limit:
            query = query.limit(limit)
        
        return query.all()

    def get_click_count_by_date(self, url_id: int) -> dict[str, int]:
        """
        Get click count grouped by date for a URL.
        
        Args:
            url_id: The URL ID
        
        Returns:
            Dictionary mapping date strings to click counts
        """
        results = (
            self.db.query(
                func.date(Analytics.clicked_at).label("date"),
                func.count(Analytics.id).label("count"),
            )
            .filter(Analytics.url_id == url_id)
            .group_by(func.date(Analytics.clicked_at))
            .order_by(func.date(Analytics.clicked_at).desc())
            .all()
        )
        
        return {str(result.date): result.count for result in results}

    def get_unique_ip_count(self, url_id: int) -> int:
        """
        Get count of unique IP addresses for a URL.
        
        Args:
            url_id: The URL ID
        
        Returns:
            Number of unique IPs
        """
        result = (
            self.db.query(func.count(distinct(Analytics.ip_address)))
            .filter(Analytics.url_id == url_id)
            .scalar()
        )
        return result or 0

    def get_top_referers(self, url_id: int, limit: int = 10) -> list[dict[str, int]]:
        """
        Get top referers for a URL.
        
        Args:
            url_id: The URL ID
            limit: Number of top referers to return
        
        Returns:
            List of dictionaries with referer and count
        """
        results = (
            self.db.query(
                Analytics.referer,
                func.count(Analytics.id).label("count"),
            )
            .filter(
                Analytics.url_id == url_id,
                Analytics.referer.isnot(None),
            )
            .group_by(Analytics.referer)
            .order_by(func.count(Analytics.id).desc())
            .limit(limit)
            .all()
        )
        
        return [{"referer": result.referer, "count": result.count} for result in results]

    def get_clicks_by_hour(self, url_id: int) -> dict[str, int]:
        """
        Get click count grouped by hour of day for a URL.
        
        Args:
            url_id: The URL ID
        
        Returns:
            Dictionary mapping hour strings to click counts
        """
        results = (
            self.db.query(
                func.extract("hour", Analytics.clicked_at).label("hour"),
                func.count(Analytics.id).label("count"),
            )
            .filter(Analytics.url_id == url_id)
            .group_by(func.extract("hour", Analytics.clicked_at))
            .order_by(func.extract("hour", Analytics.clicked_at))
            .all()
        )
        
        return {f"{int(result.hour):02d}:00": result.count for result in results}

