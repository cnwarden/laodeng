# CLI Contract: gen_image

**Type**: Command Line Interface
**Entry Point**: `python -m laodeng.cli.gen_image` or `uv run python -m laodeng.cli.gen_image`

## Command Signature

```bash
gen_image [OPTIONS] PROMPT
```

## Arguments

| Name | Type | Required | Description |
|------|------|----------|-------------|
| PROMPT | TEXT | Yes | Text description for image generation |

## Options

| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| --size | -s | TEXT | 1024x1536 | Image size in WIDTHxHEIGHT format |
| --model | -m | TEXT | gpt-image-2 | Model identifier to use |
| --timeout | -t | INTEGER | 180 | Request timeout in seconds |
| --json | -j | FLAG | false | Output raw JSON response |
| --help | -h | FLAG | - | Show help message and exit |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| T8STAR_TOKEN | Yes | API authentication token |

## Output Formats

### Standard Output (default)

```
✓ Image generated successfully
URL: https://example.com/generated/image.png
Time: 45.2s
```

### JSON Output (--json flag)

```json
{
  "success": true,
  "urls": ["https://example.com/generated/image.png"],
  "prompt": "A sunset over mountains",
  "model": "gpt-image-2",
  "size": "1024x1536",
  "elapsed_seconds": 45.2
}
```

### Error Output

```
✗ Error: Authentication failed. Check your API token.
```

## Exit Codes

| Code | Name | Description |
|------|------|-------------|
| 0 | SUCCESS | Image generated successfully |
| 1 | ERROR_GENERAL | Unspecified error |
| 2 | ERROR_INVALID_ARGS | Invalid command line arguments |
| 3 | ERROR_AUTH | Authentication failure |
| 4 | ERROR_NETWORK | Network or timeout error |
| 5 | ERROR_API | API returned an error |

## Examples

```bash
# Basic usage
uv run python -m laodeng.cli.gen_image "A sunset over mountains"

# Custom size
uv run python -m laodeng.cli.gen_image "A sunset" --size 1024x1024

# JSON output
uv run python -m laodeng.cli.gen_image "A sunset" --json

# All options
uv run python -m laodeng.cli.gen_image "A sunset" -s 1024x1024 -m gpt-image-2 -t 300 --json
```
