## Why

The workspace contains application code, OpenSpec artifacts, installed dependencies, caches, and build output, but it is not currently a Git repository. Initializing version control with a clean main-branch commit creates a stable baseline before further changes.

## What Changes

- Initialize a Git repository in the workspace if one does not already exist.
- Create or update a `.gitignore` that excludes generated and local-only artifacts such as `node_modules/`, `dist/`, Python cache directories, pytest cache, server logs, local environment files, and editor/OS noise.
- Stage source code, configuration examples, package lock files, documentation, and OpenSpec artifacts intended to be versioned.
- Set the active branch to `main`.
- Create an initial commit on `main` with a clear commit message.
- Verify the repository status after commit and confirm generated artifacts remain untracked/ignored.

## Capabilities

### New Capabilities

- `repository-version-control`: Covers initializing Git repository state, ignore rules, main branch setup, staging policy, commit creation, and post-commit verification.

### Modified Capabilities

- None.

## Impact

- Adds Git metadata under `.git/` and a tracked `.gitignore`.
- Creates a commit history baseline for existing application and OpenSpec files.
- Does not change application runtime behavior, API behavior, frontend behavior, dependency versions, or OpenSpec requirements.
- Generated local artifacts should remain out of version control.
