-- =============================================================================
-- Computer Vision & Real-Time Person Analytics System
-- Database Initialization Script
-- =============================================================================

-- Enable pgvector extension for face embedding storage & similarity search
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- Persons table: stores registered person information
-- =============================================================================
CREATE TABLE IF NOT EXISTS persons (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id       VARCHAR(50) UNIQUE NOT NULL,
    name            VARCHAR(255) NOT NULL,
    email           VARCHAR(255),
    phone           VARCHAR(50),
    department      VARCHAR(255),
    role            VARCHAR(255),
    additional_info JSONB DEFAULT '{}',
    face_image_path VARCHAR(500),
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active       BOOLEAN DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS idx_persons_person_id ON persons(person_id);
CREATE INDEX IF NOT EXISTS idx_persons_is_active ON persons(is_active);
CREATE INDEX IF NOT EXISTS idx_persons_name ON persons(name);
CREATE INDEX IF NOT EXISTS idx_persons_department ON persons(department);

-- =============================================================================
-- Face embeddings table: stores ArcFace 512-dim embeddings with pgvector
-- =============================================================================
CREATE TABLE IF NOT EXISTS face_embeddings (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    person_id           UUID NOT NULL REFERENCES persons(id) ON DELETE CASCADE,
    embedding           VECTOR(512) NOT NULL,
    model_name          VARCHAR(100) NOT NULL DEFAULT 'buffalo_l',
    embedding_dimension INTEGER NOT NULL DEFAULT 512,
    quality_score       FLOAT DEFAULT 0.0,
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at          TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_face_embeddings_person_id ON face_embeddings(person_id);

-- HNSW index for fast cosine similarity search on face embeddings
-- m=16: connections per layer; ef_construction=64: build-time search width
CREATE INDEX IF NOT EXISTS idx_face_embeddings_hnsw
    ON face_embeddings
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- =============================================================================
-- Detection events table: stores periodic detection snapshots
-- =============================================================================
CREATE TABLE IF NOT EXISTS detection_events (
    id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tracking_id             INTEGER NOT NULL,
    person_id               UUID REFERENCES persons(id) ON DELETE SET NULL,
    hands_count             INTEGER DEFAULT 0,
    fingers_count           INTEGER DEFAULT 0,
    eye_state               VARCHAR(50) DEFAULT 'unknown',
    awake_status            VARCHAR(50) DEFAULT 'unknown',
    estimated_expression    VARCHAR(50) DEFAULT 'unknown',
    expression_confidence   FLOAT DEFAULT 0.0,
    face_confidence         FLOAT DEFAULT 0.0,
    bbox                    JSONB,
    timestamp               TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_detection_events_person_id ON detection_events(person_id);
CREATE INDEX IF NOT EXISTS idx_detection_events_timestamp ON detection_events(timestamp);
CREATE INDEX IF NOT EXISTS idx_detection_events_tracking_id ON detection_events(tracking_id);

-- =============================================================================
-- Function: auto-update updated_at on row modification
-- =============================================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_persons_updated_at
    BEFORE UPDATE ON persons
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trigger_face_embeddings_updated_at
    BEFORE UPDATE ON face_embeddings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- Cleanup: automatic deletion of old detection events (optional)
-- Run periodically via cron or application-level scheduler
-- =============================================================================
-- DELETE FROM detection_events WHERE timestamp < NOW() - INTERVAL '30 days';
