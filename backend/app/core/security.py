"""Security utilities for URL validation and short code generation."""

import secrets
import string
from urllib.parse import urlparse

import validators

from app.config import settings
from app.core.exceptions import InvalidURLError


def generate_short_code(length: int = None) -> str:
    """
    Generate a random short code for URL shortening.
    
    Args:
        length: Length of the short code. Defaults to settings.SHORT_CODE_LENGTH.
    
    Returns:
        str: Random alphanumeric short code
    """
    if length is None:
        length = settings.SHORT_CODE_LENGTH
    
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def validate_url(url: str) -> str:
    """
    Validate and normalize a URL.
    
    Args:
        url: URL string to validate
    
    Returns:
        str: Normalized URL
    
    Raises:
        InvalidURLError: If the URL is invalid
    """
    if not url or not isinstance(url, str):
        raise InvalidURLError("URL cannot be empty")
    
    url = url.strip()
    
    # Add protocol if missing
    parsed = urlparse(url)
    if not parsed.scheme:
        url = f"https://{url}"
    
    # Validate URL
    if not validators.url(url):
        raise InvalidURLError(f"Invalid URL format: {url}")
    
    # Check URL length
    if len(url) > settings.MAX_URL_LENGTH:
        raise InvalidURLError(f"URL exceeds maximum length of {settings.MAX_URL_LENGTH}")
    
    return url

