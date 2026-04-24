# Quickstart: Image Generation CLI

## Prerequisites

- Python 3.12+
- uv package manager
- T8STAR API token

## Setup

1. **Clone and install**:
   ```bash
   git clone <repo>
   cd laodeng
   uv sync --dev
   ```

2. **Configure API token**:
   ```bash
   export T8STAR_TOKEN="your-api-token-here"
   ```

## Basic Usage

Generate an image with a simple prompt:

```bash
uv run python -m laodeng.cli.gen_image "A beautiful sunset over mountains"
```

Output:
```
✓ Image generated successfully
URL: https://example.com/generated/image.png
Time: 45.2s
```

## Common Options

### Custom Image Size

```bash
uv run python -m laodeng.cli.gen_image "A sunset" --size 1024x1024
```

### Different Model

```bash
uv run python -m laodeng.cli.gen_image "A sunset" --model gpt-image-2
```

### JSON Output (for scripting)

```bash
uv run python -m laodeng.cli.gen_image "A sunset" --json
```

### Extended Timeout

```bash
uv run python -m laodeng.cli.gen_image "Complex scene description" --timeout 300
```

## Reference Images

Include reference image URLs directly in your prompt:

```bash
uv run python -m laodeng.cli.gen_image "A person in the style of this reference: https://example.com/style.jpg"
```

## Error Handling

The CLI provides clear error messages:

| Error | Cause | Solution |
|-------|-------|----------|
| "API token not configured" | Missing T8STAR_TOKEN | Set the environment variable |
| "Authentication failed" | Invalid token | Check your API token |
| "Generation timed out" | Slow generation | Use --timeout to extend |
| "Network error" | Connection issues | Check internet connection |

## Exit Codes

- `0`: Success
- `1`: General error
- `2`: Invalid arguments
- `3`: Authentication error
- `4`: Network/timeout error
- `5`: API error

Use exit codes in scripts:

```bash
uv run python -m laodeng.cli.gen_image "A sunset" || echo "Generation failed with code $?"
```
