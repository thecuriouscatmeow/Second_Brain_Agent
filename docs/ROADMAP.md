# Roadmap

## Phase 1 — Foundation (complete)
- ✅ SQLite schema: 7 tables (knowledge_resources, projects, tasks, decisions, experiments, frameworks, sync_log)
- ✅ `scripts/db_setup.py` — idempotent DB creation/migration
- ✅ `scripts/inspect_notion.py` — full Notion workspace reader with pagination
- ✅ `scripts/notion_sync.py` — Notion→SQLite upsert sync

## Phase 2 — Notion Integration Setup
- ⬜ Set up `.env` with NOTION_TOKEN
- ⬜ Share Notion databases with integration
- ⬜ Run inspection script, review `notion_structure_report.json`
- ⬜ Populate `DATABASE_MAP` and `map_page_to_row()` in `notion_sync.py`
- ⬜ Run first successful sync

## Phase 3 — Querying & Frameworks
- ⬜ Build query scripts to read from `knowledge.db`
- ⬜ Populate `frameworks/` with personal frameworks as markdown
- ⬜ Populate `ai-system/tools/` and `ai-system/adapters/`
- ⬜ Experiment tracking via `notes/experiments/`

## Future
- Automated sync on a schedule (cron or launchd)
- MCP adapter for Claude Code to query knowledge.db directly
- Personal dashboard reading from SQLite
