# AI Spec Driven Development (ASDD) — Workflow Template

Canonical copy of my ASDD slash commands + skill. Install globally so every
project gets them, or copy `.claude/` into a single project's root when that
project needs its own variant (see below).

## What's in here

```
.claude/
├── commands/
│   ├── feature-spec.md      # Phase 0 + 1 — orient, then write a spec
│   ├── feature-plan.md      # Phase 2 — research, then write a plan
│   ├── feature-implement.md # Phases 3-6 — build it, one checkpoint at a time
│   └── commit-message.md    # Phase 7 — commit message, summary, PR description
└── skills/asdd/SKILL.md     # phase structure + principles, loaded automatically
```

## The workflow

1. `/feature-spec <requirement>` → writes `ai/feature-specs/<name>.md`, parking
   any genuine ambiguity in **Open Questions** rather than guessing at it.
   **Stop for approval.**
2. Answer the Open Questions — inline in the spec file, or in chat. The file is
   the better record; `/feature-plan` re-reads it either way.
3. `/feature-plan <name>` → promotes those answers to **Resolved Decisions** in
   the spec, then writes `ai/plans/<name>.md`. Refuses to plan on assumed
   answers. **Stop for approval.**
4. `/feature-implement <name>` → builds it **one checkpoint at a time**, stopping
   after each so you can commit before the next begins.
5. Self-verify — tests, lint, build must be green (or explicitly note what
   tooling doesn't exist).
6. Update changelog always; README/API docs if user- or API-facing.
7. Give manual test instructions.
8. `/commit-message` → commit message, summary, PR description.

Approval gates after steps 1 and 3 are non-negotiable. No implementation
starts without sign-off on both the spec and the plan.

**Git stays in your hands.** The workflow never creates, switches or deletes
branches and never commits — checkpoints are commit-sized units of work that get
handed to you with a message, not commits Claude runs. Before writing any code,
`/feature-implement` checks the branch: on `main` it stops and suggests a branch
name for you to create, and on a branch that looks unrelated to the plan it asks
first. `/commit-message` drafts; you commit.

## Where specs and plans live

Both commands write into an `ai/` directory at the project root:

```
ai/
├── feature-specs/<name>.md   # what and why, plus Open Questions → Resolved Decisions
└── plans/<name>.md           # how, files touched, checkpoints, test plan, risks
```

**Commit these.** They're the durable record of what was decided and why —
the part that survives a lost session and explains the diff six months later.
Don't gitignore them. Slugs match between the two directories, so a spec and
its plan always share a filename.

## Installing

### Option A — globally (recommended)

Copy into `~/.claude/`, and every project on the machine gets the workflow with
no per-project setup:

```bash
mkdir -p ~/.claude/commands ~/.claude/skills
cp .claude/commands/*.md ~/.claude/commands/
cp -r .claude/skills/asdd ~/.claude/skills/
```

A project-local `.claude/` still takes precedence, so a project that outgrows
the generic version can override it without disturbing anything else.

### Option B — per project

Copy `.claude/` into the project root instead. Use this when the project needs
a customized variant — multi-repo layouts being the main case.

## Setting up a new project

1. **Make sure the project has a `CLAUDE.md`.** Phase 0 (Orient) reads it, and
   the whole workflow is weaker without one. Run `/init` if it's missing.
2. Install per Option A or B above.
3. Tighten anything generic in `skills/asdd/SKILL.md` — if the project has real
   test/lint commands, name them explicitly in Self-Verify.
4. **Confirm what each verification command actually checks**, not what it looks
   like it checks. Bundler builds commonly strip types without checking them, so
   a green build is not a green typecheck. Write down which command covers what;
   a verification phase that quietly checks less than you think is worse than
   one you know is thin.
5. **If the project has more than one repo** (like fengshui-shifu's split
   API/UI), don't just copy this template as-is — it assumes a single repo.
   You'll need to add repo-targeting logic:
   - a "determine repo scope" step in `feature-spec.md` and `feature-plan.md`
   - `ai/feature-specs/` and `ai/plans/` living inside *each* repo, not at a
     shared top level
   - `commit-message.md` checking each repo independently via `git -C <repo>`
     instead of a bare `git diff`
   - See the fengshui-shifu project's `.claude/` for a worked multi-repo example.
6. Restart Claude Code and run `/help` to confirm `/feature-spec`,
   `/feature-plan`, `/feature-implement`, and `/commit-message` all appear.

## Naming gotchas (learned the hard way)

Behaviour notes are as of **August 2026** — re-test before trusting them on a
much newer Claude Code.

- **Don't name a command `/plan`** — it collided with a built-in. Use
  `/feature-plan` instead.
- **Skills auto-generate a matching slash command** from their folder name
  (`.claude/skills/asdd/` → `/asdd`). If the skill is meant as background
  reference material rather than something to run directly, set
  `user-invocable: false` in its frontmatter to keep it out of the `/` menu.
- **Slash commands only load from `.claude/commands/<name>.md`** — a file
  sitting directly in `.claude/` (not nested under `commands/`) won't be
  picked up at all.
- **Project `.claude/` doesn't inherit from parent directories.** If Claude Code
  is launched inside a subfolder, it reads that subfolder's `.claude/`, not one
  further up. Launch from wherever `.claude/` actually lives. This is separate
  from `~/.claude/`, which *does* apply everywhere — see Installing above.

## Maintenance

When the workflow itself improves (new phase, better template field, a sharper
principle), edit the files **here** first.

If you installed globally, re-run the copy commands in Option A and every
project picks up the change. If any projects hold local overrides, they've
forked deliberately — re-apply the improvement to each one by hand, and keep
the list short. Local copies are the ones that drift.
