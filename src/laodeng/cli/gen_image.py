"""Image generation CLI command."""

from __future__ import annotations

import sys

import click
from loguru import logger

from laodeng.models.generation import GenerationRequest
from laodeng.providers import (
    APIError,
    AuthenticationError,
    NetworkError,
    T8StarProvider,
    ValidationError,
)

# Exit codes
EXIT_SUCCESS = 0
EXIT_ERROR_GENERAL = 1
EXIT_ERROR_INVALID_ARGS = 2
EXIT_ERROR_AUTH = 3
EXIT_ERROR_NETWORK = 4
EXIT_ERROR_API = 5


def _configure_logging(verbose: bool, quiet: bool = False) -> None:
    """Configure loguru logging based on verbosity level.

    Args:
        verbose: Enable debug-level logging
        quiet: Suppress all logging output (for JSON mode)
    """
    logger.remove()  # Remove default handler
    if quiet:
        return  # No handlers = no output
    level = "DEBUG" if verbose else "INFO"
    logger.add(
        sys.stderr,
        format="<level>{level: <8}</level> | <cyan>{time:HH:mm:ss}</cyan> | {message}",
        level=level,
    )


@click.command()
@click.argument("prompt")
@click.option(
    "--size",
    "-s",
    default="1024x1536",
    help="Image size in WIDTHxHEIGHT format (default: 1024x1536)",
)
@click.option(
    "--model",
    "-m",
    default="gpt-image-2",
    help="Model identifier to use (default: gpt-image-2)",
)
@click.option(
    "--timeout",
    "-t",
    default=180,
    type=int,
    help="Request timeout in seconds (default: 180)",
)
@click.option(
    "--json",
    "-j",
    "output_json",
    is_flag=True,
    help="Output raw JSON response",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose/debug logging",
)
def main(
    prompt: str,
    size: str,
    model: str,
    timeout: int,
    output_json: bool,
    verbose: bool,
) -> None:
    """Generate an image from a text PROMPT using AI.

    Example:
        gen_image "A beautiful sunset over mountains"
    """
    # Configure logging based on verbosity and output mode
    _configure_logging(verbose, quiet=output_json)

    try:
        # Create provider
        logger.info("Initializing T8STAR provider...")
        provider = T8StarProvider()

        # Create request
        logger.info(f"Generating image for prompt: {prompt[:50]}...")
        request = GenerationRequest(
            prompt=prompt,
            size=size,
            model=model,
            timeout=timeout,
        )

        # Generate image
        result = provider.generate(request)

        # Output result
        if output_json:
            import json

            output = {
                "success": True,
                "urls": result.urls,
                "prompt": result.prompt,
                "model": result.model,
                "size": result.size,
                "elapsed_seconds": result.elapsed_seconds,
            }
            click.echo(json.dumps(output, indent=2))
        else:
            click.echo(click.style("✓ Image generated successfully", fg="green"))
            for url in result.urls:
                click.echo(f"URL: {url}")
            click.echo(f"Time: {result.elapsed_seconds:.1f}s")

        logger.info(f"Generation completed in {result.elapsed_seconds:.1f}s")
        sys.exit(EXIT_SUCCESS)

    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        click.echo(click.style(f"✗ Error: {e}", fg="red"), err=True)
        sys.exit(EXIT_ERROR_INVALID_ARGS)

    except AuthenticationError as e:
        logger.error(f"Authentication error: {e}")
        click.echo(click.style(f"✗ Error: {e}", fg="red"), err=True)
        sys.exit(EXIT_ERROR_AUTH)

    except NetworkError as e:
        logger.error(f"Network error: {e}")
        click.echo(click.style(f"✗ Error: {e}", fg="red"), err=True)
        sys.exit(EXIT_ERROR_NETWORK)

    except APIError as e:
        logger.error(f"API error: {e}")
        click.echo(click.style(f"✗ Error: {e}", fg="red"), err=True)
        sys.exit(EXIT_ERROR_API)

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        click.echo(click.style(f"✗ Error: {e}", fg="red"), err=True)
        sys.exit(EXIT_ERROR_GENERAL)


if __name__ == "__main__":
    main()
