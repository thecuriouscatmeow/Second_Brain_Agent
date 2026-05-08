---
name: saahilbasak-plan
version: 1.0.0
description: Adaptive planning for saahilbasak DocOps — auto-classifies tasks as SMALL/MEDIUM/LARGE and executes the appropriate workflow with TDD, Graphify integration, and subagent dispatch.
user_invocable: true
---

# saahilbasak-plan

Adaptive planning skill. Auto-classifies the task, then executes the appropriate workflow. No sub-commands — just describe what you want to do.

---

## CLAUDE.md Section

When `/saahilbasak-init` runs, it appends this block to the project's CLAUDE.md (never overwrites `## graphify`):

```markdown
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
```

---

## Task Classification

Auto-classify before doing anything else. Default to SMALL unless signals indicate otherwise.

| Size | Signals |
|------|---------|
| **SMALL** | Single concern, ≤3 obvious files, no design question in request |
| **MEDIUM** | Multiple files, uncertainty present, or escalation trigger fires |
| **LARGE** | New feature / architecture / cross-cutting / explicit "brainstorm" request |

**Escalation triggers** (auto-promote SMALL → MEDIUM):
- >3 files touched
- HIGH_RISK module involved: auth, payment, schema, security, db-migration
- Test fails twice
- LOW or STALE graph confidence on a needed dependency

---

## Subagent Model Assignments

Every subagent dispatch uses the least capable model that can handle the task:

| Role | Model | Why |
|------|-------|-----|
| sync (file updates) | Haiku | Mechanical: git diff → write files |
| doctor (checks) | Haiku | Read-only: compare dates/hashes |
| plan: SMALL execution | Haiku | 1-2 files, clear spec |
| plan: MEDIUM implementer | Haiku → Sonnet if blocked | Multi-file but spec-driven |
| plan: LARGE implementer | Sonnet | Integration judgment |
| plan: spec reviewer | Sonnet | Compliance check |
| plan: code quality reviewer | Sonnet | Quality judgment |
| brainstorming / architecture | Sonnet (main context) | Design requires full reasoning |
| final code reviewer (post-LARGE) | Sonnet | Cross-task quality pass |

Haiku is sufficient for all documentation maintenance. Main context (Sonnet) handles planning and architecture only.

---

## SMALL Path (inline, no subagents)

```
1. If existing module: 
   - Graphify: `graphify explain "ModuleName"` (--budget 600)
   - Fallback: read GRAPH_REPORT.md section for that module
2. Mini-plan (4 steps max):
   - test: [what test to write]
   - fail: [why it should fail first]
   - fix: [exact change + file:line]
   - pass: [test command to run]
3. TDD IRON LAW: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
   - [ ] 1. Write failing test
   - [ ] 2. Verify test fails for correct reason (not typo/import error)
   - [ ] 3. Write minimal code to pass
   - [ ] 4. Run test command → show full output → confirm PASS
   - [ ] 5. Run full test suite → confirm no regressions
   - [ ] 6. Commit: `fix: [message]` or `feat: [message]`
4. Verification gate: show test output before claiming done
5. SINGLE GATE if non-trivial | AUTO if truly trivial
6. /saahilbasak-sync --quick
```

---

## MEDIUM Path (Haiku implementer per milestone)

```
1. Graph context:
   - Graphify: `graphify explain/query` for impacted modules (--budget 800)
   - Fallback: read GRAPH_REPORT.md sections for impacted modules
2. Check decisions/INDEX.md — find relevant DEC refs (quick scan, ≤5s)
3. Define acceptance criteria: "Done looks like: [1-3 measurable criteria]"
4. Create plan file (docs/plans/YYYY-MM-DD-{name}.md) only if:
   - Multi-session work, OR
   - ≥3 milestones
5. For each milestone:
   - Dispatch Haiku implementer subagent
   - Give: milestone text + acceptance criteria + relevant DEC refs
   - Subagent follows TDD (RED → GREEN → commit)
   - Verification gate: run test command, show output, confirm PASS
   - [SINGLE GATE] → git commit
   - /saahilbasak-sync --quick
6. /saahilbasak-sync --full at session end
```

---

## LARGE Path — Workflow A (Planning New Work)

