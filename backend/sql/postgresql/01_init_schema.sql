\set ON_ERROR_STOP on

CREATE SCHEMA IF NOT EXISTS cv_app;
COMMENT ON SCHEMA cv_app IS 'Application schema for CV platform data.';

CREATE TABLE IF NOT EXISTS cv_app.cv_profiles (
    cv_id BIGSERIAL PRIMARY KEY,
    cv_code VARCHAR(64) NOT NULL UNIQUE,
    title VARCHAR(255),
    ext_attributes JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE cv_app.cv_profiles IS 'Minimal CV profile table used to anchor user-to-CV relationships.';
COMMENT ON COLUMN cv_app.cv_profiles.cv_id IS 'CV primary key.';
COMMENT ON COLUMN cv_app.cv_profiles.cv_code IS 'Business-facing CV identifier.';
COMMENT ON COLUMN cv_app.cv_profiles.title IS 'Optional CV title or summary label.';
COMMENT ON COLUMN cv_app.cv_profiles.ext_attributes IS 'Reserved JSONB extension attributes for future CV metadata.';
COMMENT ON COLUMN cv_app.cv_profiles.created_at IS 'Row creation timestamp.';
COMMENT ON COLUMN cv_app.cv_profiles.updated_at IS 'Row update timestamp.';

CREATE TABLE IF NOT EXISTS cv_app.users (
    user_id BIGSERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    display_name VARCHAR(255) NOT NULL,
    password_hash TEXT NOT NULL,
    role_code VARCHAR(64) NOT NULL,
    permission_code VARCHAR(64) NOT NULL,
    cv_id BIGINT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    ext_attributes JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_users_username UNIQUE (username),
    CONSTRAINT fk_users_cv_id
        FOREIGN KEY (cv_id)
        REFERENCES cv_app.cv_profiles (cv_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

COMMENT ON TABLE cv_app.users IS 'Application user account table.';
COMMENT ON COLUMN cv_app.users.user_id IS 'User ID primary key.';
COMMENT ON COLUMN cv_app.users.username IS 'User login account; must be unique.';
COMMENT ON COLUMN cv_app.users.display_name IS 'Human-readable name shown in authenticated user profiles.';
COMMENT ON COLUMN cv_app.users.password_hash IS 'Hashed password value; plaintext passwords are never stored.';
COMMENT ON COLUMN cv_app.users.role_code IS 'Coarse-grained user role such as admin or editor.';
COMMENT ON COLUMN cv_app.users.permission_code IS 'Current permission label or access tier.';
COMMENT ON COLUMN cv_app.users.cv_id IS 'Associated CV identifier referencing cv_profiles.cv_id.';
COMMENT ON COLUMN cv_app.users.is_active IS 'Whether the user account is allowed to authenticate.';
COMMENT ON COLUMN cv_app.users.ext_attributes IS 'Reserved JSONB extension attributes for future user metadata.';
COMMENT ON COLUMN cv_app.users.created_at IS 'Row creation timestamp.';
COMMENT ON COLUMN cv_app.users.updated_at IS 'Row update timestamp.';

CREATE INDEX IF NOT EXISTS idx_users_role_code
    ON cv_app.users (role_code);

CREATE INDEX IF NOT EXISTS idx_users_permission_code
    ON cv_app.users (permission_code);

CREATE INDEX IF NOT EXISTS idx_users_cv_id
    ON cv_app.users (cv_id);

CREATE INDEX IF NOT EXISTS idx_users_ext_attributes_gin
    ON cv_app.users
    USING GIN (ext_attributes);

CREATE INDEX IF NOT EXISTS idx_cv_profiles_ext_attributes_gin
    ON cv_app.cv_profiles
    USING GIN (ext_attributes);
