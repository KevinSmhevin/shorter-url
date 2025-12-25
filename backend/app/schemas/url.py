"""Pydantic schemas for URL operations."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl, field_validator


class URLCreate(BaseModel):
    """Schema for creating a new shortened URL."""

    original_url: str = Field(..., description="The original URL to shorten", max_length=2048)
    custom_code: Optional[str] = Field(
        None,
        description="Optional custom short code (must be alphanumeric, 4-20 chars)",
        min_length=4,
        max_length=20,
    )
    expires_in_days: Optional[int] = Field(
        None,
        description="Number of days until the URL expires",
        ge=1,
        le=365,
    )

    @field_validator("custom_code")
    @classmethod
    def validate_custom_code(cls, v: Optional[str]) -> Optional[str]:
        """Validate custom code is alphanumeric."""
        if v is not None:
            if not v.isalnum():
                raise ValueError("Custom code must be alphanumeric")
        return v


class URLResponse(BaseModel):
    """Schema for URL response."""

    id: int
    short_code: str
    original_url: str
    short_url: str
    created_at: datetime
    expires_at: Optional[datetime]
    is_active: bool
    click_count: int

    model_config = {"from_attributes": True}


class URLStatsResponse(BaseModel):
    """Schema for URL statistics response."""

    short_code: str
    original_url: str
    short_url: str
    created_at: datetime
    expires_at: Optional[datetime]
    is_active: bool
    total_clicks: int
    unique_clicks: Optional[int] = None
    clicks_by_date: Optional[dict[str, int]] = None

    model_config = {"from_attributes": True}


class URLListResponse(BaseModel):
    """Schema for paginated URL list response."""

    urls: list[URLResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

