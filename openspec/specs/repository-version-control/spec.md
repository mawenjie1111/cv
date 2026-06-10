# repository-version-control Specification

## Purpose
Define how this project initializes and verifies local Git version control,
including repository creation, main-branch baseline commits, ignore rules, and
post-commit status checks.
## Requirements
### Requirement: Git repository initialization
The workspace SHALL be initialized as a Git repository when no repository exists.

#### Scenario: Repository is absent
- **WHEN** `.git/` is absent at the workspace root
- **THEN** the implementation initializes a Git repository in the workspace root

#### Scenario: Repository already exists
- **WHEN** `.git/` already exists at the workspace root
- **THEN** the implementation uses the existing repository without rewriting history

### Requirement: Main branch baseline
The repository SHALL use `main` as the active branch for the initial baseline commit.

#### Scenario: Branch after initialization
- **WHEN** repository initialization or branch setup completes
- **THEN** the active branch is named `main`

### Requirement: Generated artifact ignore rules
The repository SHALL ignore generated dependencies, build outputs, caches, logs, local environment files, and local tooling state.

#### Scenario: Ignore generated files
- **WHEN** frontend dependencies, frontend build output, Python cache files, pytest cache, server logs, local environment files, or `.codex/` are present
- **THEN** those files are not staged for the baseline commit

### Requirement: Source baseline commit
The repository SHALL create an initial commit containing project source, documentation, dependency manifests, package lockfiles, and OpenSpec project artifacts.

#### Scenario: Initial commit created
- **WHEN** intended files are staged
- **THEN** Git creates a commit on `main` with a clear initial-commit message

#### Scenario: Commit identity missing
- **WHEN** Git cannot create the commit because `user.name` or `user.email` is missing
- **THEN** the implementation reports the issue and asks the user for the desired Git identity

### Requirement: Post-commit verification
The implementation SHALL verify repository state after the commit.

#### Scenario: Verify branch and status
- **WHEN** the initial commit has been attempted
- **THEN** the implementation reports the active branch, commit summary, and whether the working tree is clean except for ignored files
