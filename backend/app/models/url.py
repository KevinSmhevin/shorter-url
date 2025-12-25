"""URL model for database."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.database import Base


class URL(Base):
    """Model representing a shortened URL."""

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String(50), unique=True, index=True, nullable=False)
    original_url = Column(String(2048), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    click_count = Column(Integer, default=0, nullable=False)

    # Relationships
    owner = relationship("User", back_populates="urls")
    analytics = relationship("Analytics", back_populates="url", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_short_code_active", "short_code", "is_active"),
        Index("idx_user_id_created", "user_id", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<URL(short_code='{self.short_code}', original_url='{self.original_url[:50]}...')>"

