"""Unit tests for models."""

import pytest

from laodeng.models.generation import GenerationRequest, GenerationResult


class TestGenerationRequest:
    """Tests for GenerationRequest dataclass."""

    def test_create_with_defaults(self):
        """Test creating request with only prompt."""
        request = GenerationRequest(prompt="A sunset over mountains")
        assert request.prompt == "A sunset over mountains"
        assert request.size == "1024x1536"
        assert request.model == "gpt-image-2"
        assert request.timeout == 180

    def test_create_with_custom_values(self):
        """Test creating request with custom values."""
        request = GenerationRequest(
            prompt="A sunset",
            size="1024x1024",
            model="custom-model",
            timeout=300,
        )
        assert request.prompt == "A sunset"
        assert request.size == "1024x1024"
        assert request.model == "custom-model"
        assert request.timeout == 300

    def test_prompt_cannot_be_empty(self):
        """Test that empty prompt raises ValidationError."""
        from laodeng.providers.base import ValidationError

        with pytest.raises(ValidationError, match="Prompt cannot be empty"):
            GenerationRequest(prompt="")

    def test_prompt_cannot_be_whitespace(self):
        """Test that whitespace-only prompt raises ValidationError."""
        from laodeng.providers.base import ValidationError

        with pytest.raises(ValidationError, match="Prompt cannot be empty"):
            GenerationRequest(prompt="   ")

    def test_size_must_be_valid_format(self):
        """Test that invalid size format raises ValidationError."""
        from laodeng.providers.base import ValidationError

        with pytest.raises(ValidationError, match="Invalid size format"):
            GenerationRequest(prompt="test", size="invalid")

    def test_timeout_must_be_positive(self):
        """Test that non-positive timeout raises ValidationError."""
        from laodeng.providers.base import ValidationError

        with pytest.raises(ValidationError, match="Timeout must be positive"):
            GenerationRequest(prompt="test", timeout=0)


class TestGenerationResult:
    """Tests for GenerationResult dataclass."""

    def test_create_result(self):
        """Test creating a generation result."""
        result = GenerationResult(
            urls=["https://example.com/image.png"],
            prompt="A sunset",
            model="gpt-image-2",
            size="1024x1536",
            elapsed_seconds=45.2,
        )
        assert result.urls == ["https://example.com/image.png"]
        assert result.prompt == "A sunset"
        assert result.model == "gpt-image-2"
        assert result.size == "1024x1536"
        assert result.elapsed_seconds == 45.2

    def test_result_with_multiple_urls(self):
        """Test creating result with multiple URLs."""
        result = GenerationResult(
            urls=["https://example.com/1.png", "https://example.com/2.png"],
            prompt="A sunset",
            model="gpt-image-2",
            size="1024x1536",
            elapsed_seconds=60.0,
        )
        assert len(result.urls) == 2
