-- V1__init.sql
-- Initial database schema

CREATE TABLE IF NOT EXISTS risk_item (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    score INTEGER NOT NULL CHECK (score >= 1 AND score <= 10),
    status VARCHAR(20) NOT NULL DEFAULT 'LOW',
    owner VARCHAR(255),
    due_date DATE,
    ai_description TEXT,
    ai_recommendations JSONB,
    ai_category VARCHAR(50),
    ai_confidence DECIMAL(3,2),
    file_path VARCHAR(500),
    created_by BIGINT,
    updated_by BIGINT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_risk_status ON risk_item(status);
CREATE INDEX idx_risk_category ON risk_item(category);
CREATE INDEX idx_risk_due_date ON risk_item(due_date);
CREATE INDEX idx_risk_deleted ON risk_item(deleted) WHERE deleted = FALSE;

CREATE TABLE IF NOT EXISTS app_user (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'VIEWER',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_email ON app_user(email);
