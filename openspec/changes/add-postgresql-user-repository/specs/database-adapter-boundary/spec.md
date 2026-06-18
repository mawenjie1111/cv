## MODIFIED Requirements

### Requirement: Database configuration placeholder
The system SHALL expose database connection configuration without requiring a
concrete production database for the initial login implementation, while also
supporting automatic selection of a concrete adapter when a database URL is
provided.

#### Scenario: Database URL configured
- **WHEN** a PostgreSQL database URL is provided through environment configuration
- **THEN** the backend initializes the PostgreSQL user repository instead of the development repository

#### Scenario: Database URL omitted
- **WHEN** no database URL is provided for local development
- **THEN** the backend starts using the configured development adapter

### Requirement: Adapter replaceability
The system MUST keep authentication services independent from the concrete
persistence technology used by the user repository.

#### Scenario: PostgreSQL adapter selected
- **WHEN** the backend authenticates against PostgreSQL
- **THEN** route handlers and token validation continue to depend on the same `UserRepository` contract

#### Scenario: Configured database unavailable
- **WHEN** a database URL is configured but the PostgreSQL adapter cannot initialize or query successfully
- **THEN** the backend fails clearly instead of silently falling back to the development repository
