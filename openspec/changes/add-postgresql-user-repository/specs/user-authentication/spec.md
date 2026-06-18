## MODIFIED Requirements

### Requirement: User login
The system SHALL allow a user with valid credentials to log in through the
FastAPI backend and receive an access token for authenticated API requests.

#### Scenario: Successful PostgreSQL-backed login
- **WHEN** a user submits a known PostgreSQL-backed username and matching password to the login endpoint
- **THEN** the system returns a successful response containing an access token,
  token type, expiration information, and basic user profile data

#### Scenario: Unknown account
- **WHEN** a user submits a username that does not exist in the active repository
- **THEN** the system rejects the request without an access token and returns a stable account-not-found response the frontend can display

#### Scenario: Incorrect password
- **WHEN** a user submits a known username with a non-matching password
- **THEN** the system rejects the request without an access token and returns an authentication failure response distinct from account-not-found

#### Scenario: Inactive account
- **WHEN** a user submits valid credentials for an inactive account
- **THEN** the system rejects the request without an access token and returns an inactive-account authentication failure response

### Requirement: Password verification
The system MUST verify user passwords using a password hashing mechanism rather
than comparing plaintext stored passwords.

#### Scenario: PostgreSQL password check uses hash
- **WHEN** the backend validates login credentials loaded from PostgreSQL
- **THEN** the backend compares the provided password against the stored
  `password_hash` using the configured password verification helper
