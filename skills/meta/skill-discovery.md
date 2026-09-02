---
name: skill-discovery
description: Determine which skill(s) from the library apply to the current task before acting.
category: meta
tags: [meta, skill-system, activation]
priority: CORE
version: 1.0
---

# Skill Discovery

## Purpose
Select the smallest set of skills that actually cover the task at hand, before writing any code
or making any changes.

## When to use
- At the start of any non-trivial task, before deciding an approach.
- When a task spans multiple concerns (e.g. "add an endpoint that summarizes a document with an
  LLM" touches API design, LLM integration, and testing).

## When NOT to use
- For single-line, unambiguous edits where no judgment call is required.
- Re-run per file edit — this is a task-level step, not a per-change step.

## Inputs
- The user's request, restated in your own words.
- The repository's actual stack (don't assume Spring AI, Kafka, a specific vector store, etc. —
  verify via `repository/repository-exploration.md` first if unknown).

## Process
1. Classify the task's primary domain(s): repository understanding, architecture, API,
   persistence, messaging, integrations, security, testing, observability, AI/LLM, etc.
2. Check the inventory table in `skills/README.md` for skills matching those domains.
3. For AI-related tasks, always check whether a conceptual skill (`ai/*`) is sufficient before
   pulling in a vendor-specific skill (`integrations/openai-integration.md`, etc.) — only add the
   vendor skill if the codebase already uses that vendor or the user named it.
4. Follow each candidate skill's "Related skills" section one hop to catch adjacent concerns
   (e.g. `rag-architecture` pulls in `ai-security` for RAG poisoning, `llm-evaluation` for
   retrieval metrics).
5. Discard skills whose "When NOT to use" matches the current situation.
6. State the short list of skills you're applying and why, so the choice is auditable.

## Rules
- Prefer fewer, well-matched skills over broad coverage "just in case."
- Never invent a skill's guidance from a name alone — read the file.
- If no skill matches, don't force one; use general engineering judgment and consider whether a
  new skill is warranted (see `meta/skill-creation.md`).

## Anti-patterns
- Loading every skill in a category "to be safe."
- Picking a skill by filename similarity without reading "When to use."

## Validation
- Every skill you end up applying should be traceable to a specific part of the task.
- If you finish a task and realize a skill you skipped was actually relevant, note it — that's a
  signal the skill's "When to use" section needs sharpening.

## Related skills
`meta/skill-creation.md`, `meta/skill-review.md`, `repository/repository-exploration.md`
