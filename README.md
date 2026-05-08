# Second Brain Agent — AI-Powered Note Taking for Your Personal Knowledge System

**Capture raw thoughts. Let AI extract what matters. Add clean, structured notes to your second brain.**

> Notes for humans in an AI age.

---

## What is a Second Brain Agent?

A **second brain** is a personal knowledge management system — a place to store ideas, insights, and information outside your head so you can think more clearly, create more freely, and remember what actually matters.

The problem: capturing notes is slow. Raw thoughts are messy. Most note-taking apps demand effort *at the moment you have the least time*.

**Second Brain Agent** solves this. You dump your raw thoughts — voice, text, a brain dump — and AI extracts the key points, structures them, and prepares them for your second brain. You review, approve, and move on. The heavy lifting is done.

This is **AI-assisted note taking** built around how humans actually think.

---

## Who this is for

- People building a **personal knowledge management (PKM)** system
- **Notion users** who want structured notes synced to a local database
- Anyone following **Building a Second Brain (BASB)**, Zettelkasten, or PARA method
- Developers who want a **self-hosted, local-first** alternative to AI note apps
- People who think out loud and struggle to turn thoughts into organised knowledge

---

## How it works

```
You → raw thought (voice note, brain dump, quick text)
         ↓
    AI extracts key points, tags, and context
         ↓
    You review the summary (seconds, not minutes)
         ↓
    Clean note syncs into your second brain (Notion → SQLite)
         ↓
    Your knowledge base grows — without the friction
```

### The core loop

1. **Capture** — dump a raw thought, idea, or note in any format
2. **Extract** — AI surfaces the key insight, strips the noise
3. **Review** — you see a clean summary before it enters your system
4. **Store** — structured note lands in your local SQLite knowledge base, synced from Notion

Human judgment stays in the loop. AI removes the grunt work.

---

## Features

- **AI key point extraction** — turns brain dumps into structured notes
- **Notion → SQLite sync** — your Notion workspace as a queryable local database
- **7-table knowledge schema** — notes, tasks, journal, contacts, media, tags (see `schema.sql`)
- **Local-first** — your data stays on your machine; no third-party cloud storage
- **Fast capture, slow thinking** — optimised for the moment of the idea, not the moment of organisation
- **Open and forkable** — MIT licensed, built to be customised to your workflow

---

## Quick start

```bash
# 1. Clone
git clone https://github.com/thecuriouscatmeow/Second_Brain_Agent.git
cd Second_Brain_Agent

# 2. Install
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Connect Notion
#    notion.so/profile/integrations → New integration → copy your secret
cp .env.example .env
# Set NOTION_TOKEN=secret_... in .env

# 4. Share your Notion databases with the integration
#    Open each database in Notion → ⋯ → Connect to → your integration

# 5. Inspect your workspace
python3 scripts/inspect_notion.py

# 6. Configure the sync
#    Edit scripts/notion_sync.py — add your database IDs to DATABASE_MAP

# 7. First sync
python3 scripts/notion_sync.py
```

Your Notion knowledge is now in a local SQLite database you can query, extend, and own.

---

## Knowledge schema

```
notes       — permanent notes and key insights
tasks       — actions and to-dos
journal     — daily notes, reflections, brain dumps
contacts    — people and relationship context
media       — books, articles, podcasts, references
tags        — shared tagging across all tables
note_tags   — many-to-many note ↔ tag links
```

Full DDL with indexes, constraints, and FK enforcement in `schema.sql`.

---

## Project layout

```
schema.sql              — SQLite schema
scripts/
  setup_db.py           — initialize knowledge.db
  inspect_notion.py     — map your Notion workspace structure
  notion_sync.py        — sync Notion pages → SQLite
docs/
  STATUS.md             — current phase and resume point
  ROADMAP.md            — planned features
  CHANGELOG.md          — release history
.env.example            — environment variable template
```

---

## Roadmap

- [ ] AI key point extraction on capture
- [ ] Voice note → structured note pipeline
- [ ] Semantic search across your knowledge base
- [ ] Daily digest: surface forgotten notes by relevance
- [ ] Obsidian and Logseq export

---

## Philosophy

Most AI note tools take your notes and make them live in another AI's cloud. This project does the opposite: AI helps *you* decide what's worth keeping, then stores it somewhere *you* own and control.

Your second brain should belong to you.

**Capture fast. Think slow. Own your knowledge.**

---

## Contributing

Issues and PRs welcome. If you've built a Notion→SQLite mapping for your own workspace, share it — the community benefits from real-world DATABASE_MAP examples.

---

## License

MIT — fork it, build on it, make it yours.

---

*Keywords: second brain, personal knowledge management, PKM, AI note taking, Notion SQLite sync, building a second brain, BASB, Zettelkasten, PARA method, local-first notes, AI productivity, note taking app, personal knowledge base, self-hosted PKM, AI second brain*
