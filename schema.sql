-- Personal Intelligence System Schema

CREATE TABLE IF NOT EXISTS knowledge_resources (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT,
    content TEXT,
    summary TEXT,
    tags TEXT CHECK (tags IS NULL OR json_valid(tags)),           -- JSON array e.g. '["seo","research"]'
    notion_id TEXT UNIQUE,      -- Notion page ID for sync tracking
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    status TEXT CHECK (status IN ('active', 'completed', 'archived')),         -- 'active', 'completed', 'archived'
    description TEXT,
    notion_id TEXT UNIQUE,
    started_at TEXT,
    completed_at TEXT,
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    project_id TEXT REFERENCES projects(id),
    title TEXT NOT NULL,
    status TEXT CHECK (status IN ('todo', 'in_progress', 'done')),         -- 'todo', 'in_progress', 'done'
    priority TEXT CHECK (priority IN ('low', 'medium', 'high')),       -- 'low', 'medium', 'high'
    notion_id TEXT UNIQUE,
    due_date TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE TABLE IF NOT EXISTS decisions (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    context TEXT,        -- What problem prompted this
    decision TEXT,       -- What was decided
    outcome TEXT,        -- What happened
    lessons TEXT,        -- What to apply next time
    notion_id TEXT UNIQUE,
    decided_at TEXT,
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE TABLE IF NOT EXISTS experiments (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    hypothesis TEXT,
    method TEXT,
    results TEXT,
    conclusion TEXT,
    notion_id TEXT UNIQUE,
    started_at TEXT,
    completed_at TEXT,
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE TABLE IF NOT EXISTS frameworks (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    version TEXT DEFAULT '1.0',
    goal TEXT,
    content TEXT,        -- Full markdown content
    file_path TEXT,      -- Path to .md file
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    updated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE TABLE IF NOT EXISTS sync_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    synced_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    table_name TEXT NOT NULL,
    records_synced INTEGER DEFAULT 0,
    status TEXT NOT NULL CHECK (status IN ('success', 'error')),  -- 'success', 'error'
    error TEXT
);

-- Indexes for Notion sync lookups
CREATE INDEX IF NOT EXISTS idx_knowledge_resources_notion_id ON knowledge_resources(notion_id);
CREATE INDEX IF NOT EXISTS idx_projects_notion_id ON projects(notion_id);
CREATE INDEX IF NOT EXISTS idx_tasks_notion_id ON tasks(notion_id);
CREATE INDEX IF NOT EXISTS idx_decisions_notion_id ON decisions(notion_id);
CREATE INDEX IF NOT EXISTS idx_experiments_notion_id ON experiments(notion_id);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_tasks_project_id ON tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);
CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status);
