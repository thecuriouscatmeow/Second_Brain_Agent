## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- After modifying code files in this session, run `graphify update .` to keep the graph current (AST-only, no API cost)

## saahilbasak

### Session Start
Read: docs/STATUS.md (always)
Read: graphify-out/GRAPH_REPORT.md quick index (always, if exists)
If Graphify installed: `graphify hook status` — note stale, don't block work
If Graphify not installed: continue normally, read GRAPH_REPORT.md as static reference

### Before Touching Existing Code
If Graphify available:
  1. `graphify explain "ModuleName"` (--budget 600)
  2. `graphify path "A" "B"` if impact unclear
  3. `graphify query "what uses X?" --budget 800` for broader context
If Graphify unavailable:
  Read GRAPH_REPORT.md named section for that module. If absent, read source file directly.

### Truth Order
Code/tests > Git > Graphify graph > Docs > Memory summaries
Docs conflict with code → fix docs

### Approval Tiers
AUTO: doc sync, graph refresh, comment edits, CHANGELOG rotation, test-only
SINGLE GATE: bug fix, milestone completion, small feature done
MULTI-GATE: schema migration, auth/security/payment, architecture, new roadmap phase

### Escalation (auto-promote small → medium)
>3 files | HIGH_RISK module (auth/payment/schema/security/db-migration)
| test fails twice | LOW/STALE graph confidence on a needed dependency

### Milestone Hook (fires per milestone, never per micro-step)
1. Run test command → show full output
2. Only if tests PASS: output "✓ Milestone N complete — [what] [files] | Tests: [N]/[N]"
3. Ask: "Commit and continue? (y/n)" — WAIT
4. On Y: git commit → sync hook
If tests FAIL: stop, show failures, do not ask for approval

### Session End
/saahilbasak-sync before ending any session with dev work
