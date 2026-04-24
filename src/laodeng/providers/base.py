"""Base classes for image providers."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from laodeng.exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    ProviderError,
    ValidationError,
)

if TYPE_CHECKING:
    from laodeng.models.generation import GenerationRequest, GenerationResult

# Re-export exceptions for backward compatibility
__all__ = [
    "ImageProvider",
    "ProviderError",
    "AuthenticationError",
    "NetworkError",
    "APIError",
    "ValidationError",
]


class ImageProvider(ABC):
    """Abstract base class for image generation providers."""

    @abstractmethod
    def generate(self, request: "GenerationRequest") -> "GenerationResult":
        """
        Generate image(s) from the given request.

        Args:
            request: GenerationRequest with prompt and options

        Returns:
            GenerationResult containing image URLs and metadata

        Raises:
            AuthenticationError: Invalid or missing API credentials
            NetworkError: Connection or timeout issues
            APIError: Provider returned an error response
            ValidationError: Invalid request parameters
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the provider name for logging."""
        pass
