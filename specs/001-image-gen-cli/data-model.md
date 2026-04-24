# Data Model: Image Generation CLI

**Feature**: 001-image-gen-cli
**Date**: 2026-04-25

## Entities

### GenerationRequest

Represents a single image generation request.

| Field | Type | Required | Validation | Description |
|-------|------|----------|------------|-------------|
| prompt | string | yes | non-empty, max 4000 chars | Text description for image generation |
| size | string | no | format: WIDTHxHEIGHT | Image dimensions, default "1024x1536" |
| model | string | no | non-empty | Model identifier, default "gpt-image-2" |
| timeout | int | no | positive integer | Request timeout in seconds, default 180 |

**Validation Rules**:
- `prompt` cannot be empty or whitespace-only
- `size` must match pattern `\d+x\d+` (e.g., "1024x1536")
- `timeout` must be positive integer

### GenerationResult

Represents the API response containing generated image(s).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| urls | list[string] | yes | List of generated image URLs |
| prompt | string | yes | Original prompt used |
| model | string | yes | Model used for generation |
| size | string | yes | Requested size |
| elapsed_seconds | float | yes | Time taken for generation |

### ProviderConfig

Configuration for an image generation provider.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| api_url | string | yes | API endpoint URL |
| api_key | string | yes | Authentication token |
| default_model | string | no | Default model to use |
| default_size | string | no | Default image size |
| default_timeout | int | no | Default timeout in seconds |

## Relationships

```
GenerationRequest  ──────>  ImageProvider  ──────>  GenerationResult
      │                          │
      │                          │
      └── uses config from ──────┘
             ProviderConfig
```

## State Transitions

### Request Lifecycle

```
[Created] ──> [Validating] ──> [Sending] ──> [Waiting] ──> [Completed]
                  │               │             │              │
                  v               v             v              v
              [Invalid]      [SendError]   [Timeout]      [Success]
                                               │              │
                                               └──────────────┴──> [Logged]
```

## Module Organization

```
src/laodeng/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── generation.py      # GenerationRequest, GenerationResult
├── providers/
│   ├── __init__.py
│   ├── base.py            # ImageProvider ABC
│   └── t8star.py          # T8StarProvider implementation
└── cli/
    ├── __init__.py
    └── gen_image.py       # CLI entry point
```
