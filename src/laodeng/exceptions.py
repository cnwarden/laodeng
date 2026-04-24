"""Exception classes for laodeng package."""

from __future__ import annotations


class ProviderError(Exception):
    """Base exception for provider errors."""

    pass


class AuthenticationError(ProviderError):
    """Raised when API authentication fails."""

    pass


class NetworkError(ProviderError):
    """Raised when network connectivity issues occur."""

    pass


class APIError(ProviderError):
    """Raised when the API returns an error response."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class ValidationError(ProviderError):
    """Raised when request validation fails."""

    pass
