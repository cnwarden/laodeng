"""Unit tests for providers."""

from unittest.mock import Mock, patch

import pytest

from laodeng.providers.base import (
    APIError,
    AuthenticationError,
    NetworkError,
    ProviderError,
    ValidationError,
)


class TestProviderExceptions:
    """Tests for provider exception hierarchy."""

    def test_provider_error_is_base(self):
        """Test ProviderError is the base exception."""
        error = ProviderError("Test error")
        assert str(error) == "Test error"
        assert isinstance(error, Exception)

    def test_authentication_error_inherits_provider_error(self):
        """Test AuthenticationError inherits from ProviderError."""
        error = AuthenticationError("Auth failed")
        assert isinstance(error, ProviderError)
        assert str(error) == "Auth failed"

    def test_network_error_inherits_provider_error(self):
        """Test NetworkError inherits from ProviderError."""
        error = NetworkError("Connection failed")
        assert isinstance(error, ProviderError)
        assert str(error) == "Connection failed"

    def test_api_error_inherits_provider_error(self):
        """Test APIError inherits from ProviderError."""
        error = APIError("API returned 500", status_code=500)
        assert isinstance(error, ProviderError)
        assert str(error) == "API returned 500"
        assert error.status_code == 500

    def test_api_error_without_status_code(self):
        """Test APIError can be created without status_code."""
        error = APIError("Unknown API error")
        assert error.status_code is None

    def test_validation_error_inherits_provider_error(self):
        """Test ValidationError inherits from ProviderError."""
        error = ValidationError("Invalid input")
        assert isinstance(error, ProviderError)
        assert str(error) == "Invalid input"


class TestT8StarProviderInit:
    """Tests for T8StarProvider initialization."""

    def test_init_with_explicit_api_key(self):
        """Test provider init with explicit API key."""
        from laodeng.providers.t8star import T8StarProvider

        provider = T8StarProvider(api_key="test-token")
        assert provider.name == "T8STAR"

    def test_init_reads_env_var(self):
        """Test provider reads T8STAR_TOKEN from environment."""
        from laodeng.providers.t8star import T8StarProvider

        with patch.dict("os.environ", {"T8STAR_TOKEN": "env-token"}):
            provider = T8StarProvider()
            assert provider.name == "T8STAR"

    def test_init_raises_auth_error_when_no_token(self):
        """Test provider raises AuthenticationError when no token available."""
        from laodeng.providers.t8star import T8StarProvider

        with patch.dict("os.environ", {}, clear=True):
            # Remove T8STAR_TOKEN if it exists
            import os

            os.environ.pop("T8STAR_TOKEN", None)
            with pytest.raises(AuthenticationError, match="API token not configured"):
                T8StarProvider()


class TestT8StarProviderGenerate:
    """Tests for T8StarProvider.generate method."""

    def test_generate_success(self):
        """Test successful image generation."""
        from laodeng.models.generation import GenerationRequest
        from laodeng.providers.t8star import T8StarProvider

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"url": "https://example.com/generated.png"}]
        }

        with patch("requests.post", return_value=mock_response):
            provider = T8StarProvider(api_key="test-token")
            request = GenerationRequest(prompt="A sunset over mountains")
            result = provider.generate(request)

            assert len(result.urls) == 1
            assert result.urls[0] == "https://example.com/generated.png"
            assert result.prompt == "A sunset over mountains"
            assert result.model == "gpt-image-2"
            assert result.size == "1024x1536"
            assert result.elapsed_seconds >= 0


class TestT8StarProviderErrorHandling:
    """Tests for T8StarProvider error handling."""

    def test_generate_timeout_raises_network_error(self):
        """Test that timeout raises NetworkError."""
        import requests

        from laodeng.models.generation import GenerationRequest
        from laodeng.providers.t8star import T8StarProvider

        with patch(
            "requests.post", side_effect=requests.Timeout("Connection timed out")
        ):
            provider = T8StarProvider(api_key="test-token")
            request = GenerationRequest(prompt="A sunset")

            with pytest.raises(NetworkError, match="timed out"):
                provider.generate(request)

    def test_generate_connection_error_raises_network_error(self):
        """Test that connection error raises NetworkError."""
        import requests

        from laodeng.models.generation import GenerationRequest
        from laodeng.providers.t8star import T8StarProvider

        with patch(
            "requests.post", side_effect=requests.ConnectionError("No connection")
        ):
            provider = T8StarProvider(api_key="test-token")
            request = GenerationRequest(prompt="A sunset")

            with pytest.raises(NetworkError, match="Network error"):
                provider.generate(request)

    def test_generate_401_raises_auth_error(self):
        """Test that 401 response raises AuthenticationError."""
        from laodeng.models.generation import GenerationRequest
        from laodeng.providers.t8star import T8StarProvider

        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"

        with patch("requests.post", return_value=mock_response):
            provider = T8StarProvider(api_key="test-token")
            request = GenerationRequest(prompt="A sunset")

            with pytest.raises(AuthenticationError, match="Authentication failed"):
                provider.generate(request)

    def test_generate_500_raises_api_error(self):
        """Test that 500 response raises APIError."""
        from laodeng.models.generation import GenerationRequest
        from laodeng.providers.t8star import T8StarProvider

        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"

        with patch("requests.post", return_value=mock_response):
            provider = T8StarProvider(api_key="test-token")
            request = GenerationRequest(prompt="A sunset")

            with pytest.raises(APIError) as exc_info:
                provider.generate(request)
            assert exc_info.value.status_code == 500


class TestT8StarProviderReferenceImage:
    """Tests for T8StarProvider with reference image URLs (User Story 3)."""

    def test_generate_with_reference_url_in_prompt(self):
        """Test that prompts containing reference URLs work correctly."""
        from laodeng.models.generation import GenerationRequest
        from laodeng.providers.t8star import T8StarProvider

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"url": "https://example.com/generated.png"}]
        }

        prompt_with_url = (
            "A person like this photo: https://example.com/ref.jpg in a sunset"
        )

        with patch("requests.post", return_value=mock_response) as mock_post:
            provider = T8StarProvider(api_key="test-token")
            request = GenerationRequest(prompt=prompt_with_url)
            result = provider.generate(request)

            assert result.urls[0] == "https://example.com/generated.png"
            # Verify the full prompt was sent to API
            call_args = mock_post.call_args
            assert call_args[1]["json"]["prompt"] == prompt_with_url

    def test_generate_with_multiple_reference_urls(self):
        """Test that prompts with multiple reference URLs work correctly."""
        from laodeng.models.generation import GenerationRequest
        from laodeng.providers.t8star import T8StarProvider

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"url": "https://example.com/generated.png"}]
        }

        prompt_with_urls = "Combine this: https://example.com/ref1.jpg and this: https://example.com/ref2.png"

        with patch("requests.post", return_value=mock_response) as mock_post:
            provider = T8StarProvider(api_key="test-token")
            request = GenerationRequest(prompt=prompt_with_urls)
            result = provider.generate(request)

            assert len(result.urls) == 1
            call_args = mock_post.call_args
            assert call_args[1]["json"]["prompt"] == prompt_with_urls
