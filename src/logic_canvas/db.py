from __future__ import annotations

import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "logic_canvas.db"
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    with get_connection() as connection:
        _migrate_subject_column(connection)
        schema = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema)


def _migrate_subject_column(connection: sqlite3.Connection) -> None:
    table_exists = connection.execute(
        """
        SELECT 1
        FROM sqlite_master
        WHERE type = 'table' AND name = 'knowledge_items'
        """
    ).fetchone()
    if not table_exists:
        return

    columns = {
        row["name"] for row in connection.execute("PRAGMA table_info(knowledge_items)").fetchall()
    }
    if "subject" not in columns:
        connection.execute(
            """
            ALTER TABLE knowledge_items
            ADD COLUMN subject TEXT
            CHECK (subject IN ('sw_design', 'database', 'operating_system', 'network', 'security') OR subject IS NULL)
            """
        )
