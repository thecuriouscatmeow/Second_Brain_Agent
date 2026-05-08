# Open Questions

1. **Notion DB mapping** — Which Notion databases/properties map to which SQLite tables? (Resolved after running `inspect_notion.py` and reviewing `notion_structure_report.json`)
2. **Sync frequency** — Should `notion_sync.py` run manually or on a schedule?
3. **MCP integration** — Should `knowledge.db` be exposed to Claude Code via an MCP adapter in `ai-system/adapters/`?
