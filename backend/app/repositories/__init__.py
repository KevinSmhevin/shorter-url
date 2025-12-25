"""Repository layer for data access."""

from app.repositories.url_repository import URLRepository
from app.repositories.analytics_repository import AnalyticsRepository

__all__ = ["URLRepository", "AnalyticsRepository"]

