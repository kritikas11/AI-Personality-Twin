-- AI Personality Twin Database Schema
-- SQLite Database

-- Profiles Table
-- Stores user personality profiles and analysis results
CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    text_input TEXT NOT NULL,
    personality_traits TEXT NOT NULL,  -- JSON format: {"Creative": 85.5, "Optimistic": 72.3}
    emotion TEXT,                       -- Detected emotion: happy, sad, neutral, etc.
    sentiment_score REAL,               -- Sentiment polarity: -1.0 to 1.0
    avatar_url TEXT,                    -- DiceBear avatar URL
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CHECK(length(name) >= 2 AND length(name) <= 50),
    CHECK(length(text_input) >= 10),
    CHECK(sentiment_score >= -1.0 AND sentiment_score <= 1.0)
);

-- Index for faster queries by name
CREATE INDEX IF NOT EXISTS idx_profiles_name ON profiles(name);

-- Index for faster queries by creation date
CREATE INDEX IF NOT EXISTS idx_profiles_created_at ON profiles(created_at DESC);

-- Index for emotion analysis
CREATE INDEX IF NOT EXISTS idx_profiles_emotion ON profiles(emotion);

-- Optional: User Sessions Table (for future use)
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT UNIQUE NOT NULL,
    user_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optional: Trait Statistics Table (for analytics)
CREATE TABLE IF NOT EXISTS trait_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trait_name TEXT NOT NULL,
    total_count INTEGER DEFAULT 0,
    avg_confidence REAL DEFAULT 0.0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(trait_name)
);

-- Trigger to update last_activity in sessions
CREATE TRIGGER IF NOT EXISTS update_session_activity
AFTER INSERT ON profiles
BEGIN
    UPDATE sessions 
    SET last_activity = CURRENT_TIMESTAMP 
    WHERE user_name = NEW.name;
END;

-- Sample Views for Analytics

-- View: Recent Profiles
CREATE VIEW IF NOT EXISTS recent_profiles AS
SELECT 
    id,
    name,
    emotion,
    sentiment_score,
    created_at
FROM profiles
ORDER BY created_at DESC
LIMIT 10;

-- View: Emotion Distribution
CREATE VIEW IF NOT EXISTS emotion_distribution AS
SELECT 
    emotion,
    COUNT(*) as count,
    ROUND(AVG(sentiment_score), 2) as avg_sentiment
FROM profiles
GROUP BY emotion
ORDER BY count DESC;

-- View: Top Traits
CREATE VIEW IF NOT EXISTS top_traits AS
SELECT 
    name,
    personality_traits,
    sentiment_score
FROM profiles
ORDER BY created_at DESC;