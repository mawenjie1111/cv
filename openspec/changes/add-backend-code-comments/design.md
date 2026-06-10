## Context

The backend was introduced as a compact FastAPI application with authentication endpoints, token helpers, dependency injection, repository boundaries, schemas, and tests. The code is small enough to understand, but several files contain security-sensitive or framework-driven behavior that benefits from explicit explanation for future maintainers.

This change is documentation-only. It should improve source readability without changing imports, public API behavior, route paths, response shapes, dependency versions, generated files, or frontend code.

## Goals / Non-Goals

**Goals:**

- Add file-level docstrings to backend Python files explaining each module's responsibility.
- Add class and function docstrings where they clarify purpose, parameters, return values, or error behavior.
- Add inline comments only where implementation intent is non-obvious, especially around authentication, hashing, token validation, dependency injection, and repository replacement.
- Add targeted comments to tests describing the contract each test protects.
- Keep comments accurate, concise, and useful to a developer reading or changing the backend.

**Non-Goals:**

- No behavior changes, refactors, endpoint changes, dependency changes, or frontend changes.
- No comments for generated files, cache files, build artifacts, or installed dependencies.
- No exhaustive line-by-line commenting that restates Python syntax.
- No new external documentation system.

## Decisions

1. Use Python docstrings for module, class, and function explanations.

   Docstrings are the native Python mechanism for explaining modules and callable contracts. Alternatives considered were separate Markdown-only documentation or only inline comments. Markdown would drift away from code, and inline-only comments are harder to discover through editor tooling.

2. Prefer parameter-focused docstrings on public helpers and boundary functions.

   Settings loaders, repository methods, token helpers, route handlers, and FastAPI dependencies are integration points. Their docstrings should explain what each parameter means and what the function returns or raises. Internal one-line helpers can remain lightly documented if names are sufficient.

3. Keep inline comments sparse and intent-driven.

   Inline comments should explain why a choice exists, not narrate obvious operations. This is especially important in security code: comments should clarify trust boundaries, token structure, constant-time comparisons, and repository substitution without creating noise.

4. Treat tests as documentation of behavior.

   Backend tests should receive short comments or docstrings only when they clarify the API contract being protected. The test names should remain the primary description.

## Risks / Trade-offs

- [Risk] Comments become stale after future behavior changes -> Mitigation: keep comments tied to stable intent and integration contracts, not incidental implementation details.
- [Risk] Too many comments reduce readability -> Mitigation: avoid comments that restate obvious assignments, imports, or route decorators.
- [Risk] Documentation accidentally changes behavior during editing -> Mitigation: run backend tests after applying the change and avoid structural rewrites.
- [Risk] Security comments reveal misleading guarantees -> Mitigation: describe current mechanics precisely and avoid overstating production readiness.

## Migration Plan

1. Add docstrings and targeted comments to backend source files under `backend/app/`.
2. Add focused explanatory comments to backend tests under `backend/tests/`.
3. Run backend tests to confirm behavior remains unchanged.
4. Review comments for accuracy, concision, and unnecessary noise.

Rollback is removing the added comments/docstrings. No data migration or deployment migration is required.

## Open Questions

- Should comments be written in English, Chinese, or a bilingual style? The existing code uses English identifiers and docs, so the default implementation should use English unless requested otherwise.
