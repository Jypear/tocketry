# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Tocketry is a modern statement-based scheduling framework for Python. It's a fork of Rocketry that aims to be lighter without requiring pydantic as a dependency (though it currently still uses pydantic). The project provides powerful scheduling capabilities with support for concurrency, parametrization, task pipelining, and async operations.

## Development Commands

### Testing
- Run all tests: `pytest --pyargs tocketry -r chars`
- Run tests with coverage: `pytest --cov=tocketry --cov-report=html tocketry/test`
- Run single test module: `pytest tocketry/test/path/to/test_file.py`
- Run single test: `pytest tocketry/test/path/to/test_file.py::test_function_name`

**IMPORTANT**: Always run tests after making changes, especially during major refactoring like pydantic removal. Use `pytest --pyargs tocketry -r chars` for quick validation and full coverage tests before committing.

### Code Quality
- Lint code: `ruff check` (configured in pyproject.toml with line-length 120)
- Format code: `ruff format` (follows ruff configuration)

### Documentation
- Build docs: `sphinx-build docs "docs/_build/html" --color -W -bhtml`
- Or using tox: `tox -e docs`

### Package Management
- Install in development mode: `pip install -e .`
- Install with test dependencies: `pip install -e .[test]`
- Install with docs dependencies: `pip install -e .[docs]`

### Build and Release
- Build package: `python setup.py bdist_wheel sdist`
- Using tox: `tox -e build`

## Architecture Overview

### Core Components

**Session (`tocketry/session.py`)**: Central orchestrator that manages tasks, parameters, scheduler configuration, and execution. Uses pydantic BaseModel for configuration management.

**Application (`tocketry/application.py`)**: User-facing API through the `Tocketry` class. Provides decorators for creating tasks (`@app.task`), conditions (`@app.cond`), and parameters (`@app.param`).

**Core Module (`tocketry/core/`)**: Contains fundamental building blocks:
- `Task`: Represents executable units of work
- `Scheduler`: Manages task execution timing and coordination  
- `BaseCondition`: Base class for scheduling conditions
- `Parameters`: Handles parameter injection and management
- `TimePeriod`: Time-based scheduling primitives

**Conditions (`tocketry/conditions/`)**: Scheduling logic including time-based conditions, task dependencies, and custom condition support.

**Tasks (`tocketry/tasks/`)**: Different task types including function tasks, command tasks, and code tasks with various execution modes (sync, async, thread, process).

### Key Patterns

**Statement-based Scheduling**: Uses condition objects that can be combined with logical operators (`&`, `|`) to create complex scheduling rules.

**Execution Modes**: Tasks support multiple execution contexts:
- `"main"`: Synchronous execution in main thread
- `"async"`: Asynchronous execution 
- `"thread"`: Separate thread execution
- `"process"`: Separate process execution

**Parameter Injection**: Uses a dependency injection system where task functions can receive computed parameters, return values from other tasks, and external arguments.

**Pipelining**: Tasks can depend on other tasks and receive their return values through the `Return` argument.

## Important Notes

- The project currently uses pydantic despite goals to remove this dependency
- Tests are located within the package at `tocketry/test/` rather than a separate `tests/` directory
- The project includes an embedded `redbird` module for repository patterns and `pybox` for utilities
- Documentation uses Sphinx and is configured for ReadTheDocs deployment
- Coverage reports are generated to `htmlcov/` directory