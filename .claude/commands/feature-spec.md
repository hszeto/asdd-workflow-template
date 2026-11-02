---
description: Phase 0 + Phase 1 of ASDD — orient in the codebase, then write a feature spec for approval.
argument-hint: Feature description
---

# /feature-spec $ARGUMENTS

Follow the `asdd` skill's phase structure. This command covers **Phase 0 (Orient)**
and **Phase 1 (Feature Spec)** only. Do not proceed to planning or implementation.

## 1. Orient (Phase 0)

Read `CLAUDE.md` if it exists, plus the existing code relevant to this
requirement — don't assume patterns from memory; confirm them by reading the
actual files.

## 2. Write the feature spec (Phase 1)

Requirement: "$ARGUMENTS"

Write the spec to `ai/feature-specs/<name>.md`, where `<name>` is a short
kebab-case slug derived from the requirement.

**Choose the folder first.** If this folder holds other git repos (a workspace
rather than a single repo), ask which repo or repos the feature touches. One
repo: write to `<repo>/ai/feature-specs/`. Two or more: write to this folder's
`ai/feature-specs/` and name the repo for each checkpoint in the plan. A
single-repo folder always writes to its own `ai/`.

**Keep it scannable.** Bullets, not paragraphs. One line per bullet. A whole
spec should fit on one screen — if it doesn't, the feature is too big to spec
in one file. Omit any section that would be empty; don't pad it with filler.

Use this template:

```markdown
# Feature Spec: <name>

## Summary
<1-2 sentences: what this does and who it's for>

## Requirements
- <one line each, testable>

## Non-Goals
- <one line each>

## Edge Cases
- <case> → <expected behavior>

## Acceptance Criteria
- <one line each, checkable as done/not done>

## Approval
- [ ] Spec approved
```

If you have genuine ambiguity about requirements, put it in **Open Questions**
rather than guessing — do not invent acceptance criteria to fill the section.

## 3. Review page

Follow the **Review page** steps in the `asdd` skill: render the page, then start
the review server in the background. Keep the chat reply short: the spec path,
the review URL, and the Open Questions count. Do not paste the spec into chat.

## 4. Stop

Wait for the review server to finish. When it does, run the apply step from the
`asdd` skill, then summarize what changed and what is still open. Do not run
`/feature-plan` automatically — it runs only after **Spec approved** is ticked.
