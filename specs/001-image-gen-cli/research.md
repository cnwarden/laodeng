# Research: Image Generation CLI

**Feature**: 001-image-gen-cli
**Date**: 2026-04-25

## Technology Decisions

### 1. CLI Framework

**Decision**: Click

**Rationale**:
- 用户明确要求使用 Click 库
- Click 是 Python 生态最成熟的 CLI 框架之一
- 支持命令组、参数验证、自动帮助文档
- 与 loguru 日志库兼容良好

**Alternatives considered**:
- argparse: 标准库，但 API 冗长
- typer: 基于 Click，但引入额外依赖

### 2. Logging Framework

**Decision**: Loguru

**Rationale**:
- 用户明确要求使用 loguru
- 零配置即可使用，API 简洁
- 自动格式化、颜色输出、文件轮转
- 支持结构化日志和异常追踪

**Alternatives considered**:
- logging: 标准库，配置繁琐
- structlog: 功能强大但学习曲线陡

### 3. HTTP Client

**Decision**: requests

**Rationale**:
- 用户提供的参考代码使用 requests
- 最广泛使用的 HTTP 客户端
- 简单同步 API，适合 CLI 场景

**Alternatives considered**:
- httpx: 支持 async，但此场景不需要
- urllib3: 底层库，API 不够友好

### 4. Provider Abstraction

**Decision**: Abstract interface in `src/laodeng/providers/`

**Rationale**:
- 用户明确要求 API 调用需要抽象接口到 src/laodeng/providers
- 便于未来扩展支持多种图像生成 API
- 符合 constitution 的模块化架构原则
- 便于测试（可 mock provider）

**Structure**:
```
src/laodeng/providers/
├── __init__.py
├── base.py           # Abstract base class
└── t8star.py         # T8STAR implementation
```

### 5. Project Structure

**Decision**: src layout with providers module

**Rationale**:
- 符合 constitution 规定的项目结构
- src layout 避免导入冲突
- providers 模块实现可扩展性

## API Analysis

### T8STAR Image Generation API

**Endpoint**: `https://ai.t8star.cn/v1/images/generations`

**Request**:
```json
{
  "model": "gpt-image-2",
  "prompt": "<text prompt>",
  "size": "1024x1536"
}
```

**Headers**:
- `Content-Type: application/json`
- `Authorization: Bearer <T8STAR_TOKEN>`

**Response** (success):
```json
{
  "data": [
    {"url": "https://..."}
  ]
}
```

**Timeout**: 3 minutes recommended (image generation can be slow)

## Error Handling Strategy

| Error Type | Detection | User Message |
|------------|-----------|--------------|
| Missing token | `T8STAR_TOKEN` env var empty | "API token not configured. Set T8STAR_TOKEN environment variable." |
| Auth failure | HTTP 401/403 | "Authentication failed. Check your API token." |
| Rate limit | HTTP 429 | "Rate limit exceeded. Try again later." |
| Timeout | requests.Timeout | "Generation timed out after {timeout}s. Try a simpler prompt." |
| Network error | requests.ConnectionError | "Network error. Check your internet connection." |
| API error | HTTP 4xx/5xx | "API error: {status_code} - {message}" |
| Invalid size | Validation | "Invalid size format. Use WIDTHxHEIGHT (e.g., 1024x1536)." |

## CLI Design

### Command Structure

```bash
# Basic usage
uv run python -m laodeng.cli.gen_image "A sunset over mountains"

# With options
uv run python -m laodeng.cli.gen_image "A sunset" --size 1024x1024 --model gpt-image-2 --timeout 180
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| prompt | string | (required) | Image generation prompt |
| --size | string | 1024x1536 | Image dimensions (WIDTHxHEIGHT) |
| --model | string | gpt-image-2 | Model to use |
| --timeout | int | 180 | Request timeout in seconds |
| --json | flag | false | Output raw JSON response |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | Authentication error |
| 4 | Network/timeout error |
| 5 | API error |
