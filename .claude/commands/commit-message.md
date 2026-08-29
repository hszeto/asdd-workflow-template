---
description: Phase 7 of ASDD — generate a commit message, summary, and PR description from the current diff.
allowed-tools: Bash(git diff:*), Bash(git log:*)
---

# /commit-message

## Current repo status

- Staged: !`git diff --staged`
- Unstaged: !`git diff`
- Recent log: !`git log --oneline -10`

## Instructions

1. If there are no staged or unstaged changes, say so and stop.
2. Write a self-contained commit message (conventional-commit style:
   `type(scope): summary`) based on the diff above.
3. Finish with:
   - **Summary** — plain-language recap of what was built.
   - **PR description** — using the commit message as the title, with a short
     body covering what changed and why.

Do not run `git commit` or `git push` — only draft the message for the user to
review and use.
