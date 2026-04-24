# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

laodeng 是一个基于 uv 的 Python 应用项目，采用 Apache 2.0 许可证。

## Development Setup

```bash
# 安装依赖（包含开发依赖）
uv sync --dev
```

## Commands

```bash
# 运行应用
uv run python main.py

# 运行所有测试
uv run pytest

# 运行单个测试文件
uv run pytest tests/test_xxx.py

# 运行单个测试函数
uv run pytest tests/test_xxx.py::test_function_name -v

# 代码格式化
uv run ruff format .

# 代码检查
uv run ruff check .

# 添加依赖
uv add <package>

# 添加开发依赖
uv add --dev <package>
```

## Architecture

console 是前端代码

src/laodeng 是后端代码

<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan
at `specs/001-image-gen-cli/plan.md`
<!-- SPECKIT END -->
