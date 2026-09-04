# AI Spec Driven Development (ASDD) — Workflow Template

Canonical copy of my ASDD slash commands + skill. Install globally so every
project gets them, or copy `.claude/` into a single project's root when that
project needs its own variant (see below).

## What's in here

```
.claude/
├── CLAUDE.md                # behavioral guidelines — how code gets written
├── settings.json            # PreToolUse hook — warns on edits to main/master
├── commands/
│   ├── feature-spec.md      # Phase 0 + 1 — orient, then write a spec
│   ├── feature-plan.md      # Phase 2 — research, then write a plan
│   ├── feature-implement.md # Phases 3-6 — build it, one checkpoint at a time
│   └── commit-message.md    # Phase 7 — commit message, summary, PR description
└── skills/asdd/SKILL.md     # phase structure + principles
```

Four layers, each answering a different question:

| Layer | Question | Loads |
| --- | --- | --- |
| `CLAUDE.md` | *How* should code be written? | every session |
| `SKILL.md` | *What order*, and which gates? | when a command runs |
| `commands/*.md` | What do I do *right now*? | when you type the command |
| `settings.json` | What fires *no matter what*? | registered at startup |

The first three are context — Claude reads them and follows them, but nothing
forces compliance. `settings.json` is the only deterministic layer: hooks run
as shell commands at fixed points regardless of what Claude decides. Today it
holds one `PreToolUse` hook on `Edit`/`Write`/`NotebookEdit` that checks the
current branch and warns when it's `main` or `master`. It **warns, it does not
block** — it exits 0 and injects a message. A backstop for the branch rule in
`SKILL.md`, not a replacement for it.

`.claude/CLAUDE.md` is a supported project memory location, equivalent to a
root `CLAUDE.md`. Keeping it inside `.claude/` means the whole payload is one
directory to copy.

`CLAUDE.md` is adapted from
[andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills),
with its "loop independently" guidance reworked — running ahead autonomously is
exactly what ASDD's per-checkpoint stop exists to prevent.

## What loads when

Two different sequences run, and conflating them is what makes the file layout
confusing.

**At session start** — broadest scope first, all concatenated, none overriding:

```
~/.claude/CLAUDE.md        (if installed globally)
  └─ ./CLAUDE.md and/or ./.claude/CLAUDE.md   ← behavioral rules, always in context
     └─ .claude/settings.json                 ← hooks registered, not read as text
        └─ skill + command descriptions       ← names only; bodies load on demand
```

Command and skill *bodies* are not in context at startup. Claude knows
`/feature-spec` exists; it doesn't know what's in it until you run it. That's
deliberate — it keeps startup context small.

**During a feature** — each command pulls in what it needs:

```
/feature-spec <req>   → loads SKILL.md + feature-spec.md
                      → reads CLAUDE.md context already in scope
                      → writes ai/feature-specs/<name>.md          ⏸ APPROVAL

  you answer Open Questions (in the file, or in chat)

/feature-plan <name>  → re-reads the spec, promotes answers to
                        Resolved Decisions, researches the code
                      → writes ai/plans/<name>.md                  ⏸ APPROVAL

/feature-implement    → checks the branch (hook also fires on first edit)
                      → checkpoint 1 → verify → report → ⏸ you commit
                      → checkpoint 2 → verify → report → ⏸ you commit
                      → ... then docs, changelog, manual test steps

/commit-message       → reads the diff, drafts message + PR description
                      → you run the commit
```

The ⏸ marks are where Claude stops and you act. There are only two kinds: the
two approval gates, and one per checkpoint for the commit.

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
cp .claude/CLAUDE.md ~/.claude/CLAUDE.md   # skip if you already have one — merge instead
```

`settings.json` is deliberately **not** copied globally. Hooks in
`~/.claude/settings.json` run in every project on the machine, including ones
where a `main`-branch warning is just noise. Copy it per project instead, into
that project's `.claude/settings.json`.

`~/.claude/CLAUDE.md` is global memory: it applies to every project on the
machine, ASDD-driven or not. If you already have one, merge rather than
overwrite.

A project-local `.claude/` still takes precedence, so a project that outgrows
the generic version can override it without disturbing anything else.

### Option B — per project

Copy `.claude/` into the project root instead. Use this when the project needs
a customized variant — multi-repo layouts being the main case.

```bash
cp -r .claude /path/to/project/
```

`CLAUDE.md` comes along inside `.claude/` and loads as-is — no extra step. If
the project already has a root `CLAUDE.md`, both load and are concatenated, so
merge them rather than keeping two sets of overlapping rules.

**Don't install both ways.** A global `~/.claude/CLAUDE.md` and a project copy
are both loaded and concatenated, not overridden — you'd get the same rules
twice. Pick one scope.

## Setting up a new project

1. **Run `/init` first, before copying anything in.** It generates a root
   `CLAUDE.md` describing the project's *facts* — build commands, architecture,
   conventions it discovered. Doing this on a clean tree avoids any question
   about how `/init` reacts to an existing `.claude/CLAUDE.md`.
2. **Install per Option A or B above.** You now have two CLAUDE.md files, and
   that's fine — see below.
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

## Verifying what actually loaded

`CLAUDE.md` has no trigger — it loads unconditionally at session start, before
you type anything. That makes it easy to *assume* it loaded when it didn't.

**Run `/context`.** Loaded files are listed under **Memory files**. If
`.claude/CLAUDE.md` appears there, it was processed. If it doesn't, Claude
can't see it. That's the whole check — no configuration needed.

In fullscreen mode the per-item breakdown is collapsed to keep the grid
visible, so use `/context all` there to see the file list.

Worth running once after installing, and once after a `/compact` in a long
session. The docs promise a *project-root* `CLAUDE.md` is re-read and
re-injected after compaction, but don't say whether `.claude/CLAUDE.md` gets
the same treatment. If it disappears from `/context` after a compact, move the
file to the project root — behavioral rules silently dropping out of long
sessions is the worst time to lose them.

## Two CLAUDE.md files is the intended state

After `/init` plus an install you'll have both `./CLAUDE.md` and
`./.claude/CLAUDE.md`. Nothing breaks. Both are project scope, and Claude Code
concatenates discovered memory files rather than overriding one with the other.
Run `/context` to confirm — loaded files appear under **Memory files**.

They carry different content on purpose:

| File | Contains | Owned by |
| --- | --- | --- |
| `./CLAUDE.md` | project facts — build commands, architecture, layout | the project |
| `./.claude/CLAUDE.md` | behavior — simplicity, surgical diffs, verifiable goals | this template |

**Don't merge them.** Merging looks tidier but destroys the ownership split:
`.claude/CLAUDE.md` is re-copyable whenever this template improves, while a
merged file makes every project a manual fork — the drift problem described
under Maintenance.

**Do watch for contradictions.** If two instructions conflict, Claude may pick
one arbitrarily. `/init` sometimes emits behavioral lines ("prefer X", "run
tests before committing") that overlap the template file. Skim its output once
and delete anything that restates or fights the behavioral rules.

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
  picked up at all. `CLAUDE.md` is the exception: `.claude/CLAUDE.md` and
  `./CLAUDE.md` are both valid project memory locations. Confirm with
  `/context` — loaded files show under **Memory files**.
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
