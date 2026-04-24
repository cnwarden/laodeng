"""T8STAR API image generation provider."""

from __future__ import annotations

import os
import time

import requests

from laodeng.models.generation import GenerationRequest, GenerationResult
from laodeng.providers.base import (
    APIError,
    AuthenticationError,
    ImageProvider,
    NetworkError,
)


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
        self._api_key = api_key or os.environ.get("T8STAR_TOKEN")
        if not self._api_key:
            raise AuthenticationError(
                "API token not configured. Set T8STAR_TOKEN environment variable."
            )

    @property
    def name(self) -> str:
        """Return the provider name for logging."""
        return "T8STAR"

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
        """
        start_time = time.time()

        body = {
            "model": request.model,
            "prompt": request.prompt,
            "size": request.size,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }

        try:
            response = requests.post(
                self.API_URL,
                headers=headers,
                json=body,
                timeout=request.timeout,
            )
        except requests.Timeout:
            raise NetworkError(
                f"Request timed out after {request.timeout}s. "
                "Try a simpler prompt or increase timeout."
            )
        except requests.ConnectionError:
            raise NetworkError("Network error. Check your internet connection.")

        elapsed = time.time() - start_time

        # Handle HTTP errors
        if response.status_code == 401 or response.status_code == 403:
            raise AuthenticationError("Authentication failed. Check your API token.")
        elif response.status_code == 429:
            raise APIError(
                "Rate limit exceeded. Try again later.",
                status_code=429,
            )
        elif response.status_code >= 400:
            raise APIError(
                f"API error: {response.status_code} - {response.text}",
                status_code=response.status_code,
            )

        # Parse successful response
        data = response.json()
        urls = [item["url"] for item in data.get("data", [])]

        return GenerationResult(
            urls=urls,
            prompt=request.prompt,
            model=request.model,
            size=request.size,
            elapsed_seconds=elapsed,
        )
