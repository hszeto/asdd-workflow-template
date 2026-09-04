# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. These govern *how*
code gets written; the `asdd` skill governs *what order* and *which gates*.
Merge with project-specific instructions as needed.

Adapted from https://github.com/multica-ai/andrej-karpathy-skills.

**Tradeoff:** these bias toward caution over speed. For trivial tasks, use
judgment — but ASDD's approval gates are not the trivial case, and are never
skipped.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

- State assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask: "would a senior engineer call this overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor what isn't broken.
- Match existing style, even if you'd do it differently.
- Notice unrelated dead code? Mention it — don't delete it.
- Remove imports/variables/functions that *your* changes orphaned. Leave
  pre-existing dead code alone unless asked.

The test: every changed line traces directly to the request.

## 4. Verifiable Goals

**Define success criteria before starting, not after.**

- "Add validation" → "write tests for invalid inputs, then make them pass"
- "Fix the bug" → "write a test that reproduces it, then make it pass"
- "Refactor X" → "ensure tests pass before and after"

Pair every step with its check: `<step> → verify: <check>`. Weak criteria
("make it work") force constant clarification; strong ones make "done"
unambiguous.

Strong criteria are **not** license to run ahead. Under ASDD, finish one
checkpoint, verify it, report it, and stop for the user to commit.
