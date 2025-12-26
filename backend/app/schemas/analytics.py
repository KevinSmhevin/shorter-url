"""Pydantic schemas for analytics operations."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AnalyticsResponse(BaseModel):
    """Schema for individual analytics record."""

    id: int
    url_id: int
    clicked_at: datetime
    ip_address: Optional[str]
    user_agent: Optional[str]
    referer: Optional[str]

    model_config = {"from_attributes": True}


class RefererItem(BaseModel):
    """Schema for a referer item in top referers list."""

    referer: str
    count: int


class AnalyticsSummaryResponse(BaseModel):
    """Schema for analytics summary."""

    total_clicks: int
    unique_ips: Optional[int] = None
    clicks_by_date: dict[str, int]
    top_referers: Optional[list[RefererItem]] = None
    clicks_by_hour: Optional[dict[str, int]] = None

