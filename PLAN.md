# Plan for Removing Pydantic Dependency from Tocketry

## Analysis Summary

**Pydantic Usage Distribution:**
- **Core Components**: 5 main classes (Config, Session, Task, LogRecord models, Dependencies)
- **Redbird Module**: Extensive usage in repository abstractions (7+ classes)  
- **Validation**: 20+ field validators and 2 model validators
- **Configuration**: Heavy reliance on ConfigDict for model behavior

## Migration Strategy

### Phase 1: Core Infrastructure (High Priority)
**Goal**: Replace core pydantic models with dataclasses/plain classes

1. **Config Class** (`session.py:53`):
   - Replace `BaseModel` with `@dataclass` 
   - Convert 20+ configuration fields to dataclass fields
   - Implement manual validation for `execution`, `shut_cond`, `timeout`
   - Add custom `__post_init__` for model validation logic

2. **Session Class** (`session.py:153`):
   - Remove `ConfigDict(arbitrary_types_allowed=True)`
   - Replace with standard class inheritance
   - Maintain existing initialization pattern

3. **Task Class** (`core/task.py:127`):
   - Most complex migration - inherits from both `BaseModel` and `RedBase`
   - 15+ field validators need manual implementation
   - Critical for all task types (FuncTask, CommandTask)

### Phase 2: Logging Infrastructure (Medium Priority)
**Goal**: Replace log record models

4. **Log Record Models** (`log/log_record.py`):
   - `MinimalRecord`, `LogRecord`, `TaskLogRecord` classes
   - 3 field validators for datetime/timedelta conversion
   - Replace with dataclasses + utility functions

### Phase 3: Repository Layer (Low Priority - Consider Scope)
**Goal**: Evaluate redbird module necessity

5. **Redbird Module Assessment**:
   - **Option A**: Keep as-is (maintain pydantic for this subsystem only)
   - **Option B**: Replace with simpler repository pattern
   - **Option C**: Remove entirely if not essential

## Implementation Approach

### Validation Strategy
**Replace pydantic validators with:**
- Custom validation functions
- `__post_init__` methods in dataclasses
- Property setters for runtime validation
- Type hints + runtime type checking (optional)

### Configuration Management
**Replace ConfigDict with:**
- Standard dataclass configuration
- Custom `__setattr__` for assignment validation
- Manual arbitrary type handling where needed

### Field Definitions
**Replace pydantic Field() with:**
- Dataclass field() with metadata
- Default values in field definitions
- Custom descriptors for complex fields

## Risk Assessment

**High Risk Areas:**
- Task validation logic (execution modes, conditions)
- Session configuration validation
- Serialization/deserialization of task parameters

**Migration Dependencies:**
- Task class must be migrated before FuncTask/CommandTask
- Config class before Session class
- Consider test coverage during migration

## Testing Strategy
- Maintain existing test suite functionality
- Add validation tests for new manual validation logic
- Ensure backward compatibility during transition
- Performance benchmarking (pydantic removal should improve performance)

**Estimated Effort**: 3-5 days for core components, +2-3 days if including redbird module migration

## Implementation Progress

### Phase 1: Core Infrastructure
- [ ] Config class migration
- [ ] Session class migration  
- [ ] Task class migration

### Phase 2: Logging Infrastructure
- [ ] Log record models migration

### Phase 3: Dependency Updates
- [ ] Remove pydantic from pyproject.toml
- [ ] Update imports across codebase
- [ ] Test suite validation