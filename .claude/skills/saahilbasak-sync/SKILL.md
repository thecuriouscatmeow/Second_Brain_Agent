---
name: saahilbasak-sync
version: 1.0.0
description: Session sync for saahilbasak DocOps — updates CHANGELOG, STATUS.md, ROADMAP, and decisions. Three modes: quick (after milestones), full (session end), prune (monthly).
user_invocable: true
arguments: "[--full | --prune]"
---

# saahilbasak-sync

Session documentation sync. Runs as a **Haiku subagent**. Git-first — derives all facts from commits, not memory.

## Usage

```bash
/saahilbasak-sync           # quick (default) — run after every milestone
/saahilbasak-sync --full    # full — run at session end
/saahilbasak-sync --prune   # monthly maintenance
```

---

## Quick Mode (default, 30–60s)

Run after every milestone commit.

```
1. git diff HEAD~1 --name-only
2. git log --oneline -3
3. Append one CHANGELOG entry per commit (format: [DATE] — <commit message> | <files changed>)
4. Update docs/STATUS.md:
   - Resume point: next pending task
   - Active issues: any known blockers
   - Sync footer: "Synced: {DATE} | Commit: {HASH}"
5. Done.
```

---

## Full Mode (2–3 min, session end)

All quick steps, plus:

```
5. Update docs/ROADMAP.md step statuses using 3-evidence check (see below)
6. Update decisions/INDEX.md:
   - Add entries for any new decisions made this session
   - Mark resolved questions (move from questions.md to a DEC file)
7. Check Graphify:
   - If installed: run `graphify hook status`
   - If GRAPH_REPORT.md is stale and hooks didn't auto-refresh: add note to STATUS.md
8. Update memory file (project-specific Claude memory, if present)
```

### Roadmap Completion — 3-Evidence Rule

A ROADMAP step is marked ✅ only when **ALL THREE** conditions are met:

| Evidence | How to check |
|----------|-------------|
| STATUS.md marks it complete (or subplan state = COMPLETE) | Read docs/STATUS.md |
| git log shows a commit corresponding to this step | Keyword match or step reference in commit message |
| Test evidence: passing test run in recent commits, OR a test file exists for the changed code | `git log --all --oneline -- tests/` or check test file presence |

If any evidence is missing:
- STATUS says done but no commit → flag: "claimed complete, no commit found"
- Commit exists but no test evidence → flag: "committed without test evidence"
- Both exist but STATUS still in-progress → auto-update STATUS to complete

---

## Prune Mode (monthly, 5–10 min)

All full steps, plus:

```
9.  Rotate CHANGELOG entries >3 months → archive/CHANGELOG_YYYY-QN.md
10. Move superseded decisions → archive/DECISIONS_archive.md
11. Flag DEC files not referenced in any plan in past 60 days (archive candidates)
12. List docs/decisions/questions.md entries >14 days old (flag for resolution)
13. Run saahilbasak-doc-doctor checks inline, show results
```

---

## Dispatch Instructions

When this skill is invoked, dispatch a **Haiku subagent** with:
- The mode (quick/full/prune) inferred from the argument
- The current working directory
- Instructions to run the git commands first, then update files based on their output
- No access to previous session context — derive everything from git and file contents

The subagent should produce a brief completion summary: files updated, CHANGELOG lines added, any flags raised.
