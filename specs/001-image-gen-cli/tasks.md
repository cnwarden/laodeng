# Tasks: Image Generation CLI

**Input**: Design documents from `specs/001-image-gen-cli/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: TDD 模式 - 测试先行，遵循 constitution 中的 Test-First Development 原则

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Add runtime dependencies (click, loguru, requests) via `uv add click loguru requests`
- [X] T002 [P] Create src/laodeng directory structure with __init__.py files
- [X] T003 [P] Create src/laodeng/models/__init__.py and src/laodeng/models/generation.py (empty)
- [X] T004 [P] Create src/laodeng/providers/__init__.py and src/laodeng/providers/base.py (empty)
- [X] T005 [P] Create src/laodeng/cli/__init__.py and src/laodeng/cli/gen_image.py (empty)
- [X] T006 [P] Create tests/unit/__init__.py, tests/unit/test_models.py, tests/unit/test_providers.py (empty)
- [X] T007 [P] Create tests/integration/__init__.py, tests/integration/test_cli.py (empty)

**Checkpoint**: Project structure ready for implementation ✅

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core models and provider interface that all user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Tests First (TDD)

- [X] T008 [P] Write unit tests for GenerationRequest validation in tests/unit/test_models.py
- [X] T009 [P] Write unit tests for GenerationResult dataclass in tests/unit/test_models.py
- [X] T010 [P] Write unit tests for ProviderError exception hierarchy in tests/unit/test_providers.py

### Implementation

- [X] T011 Implement GenerationRequest dataclass with validation in src/laodeng/models/generation.py
- [X] T012 Implement GenerationResult dataclass in src/laodeng/models/generation.py
- [X] T013 Export models from src/laodeng/models/__init__.py
- [X] T014 Implement exception hierarchy (ProviderError, AuthenticationError, NetworkError, APIError, ValidationError) in src/laodeng/providers/base.py
- [X] T015 Implement ImageProvider abstract base class in src/laodeng/providers/base.py
- [X] T016 Export base classes and exceptions from src/laodeng/providers/__init__.py

**Checkpoint**: Foundation ready - user story implementation can now begin ✅

---

## Phase 3: User Story 1 - Basic Image Generation (Priority: P1) 🎯 MVP

**Goal**: Users can generate an image by providing a text prompt via command line

**Independent Test**: Run `uv run python -m laodeng.cli.gen_image "A sunset"` and verify image URL is returned

### Tests for User Story 1 (TDD)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T017 [P] [US1] Write unit tests for T8StarProvider.__init__ (env var reading, auth error) in tests/unit/test_providers.py
- [X] T018 [P] [US1] Write unit tests for T8StarProvider.generate (success case, mock API) in tests/unit/test_providers.py
- [X] T019 [P] [US1] Write unit tests for T8StarProvider error handling (timeout, network, API errors) in tests/unit/test_providers.py
- [X] T020 [P] [US1] Write integration test for CLI basic invocation in tests/integration/test_cli.py

### Implementation for User Story 1

- [X] T021 [US1] Implement T8StarProvider.__init__ (read T8STAR_TOKEN env var) in src/laodeng/providers/t8star.py
- [X] T022 [US1] Implement T8StarProvider.generate (API call with requests) in src/laodeng/providers/t8star.py
- [X] T023 [US1] Implement T8StarProvider.name property in src/laodeng/providers/t8star.py
- [X] T024 [US1] Add error handling to T8StarProvider (map HTTP errors to exceptions) in src/laodeng/providers/t8star.py
- [X] T025 [US1] Export T8StarProvider from src/laodeng/providers/__init__.py
- [X] T026 [US1] Implement CLI entry point with Click (@click.command, prompt argument) in src/laodeng/cli/gen_image.py
- [X] T027 [US1] Configure loguru logging (console output with timestamps) in src/laodeng/cli/gen_image.py
- [X] T028 [US1] Implement main CLI logic (create provider, generate, display URL) in src/laodeng/cli/gen_image.py
- [X] T029 [US1] Implement exit codes (0=success, 1-5=errors per contract) in src/laodeng/cli/gen_image.py
- [X] T030 [US1] Add __main__.py to src/laodeng/cli/ for `python -m` invocation

**Checkpoint**: User Story 1 complete - basic image generation works with prompt only ✅

---

## Phase 4: User Story 2 - Configurable Image Parameters (Priority: P2)

**Goal**: Users can specify image dimensions and model options via CLI parameters

**Independent Test**: Run `uv run python -m laodeng.cli.gen_image "A sunset" --size 1024x1024 --model gpt-image-2` and verify parameters are used

### Tests for User Story 2 (TDD)

- [X] T031 [P] [US2] Write unit tests for size parameter validation (WIDTHxHEIGHT format) in tests/unit/test_models.py
- [X] T032 [P] [US2] Write integration test for CLI with --size and --model options in tests/integration/test_cli.py

### Implementation for User Story 2

- [X] T033 [US2] Add --size option to CLI with default 1024x1536 in src/laodeng/cli/gen_image.py
- [X] T034 [US2] Add --model option to CLI with default gpt-image-2 in src/laodeng/cli/gen_image.py
- [X] T035 [US2] Add --timeout option to CLI with default 180 in src/laodeng/cli/gen_image.py
- [X] T036 [US2] Add size validation (regex pattern \d+x\d+) in src/laodeng/cli/gen_image.py
- [X] T037 [US2] Pass parameters through to GenerationRequest and provider in src/laodeng/cli/gen_image.py

**Checkpoint**: User Story 2 complete - customizable image generation works ✅

---

## Phase 5: User Story 3 - Reference Image Support (Priority: P3)

**Goal**: Users can include reference image URLs in prompts for guided generation

**Independent Test**: Run `uv run python -m laodeng.cli.gen_image "A person like this: https://example.com/ref.jpg"` and verify generation proceeds

### Tests for User Story 3 (TDD)

- [X] T038 [P] [US3] Write unit test for prompt containing URL in tests/unit/test_providers.py
- [X] T039 [P] [US3] Write integration test for CLI with reference URL in prompt in tests/integration/test_cli.py

### Implementation for User Story 3

- [X] T040 [US3] Update T8StarProvider to handle prompts with reference URLs in src/laodeng/providers/t8star.py
- [X] T041 [US3] Add logging for detected reference URLs in src/laodeng/cli/gen_image.py

**Checkpoint**: User Story 3 complete - reference image support works ✅

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T042 [P] Add --json flag for JSON output format in src/laodeng/cli/gen_image.py
- [X] T043 [P] Add --verbose flag for detailed logging in src/laodeng/cli/gen_image.py
- [X] T044 Verify all tests pass with `uv run pytest -v`
- [X] T045 Run `uv run ruff check .` and fix any linting issues
- [X] T046 Run `uv run ruff format .` for code formatting
- [X] T047 Validate quickstart.md examples work correctly

**Checkpoint**: All phases complete ✅

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1 CLI but is independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Builds on US1 provider but is independently testable

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD)
- Models before services
- Provider implementation before CLI integration
- Core implementation before enhancements

### Parallel Opportunities

**Phase 1 (Setup)**:
- T002, T003, T004, T005, T006, T007 can run in parallel

**Phase 2 (Foundational Tests)**:
- T008, T009, T010 can run in parallel

**Phase 3 (US1 Tests)**:
- T017, T018, T019, T020 can run in parallel

**Phase 4 (US2 Tests)**:
- T031, T032 can run in parallel

**Phase 5 (US3 Tests)**:
- T038, T039 can run in parallel

**Phase 6 (Polish)**:
- T042, T043 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (TDD - write first, watch fail):
Task T017: "Write unit tests for T8StarProvider.__init__"
Task T018: "Write unit tests for T8StarProvider.generate"
Task T019: "Write unit tests for T8StarProvider error handling"
Task T020: "Write integration test for CLI basic invocation"

# Then implement sequentially (to make tests pass):
Task T021 → T022 → T023 → T024 → T025 (Provider)
Task T026 → T027 → T028 → T029 → T030 (CLI)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test with `uv run python -m laodeng.cli.gen_image "A test prompt"`
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → MVP ready!
3. Add User Story 2 → Test independently → Customization enabled
4. Add User Story 3 → Test independently → Reference images supported
5. Polish → Production ready

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- TDD: Write tests first, verify they fail, then implement
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
