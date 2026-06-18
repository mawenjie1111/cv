\set ON_ERROR_STOP on

SELECT
    'CREATE DATABASE cv_db WITH ENCODING ''UTF8'' TEMPLATE template0'
WHERE NOT EXISTS (
    SELECT 1
    FROM pg_database
    WHERE datname = 'cv_db'
)\gexec
