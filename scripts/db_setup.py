#!/usr/bin/env python3
"""Initialize or migrate knowledge.db from schema.sql."""

import sqlite3
from pathlib import Path

ROOT = Path(__file__).parent.parent
DB_PATH = ROOT / "knowledge.db"
SCHEMA_PATH = ROOT / "schema.sql"


def setup():
    schema = SCHEMA_PATH.read_text()
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(schema)
        conn.commit()
    print(f"Database ready: {DB_PATH}")

    # Verify tables were created
    with sqlite3.connect(DB_PATH) as conn:
        tables = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        ).fetchall()
    print("Tables:", [t[0] for t in tables])


if __name__ == "__main__":
    setup()
