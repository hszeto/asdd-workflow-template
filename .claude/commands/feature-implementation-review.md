---
description: Optional whole-feature review after /feature-implement — checks the branch diff against the spec, plan and contract, and writes findings to a review page for you to act on.
argument-hint: Feature name or plan md file
---

# /feature-implementation-review $ARGUMENTS

Optional. Not part of the required ASDD phases. Run it after `/feature-implement`
has finished checkpoints, on the whole feature rather than one checkpoint. This
command reviews and reports. It does not fix anything, create or switch branches,
or commit.

## 1. Locate the plan

`$ARGUMENTS` identifies the feature. Search `ai/plans/` for a matching plan, and
read it together with its spec in `ai/feature-specs/`.

- No plan → stop and tell the user to run `/feature-plan` first.
- No checkpoint ticked (`- [x]`) → stop and tell the user to run
  `/feature-implement` first.
- In a workspace folder, use the same `ai/` folder as the plan.

## 2. Gather the diff

Read git state only. Never create, switch, delete or commit branches.

- Current branch: `git branch --show-current`.
- Base branch: `main`, unless the plan names another. If no base exists, ask.
- Diff: `git diff <base>` (includes uncommitted work) and `git diff --stat <base>`.
- Empty diff → say so and stop.
- Very large diff → review it area by area, and list in **Not Covered** what you
  did not read.

## 3. Review

Run the review in a subagent on a higher-grade model: call the Agent tool with
`model: "opus"`. The main session keeps its own model, so there is nothing to
switch back.

The subagent starts with a fresh context. Its prompt must include only: the
branch diff, the spec, the plan, the contract (if the plan names one), and the
project's `CLAUDE.md`. Do not include the implementation discussion from this
chat. Ask it to return findings in the format in section 4, with file and line
for each.

Review the diff against the spec, the plan, the contract (if the plan names one),
and the project's `CLAUDE.md`. Check:

- **Plan trace:** each changed file belongs to a checkpoint's file list. Anything
  else is a finding.
- **Spec coverage:** each acceptance criterion has a test or a manual test step.
- **Contract:** code and contract agree on names, fields, and status codes.
- **Scope:** no unrelated refactors, renames, or speculative code.
- **Tests:** they assert behavior, not only that the code runs.

Judge from the artifacts only: the diff, the spec, the plan, and the contract.
Do not rely on the implementer's reasoning from the chat.

Rank each finding:
- **must fix** — wrong behavior, broken contract, or missing acceptance criterion
- **should fix** — risky, unclear, or outside the plan
- **nit** — style or small clarity issue

Every finding has a file, a line, what is wrong, and what would fix it.

## 4. Write the review

Write `ai/reviews/<name>.md` in this format:

```markdown
# Review: <name>

## Summary
- Branch <branch> against <base>: <N> files, <must> must fix, <should> should fix, <nit> nit

## Plan Trace
- <file> → checkpoint <n>
- <file> → not in plan

## Coverage
- <acceptance criterion> → <test or manual step>
- <acceptance criterion> → not covered

## Findings
- [must fix] <file>:<line> — <what is wrong and what would fix it>
- [should fix] <file>:<line> — <...>
- [nit] <file>:<line> — <...>

## Not Covered
- <area not read, or nothing>
```

Then open the review page, the same way `/feature-spec` and `/feature-plan` do.
`REVIEW` is the review script: `.claude/scripts/review.py` if this project has
it, otherwise `~/.claude/scripts/review.py`.

1. `python3 $REVIEW render ai/reviews/<name>.md`
2. `python3 $REVIEW serve ai/reviews/<name>.html --once`, in
   the background (`run_in_background`).

Each finding has an answer box. The user writes `fix` or `skip`, with a reason.

## 5. Hand off

Stop after the review page is open. Keep the chat reply short: the review path,
the URL, and the counts by severity. Do not paste the findings into chat.

When the review server exits, run `python3 $REVIEW apply
ai/reviews/<name>.md`. Then list the findings marked `fix` and ask whether to plan
them as a new checkpoint with `/feature-plan` or handle them another way. Do not
make the fixes here.
