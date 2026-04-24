# Provider Interface Contract

**Module**: `src/laodeng/providers/base.py`

## Abstract Base Class: ImageProvider

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class GenerationRequest:
    prompt: str
    size: str = "1024x1536"
    model: str = "gpt-image-2"
    timeout: int = 180

@dataclass
class GenerationResult:
    urls: list[str]
    prompt: str
    model: str
    size: str
    elapsed_seconds: float

class ImageProvider(ABC):
    """Abstract base class for image generation providers."""

    @abstractmethod
    def generate(self, request: GenerationRequest) -> GenerationResult:
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
```

## Exception Hierarchy

```python
class ProviderError(Exception):
    """Base exception for provider errors."""
    pass

class AuthenticationError(ProviderError):
    """Raised when API authentication fails."""
    pass

class NetworkError(ProviderError):
    """Raised when network or timeout errors occur."""
    pass

class APIError(ProviderError):
    """Raised when the API returns an error response."""
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code

class ValidationError(ProviderError):
    """Raised when request validation fails."""
    pass
```

## T8STAR Implementation Contract

**Module**: `src/laodeng/providers/t8star.py`

```python
class T8StarProvider(ImageProvider):
    """T8STAR API image generation provider."""

    API_URL = "https://ai.t8star.cn/v1/images/generations"

    def __init__(self, api_key: str | None = None):
        """
        Initialize provider with API key.

        Args:
            api_key: API token. If None, reads from T8STAR_TOKEN env var.

        Raises:
            AuthenticationError: If no API key available.
        """
        pass

    def generate(self, request: GenerationRequest) -> GenerationResult:
        """Implementation of ImageProvider.generate()"""
        pass

    @property
    def name(self) -> str:
        return "T8STAR"
```

## Usage Example

```python
from laodeng.providers import T8StarProvider
from laodeng.providers.base import GenerationRequest

# Create provider (uses T8STAR_TOKEN env var)
provider = T8StarProvider()

# Create request
request = GenerationRequest(
    prompt="A sunset over mountains",
    size="1024x1536",
    model="gpt-image-2",
    timeout=180
)

# Generate image
result = provider.generate(request)
print(f"Generated: {result.urls[0]}")
print(f"Time: {result.elapsed_seconds}s")
```

## Adding New Providers

To add a new provider:

1. Create `src/laodeng/providers/<provider_name>.py`
2. Implement `ImageProvider` abstract base class
3. Handle provider-specific authentication and API calls
4. Map provider errors to the standard exception hierarchy
5. Export from `src/laodeng/providers/__init__.py`
