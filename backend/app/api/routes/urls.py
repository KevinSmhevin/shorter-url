"""URL shortening API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas.url import URLCreate, URLResponse, URLStatsResponse, URLListResponse
from app.services.url_service import URLService
from app.core.exceptions import (
    InvalidURLError,
    ShortCodeGenerationError,
    URLNotFoundError,
)
from app.core.auth import get_current_user, get_current_user_optional
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def create_short_url(
    url_data: URLCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """
    Create a new shortened URL.
    Anyone can create URLs (authentication optional).
    If authenticated, the URL will be associated with your account.
    
    - **original_url**: The original URL to shorten (required)
    - **custom_code**: Optional custom short code (4-20 alphanumeric characters)
    - **expires_in_days**: Optional expiration in days (1-365)
    """
    service = URLService(db)
    
    try:
        result = service.create_short_url(
            original_url=url_data.original_url,
            custom_code=url_data.custom_code,
            expires_in_days=url_data.expires_in_days,
            user=current_user,
        )
        return URLResponse(**result)
    except InvalidURLError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except ShortCodeGenerationError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e


@router.get("/{short_code}", response_model=URLResponse)
def get_url_info(
    short_code: str,
    db: Session = Depends(get_db),
):
    """
    Get information about a shortened URL.
    
    - **short_code**: The short code to look up
    """
    service = URLService(db)
    
    try:
        result = service.get_url_stats(short_code)
        # Convert to URLResponse format
        return URLResponse(
            id=result["id"],
            short_code=result["short_code"],
            original_url=result["original_url"],
            short_url=result["short_url"],
            created_at=result["created_at"],
            expires_at=result["expires_at"],
            is_active=result["is_active"],
            click_count=result["total_clicks"],
        )
    except URLNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e


@router.get("/", response_model=URLListResponse)
def list_urls(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    List shortened URLs with pagination.
    Requires authentication - only shows URLs created by the authenticated user.
    
    - **page**: Page number (default: 1)
    - **page_size**: Number of items per page (default: 20, max: 100)
    """
    
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page must be greater than 0",
        )
    
    if page_size < 1 or page_size > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page size must be between 1 and 100",
        )
    
    service = URLService(db)
    result = service.list_urls(page=page, page_size=page_size, user=current_user)
    return URLListResponse(**result)


@router.delete("/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_url(
    short_code: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    """
    Deactivate a shortened URL.
    Requires authentication - you can only deactivate URLs you own.
    
    - **short_code**: The short code to deactivate
    """
    service = URLService(db)
    
    try:
        # Verify user owns the URL
        url = service.url_repository.get_by_short_code(short_code, include_inactive=True)
        if not url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Short code '{short_code}' not found",
            )
        if url.user_id and (not current_user or url.user_id != current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to deactivate this URL",
            )
        
        service.deactivate_url(short_code)
    except URLNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e

