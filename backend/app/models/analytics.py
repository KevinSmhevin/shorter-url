"""Analytics model for tracking URL clicks."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.database import Base


class Analytics(Base):
    """Model representing analytics data for URL clicks."""

    __tablename__ = "analytics"

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey("urls.id", ondelete="CASCADE"), nullable=False, index=True)
    clicked_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    ip_address = Column(String(45), nullable=True)  # IPv6 max length
    user_agent = Column(String(512), nullable=True)
    referer = Column(String(512), nullable=True)

    # Relationship to URL
    url = relationship("URL", back_populates="analytics")

    __table_args__ = (
        Index("idx_url_clicked_at", "url_id", "clicked_at"),
    )

    def __repr__(self) -> str:
        return f"<Analytics(url_id={self.url_id}, clicked_at='{self.clicked_at}')>"

