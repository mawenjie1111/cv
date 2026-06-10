## 1. Repository State Review

- [x] 1.1 Check whether `.git/` exists at the workspace root.
- [x] 1.2 Inspect top-level workspace contents and identify source files, generated files, logs, caches, and local tooling directories.
- [x] 1.3 Check local Git author identity with `git config user.name` and `git config user.email`.

## 2. Ignore Rules

- [x] 2.1 Create or update `.gitignore` with Python cache, pytest cache, frontend dependencies, build output, logs, local environment files, editor files, OS files, and `.codex/`.
- [x] 2.2 Verify intended generated artifacts are ignored before staging.

## 3. Git Initialization

- [x] 3.1 Initialize the repository if `.git/` is absent.
- [x] 3.2 Ensure the active branch is named `main`.

## 4. Staging and Commit

- [x] 4.1 Stage intended project files: backend source/tests/config, frontend source/config/package files, README, and OpenSpec artifacts.
- [x] 4.2 Review staged files to confirm generated artifacts and local tooling are excluded.
- [x] 4.3 Create the initial commit on `main` with a clear commit message.

## 5. Verification

- [x] 5.1 Verify the latest commit summary.
- [x] 5.2 Verify the active branch is `main`.
- [x] 5.3 Verify the working tree is clean except for ignored files.
