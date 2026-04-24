# laodeng

A Python application built with [uv](https://github.com/astral-sh/uv).

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Quick Start

```bash
# 安装依赖
uv sync

# 运行应用
uv run python main.py
```

## Development

```bash
# 安装开发依赖
uv sync --dev

# 运行测试
uv run pytest

# 代码格式化
uv run ruff format .

# 代码检查
uv run ruff check .
```

## Project Structure

```
laodeng/
├── main.py           # 应用入口
├── pyproject.toml    # 项目配置
├── tests/            # 测试目录
└── .python-version   # Python 版本锁定
```

## License

Apache License 2.0
