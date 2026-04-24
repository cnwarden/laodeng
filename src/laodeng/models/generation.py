"""Generation request and result models."""

from __future__ import annotations

import re
from dataclasses import dataclass

from laodeng.exceptions import ValidationError

SIZE_PATTERN = re.compile(r"^\d+x\d+$")


def _validate_prompt(prompt: str) -> str:
    """Validate prompt is not empty or whitespace."""
    if not prompt or not prompt.strip():
        raise ValidationError("Prompt cannot be empty")
    return prompt


def _validate_size(size: str) -> str:
    """Validate size format is WIDTHxHEIGHT."""
    if not SIZE_PATTERN.match(size):
        raise ValidationError(
            f"Invalid size format: {size}. Expected WIDTHxHEIGHT (e.g., 1024x1536)"
        )
    return size


def _validate_timeout(timeout: int) -> int:
    """Validate timeout is positive."""
    if timeout <= 0:
        raise ValidationError("Timeout must be positive")
    return timeout


@dataclass
class GenerationRequest:
    """Represents a single image generation request."""

    prompt: str
    size: str = "1024x1536"
    model: str = "gpt-image-2"
    timeout: int = 180

    def __post_init__(self):
        """Validate fields after initialization."""
        self.prompt = _validate_prompt(self.prompt)
        self.size = _validate_size(self.size)
        self.timeout = _validate_timeout(self.timeout)


@dataclass
class GenerationResult:
    """Represents the API response containing generated image(s)."""

    urls: list[str]
    prompt: str
    model: str
    size: str
    elapsed_seconds: float
