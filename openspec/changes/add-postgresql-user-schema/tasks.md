## 1. Bootstrap Scope

- [x] 1.1 Confirm the database name, schema name, and whether `BIGSERIAL` is acceptable for `user_id` and `cv_id`.
- [x] 1.2 Confirm that `role_code` and `permission_code` are the intended interpretations of the requested permission-related fields.

## 2. PostgreSQL Initialization Artifacts

- [x] 2.1 Add a repeatable PostgreSQL initialization SQL file that creates the application schema inside the target database.
- [x] 2.2 Add table definitions for `cv_profiles` and `users` with the agreed column names and field types.
- [x] 2.3 Add primary key, unique constraint, foreign key, default values, and timestamp columns.

## 3. Indexes and Metadata

- [x] 3.1 Add B-tree indexes for `role_code`, `permission_code`, and `cv_id`.
- [x] 3.2 Add a GIN index for the `ext_attributes` JSONB column.
- [x] 3.3 Add `COMMENT` statements for the schema, tables, and key columns.

## 4. Documentation and Handoff

- [x] 4.1 Document PostgreSQL bootstrap steps and a sample `DATABASE_URL` in backend setup docs or environment examples.
- [x] 4.2 Document that `password_hash` stores hashed credentials and that plaintext passwords must never be persisted.
- [x] 4.3 Document follow-up work needed to connect the PostgreSQL schema to the existing `UserRepository` boundary.
