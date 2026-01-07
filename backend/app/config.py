"""Application configuration management."""

import os
import warnings
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "ShortURL API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = Field(
        default="sqlite:///./shorturl.db",
        description="Database connection URL. Use PostgreSQL in production."
    )
    DATABASE_ECHO: bool = False

    # API
    API_V1_PREFIX: str = "/api/v1"
    BASE_URL: str = Field(
        default="http://localhost:8000",
        description="Base URL for the application. Must be set in production."
    )
    ALLOWED_ORIGINS: str = Field(
        default="*",
        description="Comma-separated list of allowed CORS origins. Use specific domains in production."
    )
    
    # Production settings
    ENVIRONMENT: str = Field(
        default="development",
        description="Environment: 'development' or 'production'"
    )

    # Security
    SECRET_KEY: str = Field(
        default="dev-secret-key-change-in-production",
        description="Secret key for security. MUST be set in production via environment variable."
    )
    SHORT_CODE_LENGTH: int = 8
    MAX_URL_LENGTH: int = 2048

    # Rate Limiting (for future implementation)
    RATE_LIMIT_ENABLED: bool = False
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str, info) -> str:
        """Validate that SECRET_KEY is set, especially in production."""
        is_production = info.data.get("ENVIRONMENT", "development") == "production"
        
        if not v or v == "":
            if is_production:
                raise ValueError(
                    "SECRET_KEY must be set in production. "
                    "Set it via environment variable SECRET_KEY."
                )
            else:
                warnings.warn(
                    "SECRET_KEY is not set. Using empty string for development only. "
                    "Set SECRET_KEY environment variable for production.",
                    UserWarning
                )
        elif v == "change-this-secret-key-in-production":
            if is_production:
                raise ValueError(
                    "SECRET_KEY must be changed from default value in production. "
                    "Generate a strong random key and set it via environment variable."
                )
            else:
                warnings.warn(
                    "SECRET_KEY is using default value. Change it for production.",
                    UserWarning
                )
        return v

    @field_validator("BASE_URL")
    @classmethod
    def validate_base_url(cls, v: str, info) -> str:
        """Warn if BASE_URL is using default in production."""
        is_production = info.data.get("ENVIRONMENT", "development") == "production"
        
        if is_production and ("localhost" in v or "127.0.0.1" in v):
            warnings.warn(
                f"BASE_URL is set to '{v}' which appears to be a development URL. "
                "Set BASE_URL to your production domain via environment variable.",
                UserWarning
            )
        return v

    @field_validator("ALLOWED_ORIGINS")
    @classmethod
    def validate_allowed_origins(cls, v: str, info) -> str:
        """Warn if ALLOWED_ORIGINS is too permissive in production."""
        is_production = info.data.get("ENVIRONMENT", "development") == "production"
        
        if is_production and v == "*":
            warnings.warn(
                "ALLOWED_ORIGINS is set to '*' which allows all origins. "
                "Set ALLOWED_ORIGINS to specific domains in production for security.",
                UserWarning
            )
        return v

    @field_validator("DATABASE_URL")
    @classmethod
    def validate_database_url(cls, v: str, info) -> str:
        """Warn if using SQLite in production."""
        is_production = info.data.get("ENVIRONMENT", "development") == "production"
        
        if is_production and v.startswith("sqlite"):
            warnings.warn(
                "DATABASE_URL is using SQLite. SQLite is not recommended for production. "
                "Use PostgreSQL or another production database.",
                UserWarning
            )
        return v


settings = Settings()