```
IDEA
  ↓
Read: docs/STATUS.md + graphify-out/GRAPH_REPORT.md + decisions/INDEX.md
Graphify: `graphify query "what exists in this domain?" --budget 1000`
Fallback: read GRAPH_REPORT.md module sections if graphify unavailable
  ↓
ACCEPTANCE CRITERIA required: "Done looks like: [1-3 measurable criteria]"
  ↓
BRAINSTORMING: one question at a time → 2-3 approaches → design sections
  ↓
SPEC → docs/plans/YYYY-MM-DD-{name}-spec.md
  Spec self-review: placeholders? contradictions? scope creep? ambiguity?
  ↓ [MULTI-GATE: user approves spec]
ROADMAP updated (new steps integrated)
  ↓ [MULTI-GATE: user approves ROADMAP update]
SUBPLANS written (docs/plans/YYYY-MM-DD-{name}-sub-N.md)
  Each subplan: acceptance criteria + milestone list + rollback note
  State written to docs/STATUS.md
  ↓
GIT WORKTREE created [using-git-worktrees logic]:
  `git worktree add .worktrees/{feature-name} -b feature/{name}`
  Verify .worktrees in .gitignore
  Run baseline tests — confirm green before touching code
  ↓
→ enter Workflow C (subagent-driven execution, see below)
```

---

## LARGE Execution — Workflow C (Subagent-Driven)

```
SESSION_START
  ↓
REVALIDATE:
  Read docs/STATUS.md → identify active subplan + state
  If Graphify: `graphify hook status` — note stale
  If GRAPH_REPORT exists: check generated date vs HEAD
  Run baseline tests for active subplan area → confirm still green
  ↓
SUBPLAN_LOADED: read active subplan file
  Extract ALL milestones upfront with full text
  ↓
EXECUTE milestone by milestone:

  For each milestone:
    Dispatch implementer subagent (Haiku or Sonnet per complexity table above)
    Give: full milestone text + acceptance criteria + relevant DEC refs
    Do NOT give plan file path — give extracted milestone text directly
    Subagent follows TDD: RED → verify fail → GREEN → verify pass → REFACTOR → commit

    If subagent status:
      DONE → proceed to review
      DONE_WITH_CONCERNS → read concerns, decide before review
      NEEDS_CONTEXT → provide context, redispatch
      BLOCKED → assess: context? complexity? plan gap? escalate if plan is wrong

    Post-implementation (Sonnet):
      Quick spec check: does milestone output match acceptance criteria?
      If no → implementer fixes → re-check
      If yes → milestone complete

    VERIFICATION GATE (mandatory before milestone hook):
      Run full test command → show complete output
      Must see N/N passing before proceeding
      "Should pass" claims are NOT accepted

    Milestone hook → [SINGLE GATE] → git commit → graphify auto-rebuild
    /saahilbasak-sync --quick
    ↓ next milestone

  ↓ all milestones done
SUBPLAN_COMPLETE

  Final quality pass (Sonnet): scan all changed files across subplan
  → finishing-a-development-branch:
    Run full test suite
    Present 4 options: merge locally / push PR / keep branch / discard
    Wait for user choice → execute → cleanup worktree
  ↓
STATUS updated: next subplan IN_PROGRESS or PHASE_COMPLETE
/saahilbasak-sync --full
```

---

## Bug Fix Path — Workflow B

```
REPORT
  ↓
REPRODUCE [systematic-debugging: reproduce first]
  Write failing test. Run it. Confirm it fails for the right reason.
  If cannot reproduce: stop, investigate before touching code.
  ↓
LOCATE (no source file reading yet)
  If Graphify available:
    `graphify explain "FailingModule"` → dependencies + callers
    `graphify path "Source" "Symptom"` if needed
  If Graphify unavailable:
    Read GRAPH_REPORT.md section for that module
    Fall back to reading source file only if section absent
  Check decisions/INDEX.md for relevant DEC refs (quick scan, ≤5s)
  ↓
ESCALATION CHECK → promote if any trigger fires
  ↓
MINI-PLAN (inline):
  Graph context: [what graphify/GRAPH_REPORT returned]
  Decisions: (→ DEC-NNN) if relevant
  Files: [max 3, from graph output]

  TDD IRON LAW: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
  - [ ] 1. Failing test already written (done above)
  - [ ] 2. Verify test fails for correct reason (not typo/import error)
  - [ ] 3. fix: [exact change + file:line] — minimal code to pass
  - [ ] 4. Run: [test command] → show full output → confirm PASS
  - [ ] 5. Run: full test suite → confirm no regressions
  - [ ] 6. commit: `fix: [message] (→ DEC-NNN if relevant)`
  ↓
Verification gate: show test output before claiming done
[SINGLE GATE if non-trivial | AUTO if truly trivial]
  ↓
git commit → graphify hook fires (auto-rebuild if installed)
/saahilbasak-sync --quick
  ↓
DONE
```
