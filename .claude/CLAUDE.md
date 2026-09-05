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

## 5. Lead With the Conclusion

**Say what something means before explaining how it works.**

- Open with the decision or finding in one sentence. Mechanics come after, or
  wait until asked.
- "The destination already has a `settings.json`, so it needs a merge, not a
  copy" — not a flag-by-flag tour of the merge command.
- Verdict before caveats: "yes, with one change", then the change.
- Having made a recommendation, don't re-survey the alternatives.
- When a command's real output answers the question faster than prose, run it
  and show the output.

Burying the point under implementation detail forces the reader to
reverse-engineer intent from syntax.
