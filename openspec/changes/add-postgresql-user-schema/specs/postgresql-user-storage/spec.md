## ADDED Requirements

### Requirement: PostgreSQL bootstrap artifacts
The project SHALL define repeatable PostgreSQL bootstrap artifacts for the first concrete user persistence schema.

#### Scenario: Fresh database initialization
- **WHEN** a maintainer provisions a new PostgreSQL environment for this project
- **THEN** the project provides SQL commands or scripts to create the target database, application schema, and required tables

### Requirement: User account table
The system SHALL define a PostgreSQL `users` table for persisted authentication records.

#### Scenario: Required user fields
- **WHEN** the `users` table is created
- **THEN** it includes at least `user_id`, `username`, `password_hash`, `role_code`, `permission_code`, `cv_id`, `ext_attributes`, `created_at`, and `updated_at`

#### Scenario: Unique login account
- **WHEN** two rows attempt to persist the same `username`
- **THEN** the database rejects the duplicate through a uniqueness constraint

#### Scenario: Safe password storage
- **WHEN** user credentials are persisted
- **THEN** the schema stores a password hash field instead of a plaintext password column

### Requirement: CV foreign key integrity
The system SHALL enforce referential integrity for the stored CV identifier.

#### Scenario: User linked to CV
- **WHEN** a user row contains a non-null `cv_id`
- **THEN** that value references an existing row in the PostgreSQL CV table through a foreign key constraint

### Requirement: Indexes and comments
The PostgreSQL schema SHALL be self-describing and support common lookup paths.

#### Scenario: Indexed user lookups
- **WHEN** the schema is created
- **THEN** it defines indexes appropriate for username uniqueness, authorization-field lookup, CV lookup, and JSONB extension querying

#### Scenario: Commented schema metadata
- **WHEN** a maintainer inspects the PostgreSQL schema
- **THEN** the schema exposes `COMMENT` metadata for the application schema, tables, and key columns

### Requirement: JSONB extension support
The PostgreSQL user schema SHALL reserve structured storage for future attributes that are not yet stable enough for dedicated columns.

#### Scenario: Future user metadata
- **WHEN** new optional user metadata must be stored before the relational model is finalized
- **THEN** the schema can persist that data in a non-null `JSONB` extension column with a default empty object
