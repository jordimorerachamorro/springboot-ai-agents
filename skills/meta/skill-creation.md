---
name: skill-creation
description: Author a new reusable skill for this library, or extend an existing one correctly.
category: meta
tags: [meta, skill-system, authoring]
priority: HIGH
version: 1.0
---

# Skill Creation

## Purpose
Keep the skill library coherent as it grows: every new skill should be a genuinely reusable
capability, not a project-specific instruction or a duplicate of existing coverage.

## When to use
- A recurring task keeps requiring the same non-obvious reasoning that no existing skill covers.
- A task revealed a gap explicitly called out in the README's documented backlog.

## When NOT to use
- The guidance is project-specific (a particular team's naming convention, a particular
  database's connection string) — that belongs in the project's own CLAUDE.md, not this library.
- An existing skill already covers this; extend it instead (see Process step 1).

## Inputs
- The recurring problem this skill would solve.
- Confirmation it's not company/project/domain/provider-specific (or, if provider-specific, that
  it belongs under `integrations/` or `ai/*` as an explicitly optional companion to a conceptual
  skill).

## Process
1. **Search first.** Check `skills/README.md`'s inventory table and the relevant category
   directory. If 70%+ overlap exists with a current skill, extend that file instead of forking.
2. Decide the category directory (see the tree in `skills/README.md`). If it doesn't fit any
   existing category, that itself is a signal to reconsider scope before adding a new directory.
3. Write the skill using the standard template (frontmatter + Purpose / When to use / When NOT to
   use / Inputs / Process / Rules / Patterns / Anti-patterns / Examples / Validation / Related
   skills — omit sections that don't apply, never omit When to use / When NOT to use / Validation).
4. Keep activation conditions narrow and concrete — "use when X, not when Y" — not "use for
   anything related to backend development."
5. Add the skill to the inventory table in `skills/README.md` with category, purpose,
   dependencies, and priority (CORE/HIGH/MEDIUM/OPTIONAL).
6. Link related skills bidirectionally where practical.
7. Run `meta/skill-review.md` before considering it done.

## Rules
- No skill should reference a specific company, product name, cloud account, or repository.
- Provider/technology-specific skills must have a corresponding conceptual skill they depend on
  (e.g. `integrations/anthropic-integration.md` depends on `ai/llm/llm-integration-fundamentals.md`).
- A skill must earn its own file: if it only differs from an existing skill by "use library X
  instead of Y," add a subsection to the existing skill instead of a new file, unless the
  X/Y distinction is itself a whole vendor SDK's worth of detail.

## Anti-patterns
- Micro-skills bound to a single code snippet (e.g. `create-controller.md`).
- Monolithic skills covering an entire discipline (e.g. one `spring-boot.md` for all of Spring).
- Skills whose "When to use" is broad enough to always match.

## Validation
- Would a skilled engineer recognize this as a distinct, nameable capability?
- Can you point to a real task where lacking this skill would have caused a worse outcome?
- Does the README inventory table stay accurate after this addition?

## Related skills
`meta/skill-discovery.md`, `meta/skill-review.md`
