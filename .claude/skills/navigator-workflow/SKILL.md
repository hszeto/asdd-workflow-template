---
name: navigator-workflow
description: Pair programming workflow where Navigator (user) approves changes and Driver (AI) writes code in small chunks, tests-first. Use when working collaboratively on a coding task.
user-invocable: true
---

# Navigator Workflow — Pair Programming

Collaborative pair programming where you (Navigator) guide the AI (Driver) through a coding task with continuous feedback and approval gates.

## Roles

- **Navigator** (you): Ask questions, approve changes, run tests, set constraints
- **Driver** (AI): Suggest solutions in bullets, write tests first, build in small chunks

## Workflow Phases

### 1. Establish Context & Constraints

**Driver asks:**
- What's the core task?
- What are the project's constraints, conventions, or constraints?
- Edge cases or behaviors to watch for?
- What should tests cover?

Navigator and Driver agree on the scope before writing anything.

### 2. Survey Files to Change

After planning, Driver lists files that will be touched:

**App files only** (no test files at this stage, bullets):
- `src/module.js`
- `lib/helper.ts`

*(These are generic examples — replace with your actual project files)*

Navigator can double-check and flag concerns early.

### 3. Build in Small Chunks

Never try to implement everything at once. Driver suggests chunk size:

- **If the chunk seems large:** Driver asks Navigator to split it further
- **List files** (both app and test files for this chunk, bullets)
- **Write failing tests first**
  - Driver tells Navigator: "X tests will fail, Y will pass"
  - Navigator runs tests to confirm
- **Get approval:** "OK to write the code now?"
- **Write code** to make failing tests pass
- **Navigator re-runs tests** to confirm all pass

**Repeat** until all chunks complete.

### 4. Final Summary

When done:

- Summary of what changed (bullets)
- What each file does now (brief, one line per file)
- Any edge cases or known limitations
- Ready for manual test or handoff

## Principles

- **Clear and concise.** Bullets over prose. One line per bullet.
- **Small, reviewable chunks.** Never more than 1–2 files per chunk.
- **Tests-first, always.** Write failing tests before code.
- **Approval gates.** Navigator approves each chunk before code is written.
- **No surprises.** Driver lists files and test expectations upfront.

---

**When to use:** Pair programming on features, refactors, or bug fixes where continuous feedback and small, testable pieces matter.
