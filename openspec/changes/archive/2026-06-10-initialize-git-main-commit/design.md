## Context

The workspace is not currently a Git repository. It contains application source, OpenSpec change artifacts, frontend installed dependencies, frontend build output, Python caches, logs, and local tooling directories. A clean initial commit should capture source and project metadata while excluding generated and local-only files.

## Goals / Non-Goals

**Goals:**

- Initialize a Git repository at the workspace root if `.git/` is absent.
- Ensure the default branch is named `main`.
- Add a `.gitignore` that keeps generated dependencies, build output, caches, logs, environment files, and local tooling state out of version control.
- Stage source files, documentation, dependency manifests/lockfiles, and OpenSpec artifacts that define the current project.
- Create one initial commit on `main` and verify the working tree is clean except for ignored files.

**Non-Goals:**

- No remote repository creation, push, pull, or credential setup.
- No rewriting existing Git history if a repository already exists.
- No application code changes beyond `.gitignore` if needed.
- No deletion of local generated files such as `node_modules/`, `dist/`, or cache directories.

## Decisions

1. Use `main` as the primary branch.

   The user explicitly asked to commit to the main branch. Alternatives such as `master` or a feature branch would not satisfy the request.

2. Track source and reproducibility metadata, ignore generated artifacts.

   Backend/frontend source, README, OpenSpec artifacts, `backend/requirements.txt`, `backend/pyproject.toml`, `frontend/package.json`, and `frontend/package-lock.json` should be versioned. `frontend/node_modules/`, `frontend/dist/`, Python `__pycache__/`, `.pytest_cache/`, server logs, and local `.env` files should remain untracked because they are generated or machine-specific.

3. Exclude local assistant/tooling state by default.

   The `.codex/` directory contains local workflow tooling and personal environment context. It should not be staged unless the user explicitly asks to version it. OpenSpec project files under `openspec/` are project artifacts and should be staged.

4. Use non-interactive Git commands.

   Implementation should avoid interactive Git flows. If Git user identity is missing and commit fails, pause and ask for the desired `user.name` and `user.email` rather than inventing identity values.

## Risks / Trade-offs

- [Risk] Accidentally committing generated dependencies or logs -> Mitigation: write `.gitignore` before staging and verify `git status --short --ignored` as needed.
- [Risk] Missing important project metadata -> Mitigation: inspect `git status --short` after staging to confirm intended source, lockfiles, docs, and OpenSpec artifacts are included.
- [Risk] Existing Git repository appears during apply -> Mitigation: inspect current repository state before initializing and avoid history rewrites.
- [Risk] Commit fails because Git identity is unset -> Mitigation: report the exact failure and ask the user for identity configuration.

## Migration Plan

1. Check whether `.git/` exists.
2. Create or update `.gitignore` at the workspace root.
3. Initialize Git if needed and ensure the branch is `main`.
4. Stage intended project files while respecting `.gitignore`.
5. Review staged files.
6. Create the initial commit.
7. Verify branch name and working tree state.

Rollback before pushing is local-only: remove the commit or repository metadata if the user asks for that explicitly. No application data migration is involved.

## Open Questions

- What commit author identity should be used if the local Git configuration does not already define `user.name` and `user.email`?
