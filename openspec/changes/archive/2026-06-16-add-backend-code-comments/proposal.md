## Why

The backend now contains authentication, token handling, repository boundaries, and configuration logic that future developers will need to understand before extending it. Adding clear file-level and targeted code comments will reduce onboarding friction while keeping behavior unchanged.

## What Changes

- Add concise file-level docstrings or module comments to backend Python source files describing each file's responsibility.
- Add docstrings or inline comments to backend functions, classes, and helpers where parameter meaning, return value, or implementation intent is not obvious from names alone.
- Add explanatory comments for authentication-sensitive logic such as password hashing, token signing/verification, repository lookup, dependency injection, and route protection.
- Add comments to backend tests where they clarify which behavior or API contract the test protects.
- Avoid noisy comments that simply restate obvious syntax.
- Do not change runtime behavior, public API shape, dependency versions, or frontend code.

## Capabilities

### New Capabilities

- `backend-code-documentation`: Covers maintainable backend source comments, file role descriptions, function/class docstrings, parameter meaning, and behavior-preserving documentation for backend code.

### Modified Capabilities

- None.

## Impact

- Affects backend Python source and backend tests under `backend/app/` and `backend/tests/`.
- Does not affect frontend files, generated cache/build artifacts, API behavior, authentication semantics, dependency installation, database adapter behavior, or runtime configuration.
- Verification should confirm backend tests still pass after documentation-only changes.
