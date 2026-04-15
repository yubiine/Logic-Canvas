CREATE TABLE IF NOT EXISTS knowledge_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL CHECK (category IN ('algorithm', 'pattern', 'cs')),
    subject TEXT CHECK (subject IN ('sw_design', 'database', 'operating_system', 'network', 'security') OR subject IS NULL),
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    code_snippet TEXT,
    code_language TEXT CHECK (code_language IN ('python', 'dart') OR code_language IS NULL),
    needs_review INTEGER NOT NULL DEFAULT 0 CHECK (needs_review IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_knowledge_items_category
    ON knowledge_items (category);

CREATE INDEX IF NOT EXISTS idx_knowledge_items_subject
    ON knowledge_items (subject);

CREATE INDEX IF NOT EXISTS idx_knowledge_items_needs_review
    ON knowledge_items (needs_review);

CREATE UNIQUE INDEX IF NOT EXISTS idx_knowledge_items_subject_title
    ON knowledge_items (subject, title);
