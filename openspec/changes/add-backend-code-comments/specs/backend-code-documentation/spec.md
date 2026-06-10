## ADDED Requirements

### Requirement: Backend file role comments
Backend Python source files SHALL include a file-level docstring or equivalent module comment that explains the file's responsibility.

#### Scenario: Backend module opened by a maintainer
- **WHEN** a maintainer opens a Python file under `backend/app/`
- **THEN** the file provides a concise explanation of what that module owns or exposes

#### Scenario: Generated backend files excluded
- **WHEN** generated cache files such as `__pycache__` artifacts are present
- **THEN** the change does not add or modify comments in generated artifacts

### Requirement: Function and class purpose comments
Backend functions and classes whose purpose, parameters, return value, or error behavior is not obvious SHALL include docstrings or targeted comments explaining those details.

#### Scenario: Authentication helper reviewed
- **WHEN** a maintainer reviews password hashing or token helper functions
- **THEN** comments or docstrings explain the meaning of relevant parameters, returned values, and validation failures

#### Scenario: FastAPI dependency reviewed
- **WHEN** a maintainer reviews dependency injection code
- **THEN** comments or docstrings explain how request credentials, repositories, and settings are resolved

### Requirement: Repository boundary explanation
The backend repository boundary SHALL be documented so future database adapters can be added without changing route behavior.

#### Scenario: Database adapter replacement
- **WHEN** a maintainer reviews the user repository interface and development adapter
- **THEN** comments explain which methods a future adapter must implement and why route handlers depend on the interface

### Requirement: Behavior-preserving documentation
The documentation change MUST NOT alter backend runtime behavior, API routes, response schemas, authentication semantics, dependency versions, or frontend files.

#### Scenario: Backend tests after comments
- **WHEN** backend tests run after comments are added
- **THEN** the same authentication and health-check tests pass without requiring behavior changes

### Requirement: Useful comment density
Comments SHALL explain intent and contracts rather than restating obvious syntax.

#### Scenario: Obvious code reviewed
- **WHEN** code contains straightforward imports, assignments, route decorators, or return statements
- **THEN** the implementation avoids adding comments that merely repeat the syntax
