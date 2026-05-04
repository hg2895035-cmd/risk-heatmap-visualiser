-- V3__rbac.sql
-- Role-based access control

CREATE TABLE IF NOT EXISTS app_role (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL
);

-- Seed default roles
INSERT INTO app_role (name) VALUES ('ADMIN'), ('MANAGER'), ('VIEWER')
ON CONFLICT (name) DO NOTHING;
