"""URL shortening API routes."""

from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import logging

from app.database import get_db
from app.schemas.url import URLCreate, URLResponse, URLStatsResponse, URLListResponse
from app.services.url_service import URLService
from app.services.qr_service import QRService
from app.core.exceptions import (
    InvalidURLError,
    ShortCodeGenerationError,
    URLNotFoundError,
)
from app.core.auth import get_current_user, get_current_user_optional
from app.models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)  

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

@router.get("/{short_code}/qr", response_class=Response)
async def get_qr_code(
    short_code: str,
    size: int = Query(default=400, ge=100, le=1000, description="The size of the QR code in pixels (100-1000)"),
    error_correction: str = Query(default="M", regex="^[LMQHlmqh]$", description="The error correction level (L, M, Q, H)"),
    border: int = Query(4, ge=1, le=10, description="The border size in boxes (1-10)"),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
) -> Response:
    """
    Generate QR code for a shortened URL.
    
    - **short_code**: The short code to generate QR for
    - **size**: QR code size in pixels (default: 400, min: 100, max: 1000)
    - **error_correction**: Error correction level - L, M, Q, or H (default: M)
    - **border**: Border size in boxes (default: 4, min: 1, max: 10)
    
    Returns PNG image that can be displayed or downloaded.
    """
    
    service = URLService(db)
    qr_service = QRService()
    
    try:
        # 1. Validate short code exists and is active
        try:
            url_info = service.get_url_stats(short_code)
        except URLNotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            ) from e
        
        # 2. Check if URL is active
        if not url_info["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_410_GONE,
                detail=f"Short code '{short_code}' has been deactivated",
            )
        
        # 3. Check if URL is expired
        if url_info["expires_at"]:
            if url_info["expires_at"] < datetime.utcnow():
                raise HTTPException(
                    status_code=status.HTTP_410_GONE,
                    detail=f"Short code '{short_code}' has expired",
                )
        
        # 4. Get short URL
        short_url = url_info["short_url"]

        # 4. Get short URL
        short_url = url_info["short_url"]
        
        # 5. Validate URL is not empty
        if not short_url or not short_url.strip():
            logger.error(f"Empty short URL for code: {short_code}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to generate QR code: Invalid URL",
            )
        
        # 6. Generate QR code with error handling
        try:
            qr_bytes = qr_service.generate_qr_code(
                url=short_url,
                size=size,
                error_correction=error_correction.upper(),
                border=border,
            )
        except ValueError as e:
            # Handle validation errors from QRService
            logger.warning(f"QR generation validation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            ) from e
        except Exception as e:
            # Handle unexpected QR generation errors
            logger.error(f"QR generation failed for {short_code}: {type(e).__name__}: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate QR code. Please try again later.",
            ) from e
        
        # 7. Validate QR code was generated (not empty)
        if not qr_bytes or len(qr_bytes) == 0:
            logger.error(f"Empty QR code generated for {short_code}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate QR code. Please try again later.",
            )
        
        # 8. Return successful response
        return Response(
            content=qr_bytes,
            media_type="image/png",
            headers={
                "Content-Disposition": f'inline; filename="qr-{short_code}.png"',
                "Cache-Control": "public, max-age=3600",  # Cache for 1 hour
                "Content-Length": str(len(qr_bytes)),
            }
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions (already properly formatted)
        raise
    except Exception as e:
        # Catch-all for unexpected errors
        logger.error(f"Unexpected error generating QR for {short_code}: {type(e).__name__}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later.",
        ) from e