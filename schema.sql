-- Personal Intelligence System Schema

CREATE TABLE IF NOT EXISTS knowledge_resources (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT,
    content TEXT,
    summary TEXT,
    tags TEXT,           -- JSON array e.g. '["seo","research"]'
    notion_id TEXT,      -- Notion page ID for sync tracking
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    status TEXT,         -- 'active', 'completed', 'archived'
    description TEXT,
    notion_id TEXT,
    started_at TEXT,
    completed_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    project_id TEXT REFERENCES projects(id),
    title TEXT NOT NULL,
    status TEXT,         -- 'todo', 'in_progress', 'done'
    priority TEXT,       -- 'low', 'medium', 'high'
    notion_id TEXT,
    due_date TEXT,
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS decisions (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    context TEXT,        -- What problem prompted this
    decision TEXT,       -- What was decided
    outcome TEXT,        -- What happened
    lessons TEXT,        -- What to apply next time
    notion_id TEXT,
    decided_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS experiments (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    hypothesis TEXT,
    method TEXT,
    results TEXT,
    conclusion TEXT,
    notion_id TEXT,
    started_at TEXT,
    completed_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS frameworks (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    version TEXT DEFAULT '1.0',
    goal TEXT,
    content TEXT,        -- Full markdown content
    file_path TEXT,      -- Path to .md file
    created_at TEXT,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS sync_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    synced_at TEXT NOT NULL,
    table_name TEXT NOT NULL,
    records_synced INTEGER DEFAULT 0,
    status TEXT NOT NULL,  -- 'success', 'error'
    error TEXT
);
