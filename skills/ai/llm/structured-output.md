---
name: structured-output
description: Get reliable, validated structured/JSON output from an LLM instead of parsing free text.
category: ai/llm
tags: [llm, structured-output, json, validation]
priority: CORE
version: 1.0
---

# Structured Output

## Purpose
Turn LLM output into a typed, validated data structure your code can rely on — the single
highest-leverage practice for making AI features robust in production.

## When to use
- Any time an LLM's output feeds into business logic, persistence, another API call, or a tool
  execution — i.e. almost always, except free-form conversational text meant for direct display.

## When NOT to use
- Pure conversational/creative text meant for direct human reading with no downstream parsing.

## Inputs
- The exact schema needed downstream (fields, types, required vs. optional, allowed enum values).

## Process
1. Use the provider/SDK's native structured output mechanism (JSON schema-constrained generation,
   tool/function-calling with a schema) rather than instructing "respond in JSON" in the prompt
   and parsing the raw text — native mechanisms are far more reliable and avoid prose wrapping
   the JSON.
2. Define the schema as narrowly as the use case allows: required fields, constrained enums over
   free strings where a fixed set of values exists, explicit types.
3. Validate the parsed result against the schema in code before use — even with native structured
   output support, treat a schema violation as an expected failure mode, not an impossible case.
4. On validation failure, have a defined behavior: retry with a clarifying instruction, fall back
   to a default/degraded response, or surface an error — never silently proceed with partially
   invalid data.
5. Keep the schema stable and versioned if it's consumed by multiple call sites or persisted —
   schema drift between prompt version and consuming code is a common silent-failure source.
6. For nested/complex extraction, prefer decomposing into smaller, more reliable extractions over
   one large complex schema the model is more likely to get wrong.

## Rules
- Never parse LLM output with hand-rolled regex/string-splitting when a structured output
  mechanism is available.
- A structured-output call is not "done" until its result passes schema validation in code.
- Downstream code never assumes a field is present without either the schema marking it required
  and validation enforcing it, or explicit null-handling.

## Anti-patterns
- Prompting "return only valid JSON" and hoping, with no schema constraint or validation.
- Silently using a malformed/partial parse instead of treating it as a failure.
- A schema so loosely typed (everything a string) that it provides no real validation value.

## Validation
- Adversarial test fixtures (malformed JSON, missing fields, wrong types, extra prose around the
  JSON) are handled correctly — rejected or recovered, never silently corrupting downstream state
  (see `testing/llm-testing-strategies.md`).

## Related skills
`ai/llm/llm-integration-fundamentals.md`, `testing/llm-testing-strategies.md`,
`ai/agents/tool-design.md`, `ai/security/ai-security.md`
