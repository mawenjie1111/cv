## ADDED Requirements

### Requirement: Backend application shell
The system SHALL provide a FastAPI application entrypoint with structured routing, configuration loading, health checks, authentication routes, and protected user routes.

#### Scenario: Health check
- **WHEN** a client requests the backend health endpoint
- **THEN** the system returns a successful response indicating the API is running

#### Scenario: API route organization
- **WHEN** backend routes are implemented
- **THEN** public health routes, authentication routes, and protected user routes are organized under clear FastAPI routers or modules

### Requirement: Frontend application shell
The system SHALL provide a Vue application with routing, login view, authenticated app view, and a shared API client configured by environment.

#### Scenario: Login page render
- **WHEN** an unauthenticated user opens the frontend application
- **THEN** the system displays the login view instead of the authenticated app view

#### Scenario: Authenticated page render
- **WHEN** an authenticated user opens a protected frontend route
- **THEN** the system displays the authenticated application view with the current user's identity available

### Requirement: Route protection
The Vue application SHALL prevent unauthenticated users from viewing protected frontend routes.

#### Scenario: Unauthenticated protected route access
- **WHEN** a user without a stored valid authentication token navigates to a protected route
- **THEN** the frontend redirects the user to the login route

#### Scenario: Authenticated protected route access
- **WHEN** a user with valid authentication state navigates to a protected route
- **THEN** the frontend allows the route navigation to complete

### Requirement: API integration
The Vue application SHALL call backend API endpoints through a centralized API client that applies the configured base URL and authentication header.

#### Scenario: Authenticated API request
- **WHEN** the frontend sends a protected API request while a token is stored
- **THEN** the request includes the bearer token in the authorization header

#### Scenario: API base URL configuration
- **WHEN** the frontend application is built or run in development
- **THEN** the API client uses the configured API base URL from the environment or documented default
