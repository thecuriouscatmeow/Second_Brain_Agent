# Life OS — Personal Intelligence System

A local-first personal knowledge system that syncs your Notion workspace into a structured SQLite database. Use it as a second brain you fully own and query.

## What it does

- Inspects your Notion workspace and maps databases + properties
- Syncs Notion pages into a normalized 7-table SQLite schema
- Stores notes, tasks, journal entries, contacts, and media references
- Runs entirely on your machine — no cloud dependency beyond Notion's API

## Stack

- Python 3.10+
- SQLite (local, no server)
- [notion-client](https://github.com/ramnes/notion-sdk-py)
- python-dotenv

## Quick start

```bash
# 1. Clone and install
git clone https://github.com/thecuriouscatmeow/life-os-template.git
cd life-os-template
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Create your Notion integration
#    https://www.notion.so/profile/integrations → New integration → copy secret

# 3. Configure
cp .env.example .env
# Edit .env and set NOTION_TOKEN=secret_...

# 4. Share Notion databases with your integration
#    Open each Notion database → ⋯ → Connect to → your integration name

# 5. Inspect your workspace
python3 scripts/inspect_notion.py
# Review notion_structure_report.json

# 6. Map your databases
#    Edit scripts/notion_sync.py — fill in DATABASE_MAP and map_page_to_row()

# 7. First sync
python3 scripts/notion_sync.py
```

## Schema

Seven normalized tables: `notes`, `tasks`, `journal`, `contacts`, `media`, `tags`, `note_tags`.
See `schema.sql` for full DDL with indexes and FK enforcement.

## Project layout

```
schema.sql          — SQLite schema
scripts/
  setup_db.py       — creates knowledge.db from schema
  inspect_notion.py — maps your Notion workspace
  notion_sync.py    — syncs Notion → SQLite (configure DATABASE_MAP here)
docs/               — STATUS, ROADMAP, CHANGELOG (DocOps)
```

## Configuration

| Variable | Description |
|---|---|
| `NOTION_TOKEN` | Notion integration secret (`secret_...`) |

## Roadmap

See `docs/ROADMAP.md` for planned phases (search, AI embeddings, export).

## License

MIT
