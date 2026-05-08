---
name: saahilbasak-doc-doctor
version: 1.0.0
description: Health checks for saahilbasak DocOps — validates STATUS sync, Graphify hooks, ROADMAP evidence, orphan plans, stale decisions, and DEC file integrity.
user_invocable: true
---

# saahilbasak-doc-doctor

Read-only health check for the saahilbasak DocOps system. Runs as a **Haiku subagent**. No writes. Short output. No ceremony.

---

## Checks (run all 7 in sequence)

| # | Check | Pass condition | Fail message |
|---|-------|---------------|--------------|
| 1 | STATUS.md sync footer date | Synced within 3 days | "STATUS stale: last synced N days ago" |
| 2 | Graphify hooks | If installed: `graphify hook status` exits 0. If not installed: always pass with note. | "Graphify hooks not installed — rebuild manually" |
| 3 | GRAPH_REPORT.md freshness | Generated date ≤ HEAD commit date (only if Graphify is installed) | "GRAPH_REPORT stale — run graphify . --update" |
| 4 | Orphan plan files | No docs/plans/ files >30 days with no matching ROADMAP step | "N orphan files: [list]" |
| 5 | Stale questions | No decisions/questions.md entries >14 days old | "N questions >14 days: [list titles]" |
| 6 | ROADMAP evidence | ✅ steps pass 3-evidence check (STATUS + commit + test) | "Step N marked ✅ — no test evidence found" |
| 7 | DEC file integrity | Every reference in decisions/INDEX.md has a corresponding DEC file | "N missing DEC files: [list]" |

---

## Output Format

```
✓ STATUS: synced 1 day ago
✗ GRAPH: Graphify hooks not installed — rebuild manually
✓ GRAPH_REPORT: current (matches HEAD)
✗ Plans: 2 orphan files: [2025-01-10-auth-spec.md, 2025-01-15-cache-sub-1.md]
✓ Questions: all < 14 days
✗ ROADMAP: Step 32 marked ✅ — no test evidence found
✓ Decisions: all DEC files present

3 issues. Run /saahilbasak-sync --full to fix STATUS + ROADMAP.
```

Rules:
- ✓ = passed, ✗ = failed
- List specific file names or step numbers for every failure
- End with issue count + suggested fix command
- If 0 issues: "All checks passed."

---

## Dispatch Instructions

When this skill is invoked, dispatch a **Haiku subagent** with:
- The current working directory
- Read-only access — no file writes
- Instructions to run each check sequentially and collect results
- Output exactly in the format above (no additional commentary)
