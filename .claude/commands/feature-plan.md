---
description: Phase 2 of ASDD — research and write an implementation plan for an approved feature spec.
argument-hint: feature-spec md file
---

# /feature-plan $ARGUMENTS

Follow the `asdd` skill's phase structure. This command covers **Phase 2 (Plan)**
only. Do not begin implementation.

## 0. Check the spec review page was saved

Before anything else, check for an unsaved review:

- Run `ps -ax -o args= | grep -F "review.py serve" | grep -v grep`. If a line
  names `ai/feature-specs/<name>.html`, the review page is still waiting. Stop and
  tell the user: "Click Save on the spec review page first."
- If `ai/feature-specs/<name>.answers.json` exists, the answers haven't been
  applied. Stop and tell the user to run `apply` first.

## 1. Locate the approved spec

`$ARGUMENTS` is a feature name or note identifying which spec to plan for.
Search `ai/feature-specs/` for a matching file.

If no matching spec exists, stop and tell the user — do not plan from an
invented spec.

Before planning, re-read the spec's **Open Questions**. If any are unanswered —
in the file and in this conversation — stop and ask. Do not plan on assumed
answers.

Once answered, promote the section to **Resolved Decisions**: restate each as
the decision made, keeping the rationale, and confirm none remain open. Editing
the spec is the only write this command makes outside `ai/plans/`. If a spec has
no Open Questions section, or it is already resolved, proceed.

## 2. Research

Explore the actual code relevant to this feature (don't rely on memory of the
codebase). Confirm assumptions against `CLAUDE.md` if present, and check what
test/lint/build tooling actually exists in this project before assuming it.

## 3. Write the plan

Write to `ai/plans/<name>.md`, matching the spec's slug. In a workspace folder,
put the plan in the same `ai/` as its spec, and give each checkpoint its repo.

**Keep it scannable.** Bullets, not paragraphs. One line per bullet — if a
design decision needs more, state the decision in one line and the reason in
one more, then move on. No restating the spec. Omit any section that would be
empty.

Use this template:

```markdown
# Plan: <name>

## Confirmed Decisions
- <decision> — <one-line reason>
  <or: "none raised">

## Approach
- <key design decision, one line each — 3-6 bullets>

## Files Touched
- <path> — <what changes>

## Checkpoints
- [ ] 1. <one commit-sized unit of work> → verify: <the check that proves it done>
- [ ] 2. ...

Write every checkpoint unticked. `/feature-implement` ticks each one after the
user confirms its commit.

## Test Plan
- <specific test/case to add or run>
- <or: tooling that doesn't exist + what to verify manually instead>

## Risks / Rollback
- <risk> → <mitigation or how to undo>
```

## 4. Review page

Resolve `REVIEW` first: `.claude/scripts/review.py` if this project has it,
otherwise `~/.claude/scripts/review.py`. Then run these in Bash:

1. `python3 $REVIEW render ai/plans/<name>.md`
2. `python3 $REVIEW serve ai/plans/<name>.html --once`, in the background
   (`run_in_background`).

Do not write HTML yourself or publish an artifact. The page comes only from the
script.

Keep the chat reply short: the plan path, `http://127.0.0.1:8765/`, and any open
questions.

## 5. Stop

When the server exits, run `python3 $REVIEW apply ai/plans/<name>.md` and
summarize what changed. Do not begin implementation until the user
runs `/feature-implement`.
