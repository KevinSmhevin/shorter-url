"""Custom exception classes for the application."""


class ShortURLException(Exception):
    """Base exception for ShortURL application."""

    pass


class URLNotFoundError(ShortURLException):
    """Raised when a URL is not found."""

    pass


class InvalidURLError(ShortURLException):
    """Raised when a URL is invalid."""

    pass


class ShortCodeGenerationError(ShortURLException):
    """Raised when short code generation fails."""

    pass


class DatabaseError(ShortURLException):
    """Raised when a database operation fails."""

    pass

