#!/usr/bin/env python3
"""
Sync Notion databases → SQLite.
Run after inspect_notion.py and fill in DATABASE_MAP with your actual IDs.
"""

import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from notion_client import Client

load_dotenv(Path(__file__).parent.parent / ".env")

ROOT = Path(__file__).parent.parent
DB_PATH = ROOT / "knowledge.db"

_token = os.environ.get("NOTION_TOKEN")
if not _token:
    raise SystemExit("ERROR: NOTION_TOKEN not set. Add it to your .env file.")

notion = Client(auth=_token)

# Fill in after running inspect_notion.py
# Format: "notion_database_id": "sqlite_table_name"
DATABASE_MAP = {
    # "abc123...": "knowledge_resources",
    # "def456...": "projects",
    # "ghi789...": "decisions",
    # "jkl012...": "experiments",
}


def sync_all():
    if not DATABASE_MAP:
        print("ERROR: DATABASE_MAP is empty.")
        print("Run scripts/inspect_notion.py first, then fill in DATABASE_MAP in this file.")
        return

    for notion_db_id, table_name in DATABASE_MAP.items():
        print(f"Syncing {notion_db_id} → {table_name}...")
        try:
            count = sync_database(notion_db_id, table_name)
            log_sync(table_name, count, "success")
            print(f"  Synced {count} records.")
        except Exception as e:
            log_sync(table_name, 0, "error", str(e))
            print(f"  ERROR: {e}")


def sync_database(notion_db_id: str, table_name: str) -> int:
    """Sync all pages from a Notion database into a SQLite table."""
    pages = []
    cursor = None

    while True:
        kwargs: dict = {"database_id": notion_db_id, "page_size": 100}
        if cursor:
            kwargs["start_cursor"] = cursor
        response = notion.databases.query(**kwargs)
        pages.extend(response["results"])
        if not response.get("has_more"):
            break
        cursor = response["next_cursor"]

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        for page in pages:
            row = map_page_to_row(page, table_name)
            if row:
                upsert_row(conn, table_name, row)
        conn.commit()

    return len(pages)


def map_page_to_row(page: dict, table_name: str) -> dict | None:
    """
    Map a Notion page to a SQLite row.

    TODO: After running inspect_notion.py, add table-specific mappings here.
    Each Notion database has different property names — the inspection report
    shows the exact names to use.

    Example for knowledge_resources (replace 'Name', 'URL', 'Tags' with your actual property names):

        if table_name == "knowledge_resources":
            props = page.get("properties", {})
            return {
                "id": str(uuid.uuid4()),
                "notion_id": page["id"],
                "title": _get_title(props.get("Name", {})),
                "url": props.get("URL", {}).get("url"),
                "tags": json.dumps([s["name"] for s in props.get("Tags", {}).get("multi_select", [])]),
                "created_at": page.get("created_time"),
                "updated_at": page.get("last_edited_time"),
            }
    """
    notion_id = page["id"]

    # Generic row — always populated regardless of table
    row = {
        "id": str(uuid.uuid4()),
        "notion_id": notion_id,
        "updated_at": page.get("last_edited_time"),
        "created_at": page.get("created_time"),
    }

    # Add table-specific property mappings here after reviewing the inspection report.
    # Remove the 'return row' line below once you've added real mappings.
    return row


def _get_title(prop: dict) -> str:
    """Extract plain text from a Notion title or rich_text property."""
    key = "title" if "title" in prop else "rich_text"
    return "".join(t.get("plain_text", "") for t in prop.get(key, []))


def upsert_row(conn: sqlite3.Connection, table: str, row: dict):
    """Insert or update a row, matching on notion_id."""
    # Build upsert: insert on conflict update all non-id fields
    cols = ", ".join(row.keys())
    placeholders = ", ".join("?" * len(row))
    updates = ", ".join(f"{k}=excluded.{k}" for k in row if k != "id")
    sql = f"""
        INSERT INTO {table} ({cols}) VALUES ({placeholders})
        ON CONFLICT(id) DO UPDATE SET {updates}
    """
    conn.execute(sql, list(row.values()))


def log_sync(table: str, count: int, status: str, error: str | None = None):
    """Record a sync event in sync_log."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute(
            "INSERT INTO sync_log (synced_at, table_name, records_synced, status, error) "
            "VALUES (?, ?, ?, ?, ?)",
            [datetime.now(timezone.utc).isoformat(), table, count, status, error],
        )
        conn.commit()


if __name__ == "__main__":
    sync_all()
