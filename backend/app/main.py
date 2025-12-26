"""FastAPI application entry point."""

from fastapi import FastAPI, Request, HTTPException, status, Depends
from fastapi.responses import RedirectResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import settings
from app.database import init_db, get_db
from app.api.routes import api_router
from app.services.analytics_service import AnalyticsService
from app.core.exceptions import URLNotFoundError

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A URL shortening service with analytics",
    docs_url="/docs" if settings.DEBUG else None,  # Disable docs in production
    redoc_url="/redoc" if settings.DEBUG else None,  # Disable redoc in production
)

# CORS middleware
# In production, set ALLOWED_ORIGINS environment variable (comma-separated)
import logging

logger = logging.getLogger(__name__)

if settings.ALLOWED_ORIGINS and settings.ALLOWED_ORIGINS != "*":
    allowed_origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")]
    # Remove empty strings
    allowed_origins = [origin for origin in allowed_origins if origin]
    logger.info(f"CORS allowed origins: {allowed_origins}")
else:
    allowed_origins = ["*"] if settings.DEBUG else []
    logger.warning("CORS is set to allow all origins (DEBUG mode) or no origins")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "ShortURL API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/debug/cors")
async def debug_cors():
    """Debug endpoint to check CORS configuration (only in DEBUG mode)."""
    if not settings.DEBUG:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    
    return {
        "allowed_origins": allowed_origins,
        "raw_allowed_origins": settings.ALLOWED_ORIGINS,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots_txt():
    """
    Serve robots.txt to control web crawler behavior.
    Prevents crawling of API endpoints and rate limits crawlers.
    """
    # Use BASE_URL from settings for sitemap (if configured)
    base_url = settings.BASE_URL
    sitemap_line = f"Sitemap: {base_url}/sitemap.xml" if base_url and not base_url.startswith("http://localhost") else "# Sitemap: https://yourdomain.com/sitemap.xml"
    
    robots_content = f"""# robots.txt for ShortURL
# This file controls how web crawlers and bots interact with the site

User-agent: *
# Disallow crawling of API endpoints
Disallow: /api/
# Disallow crawling of analytics pages (privacy)
Disallow: /analytics/
# Allow crawling of the main pages
Allow: /
Allow: /urls

# Crawl-delay to rate limit aggressive crawlers (in seconds)
Crawl-delay: 10

# Sitemap location
{sitemap_line}
"""
    return robots_content


@app.get("/{short_code}")
async def redirect_to_url(
    short_code: str,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Redirect to the original URL and track analytics.
    
    - **short_code**: The short code to redirect
    """
    analytics_service = AnalyticsService(db)
    
    try:
        # Get IP address
        ip_address = request.client.host if request.client else None
        
        # Get headers
        user_agent = request.headers.get("user-agent")
        referer = request.headers.get("referer")
        
        # Track click and get original URL
        original_url = analytics_service.url_repository.get_by_short_code(short_code)
        
        if not original_url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Short code '{short_code}' not found or expired",
            )
        
        # Track analytics
        analytics_service.track_click(
            short_code=short_code,
            ip_address=ip_address,
            user_agent=user_agent,
            referer=referer,
        )
        
        return RedirectResponse(url=original_url.original_url, status_code=status.HTTP_302_FOUND)
    
    except URLNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Short code '{short_code}' not found or expired",
        )


# Include API routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )

