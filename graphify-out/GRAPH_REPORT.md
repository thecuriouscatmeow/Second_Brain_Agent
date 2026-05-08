# Graph Report - /Users/thecuriousbox/Life_OS/Notes  (2026-05-08)

## Corpus Check
- 3 files · ~1,686 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 19 nodes · 23 edges · 5 communities detected
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]

## God Nodes (most connected - your core abstractions)
1. `sync_database()` - 5 edges
2. `_extract_value()` - 4 edges
3. `inspect_workspace()` - 3 edges
4. `_get_title()` - 3 edges
5. `sync_all()` - 3 edges
6. `map_page_to_row()` - 3 edges
7. `upsert_row()` - 3 edges
8. `log_sync()` - 3 edges
9. `_get_title()` - 2 edges
10. `Extract a readable value from a Notion property.` - 1 edges

## Surprising Connections (you probably didn't know these)
- `sync_database()` --calls--> `upsert_row()`  [EXTRACTED]
  /Users/thecuriousbox/Life_OS/Notes/scripts/notion_sync.py → /Users/thecuriousbox/Life_OS/Notes/scripts/notion_sync.py  _Bridges community 0 → community 3_

## Communities

### Community 0 - "Community 0"
Cohesion: 0.36
Nodes (7): log_sync(), map_page_to_row(), Record a sync event in sync_log., Sync all pages from a Notion database into a SQLite table., Map a Notion page to a SQLite row.      TODO: After running inspect_notion.py, a, sync_all(), sync_database()

### Community 1 - "Community 1"
Cohesion: 0.7
Nodes (4): _extract_value(), _get_title(), inspect_workspace(), Extract a readable value from a Notion property.

### Community 2 - "Community 2"
Cohesion: 1.0
Nodes (2): _get_title(), Extract plain text from a Notion title or rich_text property.

### Community 3 - "Community 3"
Cohesion: 1.0
Nodes (2): Insert or update a row, matching on notion_id., upsert_row()

### Community 4 - "Community 4"
Cohesion: 1.0
Nodes (0): 

## Knowledge Gaps
- **6 isolated node(s):** `Extract a readable value from a Notion property.`, `Sync all pages from a Notion database into a SQLite table.`, `Map a Notion page to a SQLite row.      TODO: After running inspect_notion.py, a`, `Extract plain text from a Notion title or rich_text property.`, `Insert or update a row, matching on notion_id.` (+1 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 2`** (2 nodes): `_get_title()`, `Extract plain text from a Notion title or rich_text property.`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 3`** (2 nodes): `Insert or update a row, matching on notion_id.`, `upsert_row()`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.
- **Thin community `Community 4`** (2 nodes): `setup()`, `db_setup.py`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `sync_database()` connect `Community 0` to `Community 3`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Why does `_get_title()` connect `Community 2` to `Community 0`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **What connects `Extract a readable value from a Notion property.`, `Sync all pages from a Notion database into a SQLite table.`, `Map a Notion page to a SQLite row.      TODO: After running inspect_notion.py, a` to the rest of the system?**
  _6 weakly-connected nodes found - possible documentation gaps or missing edges._