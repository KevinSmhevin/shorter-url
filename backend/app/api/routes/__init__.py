"""API route modules."""

from fastapi import APIRouter

from app.api.routes import auth, urls, analytics

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(urls.router, prefix="/urls", tags=["urls"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])

