# database-adapter-boundary Specification

## Purpose
Define the persistence abstraction for authentication so the project can run
with a local development adapter today and swap to a real database adapter
later without changing route behavior.

## Requirements
### Requirement: User repository interface
The system SHALL access user records through a repository or adapter interface
instead of direct database calls from route handlers.

#### Scenario: Login user lookup
- **WHEN** the login service needs to find a user by username
- **THEN** it requests the user through the repository interface

#### Scenario: Current user lookup
- **WHEN** a protected endpoint needs the authenticated user's profile
- **THEN** it requests the user through the repository interface by user
  identifier

### Requirement: Development database adapter
The system SHALL include a development adapter or seed mechanism that allows
the login flow to run locally before a production database is connected.

#### Scenario: Local seeded user
- **WHEN** the backend runs with development configuration
- **THEN** the user repository can authenticate at least one documented seeded
  user through the normal login flow

### Requirement: Database configuration placeholder
The system SHALL expose database connection configuration without requiring a
concrete production database for the initial login implementation.

#### Scenario: Database URL configured
- **WHEN** a database URL is provided through environment configuration
- **THEN** the backend settings make that value available to database adapter
  initialization

#### Scenario: Database URL omitted
- **WHEN** no database URL is provided for local development
- **THEN** the backend can still start using the configured development adapter

### Requirement: Adapter replaceability
The system MUST keep authentication services independent from the concrete
persistence technology used by the user repository.

#### Scenario: Replace development adapter
- **WHEN** a future SQL-backed user repository implements the same user lookup
  contract
- **THEN** authentication routes and services do not require behavior changes
  to use the new adapter
