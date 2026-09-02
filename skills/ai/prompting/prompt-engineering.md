---
name: prompt-engineering
description: Design, structure, and version prompts as a maintained engineering artifact, not an inline string.
category: ai/prompting
tags: [prompting, prompt-engineering, system-prompts]
priority: CORE
version: 1.0
---

# Prompt Engineering

## Purpose
Treat prompts as versioned, testable engineering artifacts that shape model behavior reliably —
not throwaway strings tuned by trial and error with no way to detect regressions.

## When to use
- Designing or modifying any prompt (system prompt, task prompt, few-shot examples).
- A model's output quality is inconsistent or doesn't meet requirements.

## When NOT to use
- N/A within AI feature work — but don't over-engineer prompt infrastructure (templating,
  versioning systems) for a single, simple, stable prompt with no iteration history.

## Inputs
- The task's exact requirement (classification categories, extraction schema, tone/format
  constraints) and any existing prompt conventions in the codebase.

## Process
1. Separate system prompt (role, constraints, output format) from user/task content — don't
   concatenate everything into one blob; use the provider's dedicated system parameter.
2. State constraints explicitly and specifically: exact output format, what to do when
   information is missing/ambiguous, what NOT to do (avoid vague instructions like "be helpful").
3. Use few-shot examples when the desired output format or edge-case handling is hard to specify
   purely by instruction — but keep the example set small and representative, not exhaustive.
4. Externalize prompts as templates (resource files, `@Value`-loaded templates, or a Spring AI
   `PromptTemplate`) rather than hardcoded strings scattered through Java code, so they can be
   reviewed, versioned, and updated without a full redeploy if that matters for the use case.
5. Version prompts explicitly (even a simple comment/changelog) when they're consumed by
   structured-output parsing downstream — a prompt change can silently break the schema contract
   the parsing code assumes.
6. Prefer explicit structured-output instructions/schema over asking the model to reason about
   format in free text (see `ai/llm/structured-output.md`).
7. Keep prompts as short as reliably works — every token costs latency and money, and excessive
   instruction can dilute attention on what matters most (see
   `ai/cost/ai-cost-management.md`, `performance/llm-performance-optimization.md`).

## Rules
- System instructions live in the system prompt, not concatenated into user content.
- A prompt change that affects output shape requires re-validating the downstream
  structured-output parsing, not just "it looked fine in one manual test."
- Prompts handling user-supplied content must account for prompt injection (see
  `ai/security/ai-security.md`) — never let untrusted content carry instruction-level authority.

## Anti-patterns
- Giant, unfocused system prompts accumulating contradictory instructions over time with no cleanup.
- Prompt logic embedded as string concatenation deep inside business logic instead of a
  centralized, reviewable template.
- Tuning a prompt against one example and shipping without checking a broader, representative set.

## Validation
- Run the prompt against a small representative test set (see
  `ai/evaluation/llm-evaluation.md`) covering typical and edge cases, not just one manual check.
- Confirm the prompt change doesn't break downstream structured-output parsing.

## Related skills
`ai/llm/structured-output.md`, `ai/evaluation/llm-evaluation.md`, `ai/security/ai-security.md`,
`ai/cost/ai-cost-management.md`
