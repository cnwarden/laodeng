<!--
Sync Impact Report
==================
Version change: 0.0.0 → 1.0.0 (MAJOR: Initial constitution ratification)

Modified principles: N/A (initial creation)

Added sections:
- Core Principles (5 principles)
- Technology Stack
- Development Workflow
- Governance

Removed sections: N/A

Templates requiring updates:
- .specify/templates/plan-template.md: ✅ Compatible (Constitution Check section exists)
- .specify/templates/spec-template.md: ✅ Compatible (user stories, requirements sections align)
- .specify/templates/tasks-template.md: ✅ Compatible (test-first workflow aligned)

Follow-up TODOs: None
-->

# laodeng Constitution

## Core Principles

### I. Test-First Development (NON-NEGOTIABLE)

All new functionality MUST follow the TDD cycle:

1. **Write test first** - Define expected behavior before implementation
2. **Verify test fails** - Confirm test is valid (red phase)
3. **Implement minimal code** - Only enough to pass the test (green phase)
4. **Refactor** - Clean up while keeping tests passing

**Rationale**: Tests written after implementation often miss edge cases and become
documentation of implementation rather than specification of behavior. Test-first
ensures testable design and complete coverage.

### II. Simplicity First

All solutions MUST prefer the simplest approach that works:

- Single responsibility per function/class
- No premature abstractions - extract only when pattern repeats 3+ times
- Choose boring, obvious solutions over clever ones
- If explanation is needed, the code is too complex
- YAGNI (You Aren't Gonna Need It) - build only what's needed now

**Rationale**: Complexity is the primary enemy of maintainability. Simple code is
easier to understand, test, debug, and modify.

### III. Modular Architecture

Code MUST be organized into well-defined, loosely-coupled modules:

- Each module has a single, clear purpose
- Dependencies flow in one direction (no circular dependencies)
- Modules communicate through explicit interfaces
- Internal implementation details stay private

**Rationale**: Modular design enables parallel development, isolated testing,
and incremental refactoring without system-wide impact.

### IV. Code Quality Standards

All code MUST meet these quality gates before merge:

- **Passes all tests** - No skipped or disabled tests
- **No linter warnings** - `ruff check .` returns clean
- **Properly formatted** - `ruff format .` makes no changes
- **Clear commit messages** - Explain "why", not just "what"
- **Compiles successfully** - No runtime import errors

**Rationale**: Consistent quality standards prevent technical debt accumulation
and keep the codebase in a deployable state.

### V. Incremental Delivery

Changes MUST be delivered in small, working increments:

- Each commit represents a complete, working state
- Maximum 3 attempts per problem - then reassess approach
- Break large features into independently testable user stories
- Prefer many small PRs over few large PRs

**Rationale**: Small increments reduce risk, enable faster feedback, and make
code review more effective.

## Technology Stack

**Language**: Python 3.12+
**Package Manager**: uv
**Test Framework**: pytest
**Linting/Formatting**: ruff
**Project Structure**: src layout with separate tests directory

```text
laodeng/
├── src/laodeng/      # Application code
├── tests/            # Test code
├── main.py           # Entry point
└── pyproject.toml    # Project configuration
```

## Development Workflow

### Standard Development Cycle

1. **Understand** - Study existing patterns in codebase
2. **Plan** - Break work into testable increments
3. **Test** - Write failing test for next increment
4. **Implement** - Minimal code to pass test
5. **Refactor** - Clean up with tests passing
6. **Commit** - With clear message linking to requirement

### Quality Gates

Before any merge:

- [ ] All tests pass: `uv run pytest`
- [ ] No lint errors: `uv run ruff check .`
- [ ] Code formatted: `uv run ruff format .`
- [ ] Commit messages are clear and explain intent

### Problem Resolution

When stuck after 3 attempts:

1. Document what was tried and why it failed
2. Research 2-3 alternative approaches
3. Question if a simpler solution exists
4. Ask for help before continuing

## Governance

This constitution supersedes all other development practices for the laodeng project.

**Amendment Process**:

1. Propose change with rationale
2. Document impact on existing code
3. Update constitution version according to semantic versioning:
   - MAJOR: Principle removal or incompatible redefinition
   - MINOR: New principle or significant expansion
   - PATCH: Clarification or wording fix

**Compliance**: All PRs and code reviews MUST verify adherence to these principles.
Violations require explicit justification in the Complexity Tracking section of
implementation plans.

**Version**: 1.0.0 | **Ratified**: 2026-04-25 | **Last Amended**: 2026-04-25
