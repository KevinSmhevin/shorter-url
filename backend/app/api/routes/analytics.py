"""Analytics API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.analytics import AnalyticsResponse, AnalyticsSummaryResponse
from app.services.analytics_service import AnalyticsService
from app.core.exceptions import URLNotFoundError
from app.core.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/{short_code}/summary", response_model=AnalyticsSummaryResponse)
def get_analytics_summary(
    short_code: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get analytics summary for a shortened URL.
    Requires authentication - only shows analytics for URLs you own.
    
    - **short_code**: The short code to get analytics for
    
    Returns:
    - Total clicks
    - Unique IP addresses
    - Clicks by date
    - Top referers
    - Clicks by hour of day
    """
    service = AnalyticsService(db)
    
    try:
        # Verify user owns the URL
        url = service.url_repository.get_by_short_code(short_code, include_inactive=True)
        if not url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Short code '{short_code}' not found",
            )
        # Only allow access if URL is owned by the current user
        # URLs without user_id (anonymous) cannot be accessed by authenticated users
        if not url.user_id or url.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to view analytics for this URL",
            )
        
        result = service.get_analytics_summary(short_code)
        return AnalyticsSummaryResponse(**result)
    except URLNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.get("/{short_code}/clicks", response_model=list[AnalyticsResponse])
def get_recent_clicks(
    short_code: str,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get recent click records for a shortened URL.
    Requires authentication - only shows clicks for URLs you own.
    
    - **short_code**: The short code to get clicks for
    - **limit**: Maximum number of records to return (default: 50, max: 500)
    """
    if limit < 1 or limit > 500:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 500",
        )
    
    service = AnalyticsService(db)
    
    try:
        # Verify user owns the URL
        url = service.url_repository.get_by_short_code(short_code, include_inactive=True)
        if not url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Short code '{short_code}' not found",
            )
        # Only allow access if URL is owned by the current user
        # URLs without user_id (anonymous) cannot be accessed by authenticated users
        if not url.user_id or url.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to view analytics for this URL",
            )
        
        result = service.get_recent_clicks(short_code, limit=limit)
        return [AnalyticsResponse(**r) for r in result]
    except URLNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e

