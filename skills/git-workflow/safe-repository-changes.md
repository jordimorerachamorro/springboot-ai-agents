---
name: safe-repository-changes
description: Make minimal, reversible, well-scoped changes to an existing repository without destructive side effects.
category: git-workflow
tags: [git, safety, workflow]
priority: CORE
version: 1.0
---

# Safe Repository Changes

## Purpose
Change exactly what the task requires, in a way that's easy to review and easy to revert, without
risking uncommitted work or unrelated files.

## When to use
- Every task that modifies files in an existing repository.

## When NOT to use
- N/A — this applies to essentially every change; the judgment is in how much ceremony a given
  change warrants (a one-line fix needs less process than a multi-file feature).

## Inputs
- Current `git status`/`git diff` state before starting.

## Process
1. Check `git status` before starting — understand what's already modified/untracked so you don't
   conflate your changes with pre-existing work, and don't accidentally discard something.
2. Scope changes to what the task requires — resist opportunistic refactors, renames, or
   formatting sweeps in the same change unless asked. Unrelated changes make review harder and
   increase the chance of an unintended regression.
3. Prefer additive, reversible steps: rename/move rather than delete-and-recreate where behavior
   should be preserved; stash rather than discard when clearing space for an operation.
4. Never run destructive git operations (`reset --hard`, `checkout --`, `clean -f`, force-push)
   without explicit confirmation for that specific action — a prior approval doesn't cover a new,
   different destructive action.
5. Before staging, review what's actually included (`git status`/`git diff` after `git add`) —
   catch accidentally-included files, especially anything that might contain secrets.
6. Commit messages (when asked to commit) explain why, not just what — the diff already shows what.

## Rules
- Never discard uncommitted work without explicit confirmation.
- Never commit secrets — double-check file contents, not just filenames, before staging anything
  that looks credential-adjacent.
- Destructive operations require fresh, explicit confirmation each time, not blanket prior approval.

## Anti-patterns
- A "quick fix" that also reformats an entire file, obscuring the actual change in the diff.
- Force-pushing or hard-resetting to resolve a conflict instead of resolving it properly.
- Assuming a previously-granted permission for one destructive action extends to a different one.

## Validation
- `git diff` shows only the intended changes — no incidental formatting/unrelated edits.
- No secrets or unintended files are staged.

## Related skills
`repository/repository-exploration.md`, `quality/code-review.md`
