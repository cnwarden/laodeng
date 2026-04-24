# Implementation Plan: Image Generation CLI

**Branch**: `001-image-gen-cli` | **Date**: 2026-04-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-image-gen-cli/spec.md`

## Summary

实现一个基于命令行的 AI 图像生成工具，支持通过文本 prompt 生成图像。使用 Click 库构建 CLI，loguru 处理日志，通过抽象的 Provider 接口调用 T8STAR API。

## Technical Context

**Language/Version**: Python 3.12+
**Primary Dependencies**: click, loguru, requests
**Storage**: N/A (无状态 CLI)
**Testing**: pytest
**Target Platform**: Linux/macOS CLI
**Project Type**: CLI tool
**Performance Goals**: 单次请求 3 分钟内完成
**Constraints**: 依赖外部 API 可用性
**Scale/Scope**: 单用户命令行工具

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Test-First Development | ✅ Pass | TDD 流程适用于所有组件 |
| II. Simplicity First | ✅ Pass | 最小化设计，仅实现必需功能 |
| III. Modular Architecture | ✅ Pass | providers 模块实现接口抽象 |
| IV. Code Quality Standards | ✅ Pass | 使用 ruff + pytest |
| V. Incremental Delivery | ✅ Pass | 按 P1→P2→P3 优先级分阶段实现 |

## Project Structure

### Documentation (this feature)

```text
specs/001-image-gen-cli/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Technology decisions
├── data-model.md        # Entity definitions
├── quickstart.md        # Usage guide
├── contracts/
│   ├── cli.md           # CLI interface contract
│   └── provider.md      # Provider interface contract
├── checklists/
│   └── requirements.md  # Spec validation checklist
└── tasks.md             # Implementation tasks (via /speckit-tasks)
```

### Source Code (repository root)

```text
src/laodeng/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── generation.py      # GenerationRequest, GenerationResult
├── providers/
│   ├── __init__.py
│   ├── base.py            # ImageProvider ABC, exceptions
│   └── t8star.py          # T8StarProvider implementation
└── cli/
    ├── __init__.py
    └── gen_image.py       # CLI entry point (Click)

tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_models.py
│   └── test_providers.py
└── integration/
    ├── __init__.py
    └── test_cli.py
```

**Structure Decision**: 采用 src layout，将业务逻辑分为 models、providers、cli 三个模块。providers 模块遵循用户要求，实现 API 调用的抽象接口。

## Complexity Tracking

无违反 constitution 的情况，无需记录。

## Implementation Phases

### Phase 1: Core Models & Provider Interface (P1 基础)

1. 创建 `src/laodeng/models/generation.py` - 数据模型
2. 创建 `src/laodeng/providers/base.py` - 抽象接口和异常
3. 创建 `src/laodeng/providers/t8star.py` - T8STAR 实现
4. 单元测试覆盖

### Phase 2: CLI Implementation (P1 完成)

1. 创建 `src/laodeng/cli/gen_image.py` - Click CLI
2. 集成 loguru 日志
3. 错误处理和退出码
4. 集成测试

### Phase 3: Enhanced Features (P2/P3)

1. 参数验证增强
2. JSON 输出模式
3. 日志文件输出

## Next Steps

执行 `/speckit-tasks` 生成详细的任务列表。
