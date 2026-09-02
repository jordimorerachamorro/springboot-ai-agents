---
name: skill-review
description: Validate a new or edited skill file before it's added to or updated in the library.
category: meta
tags: [meta, skill-system, quality]
priority: HIGH
version: 1.0
---

# Skill Review

## Purpose
Catch scope, duplication, and quality problems in a skill file before it becomes part of the
library other agents rely on.

## When to use
- Immediately after drafting or materially editing a skill file.
- When deprecating or merging skills, to confirm nothing downstream still depends on the old name.

## When NOT to use
- For reviewing application code — use `quality/code-review.md` instead.

## Inputs
- The draft or edited skill file.
- The current `skills/README.md` inventory table.

## Process
1. **Reusability check**: does the file avoid naming a specific company, project, database
   instance, or (outside `integrations/`/`ai/*` vendor skills) a specific LLM provider?
2. **Duplication check**: search the inventory table and category directory for >50% conceptual
   overlap with an existing skill.
3. **Granularity check**: is this a meaningful capability (not a one-line snippet, not an entire
   discipline)?
4. **Activation check**: are "When to use" and "When NOT to use" concrete enough that two
   different agents would make the same call on a given task?
5. **Completeness check**: are Purpose, When to use, When NOT to use, Process, Rules, and
   Validation present and non-generic?
6. **Dependency check**: do "Related skills" links point to files that actually exist, and does
   the dependency direction make sense (a conceptual skill shouldn't depend on a vendor skill)?
7. **Inventory sync check**: is the skill listed in `skills/README.md` with correct category,
   dependencies, and priority?

## Rules
- Reject (send back for revision) any skill that fails the reusability or duplication check.
- A skill without a Validation section is incomplete — validation is how the calling agent knows
  it applied the skill correctly.

## Validation
- All checks above pass.
- The skill reads as something a senior engineer would recognize and agree with, not a generic
  tutorial.

## Related skills
`meta/skill-creation.md`, `meta/skill-discovery.md`
