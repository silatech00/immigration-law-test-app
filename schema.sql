-- User profiles and chat session storage for Immigration Law AI

CREATE TABLE IF NOT EXISTS user_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL UNIQUE,
    passport_number TEXT,
    nationality TEXT,
    ethnicity TEXT,
    criminal_record TEXT,
    social_security_number TEXT,
    current_latitude REAL,
    current_longitude REAL,
    destination_country TEXT,
    current_country TEXT,
    visa_type TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS eligibility_assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    destination_country TEXT NOT NULL,
    visa_eligibility_score REAL,
    recommended_visa_type TEXT,
    automated_recommendation TEXT,
    risk_flags TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_chat_session ON chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_eligibility_session ON eligibility_assessments(session_id);
