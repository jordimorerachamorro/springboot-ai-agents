---
name: anthropic-integration
description: Anthropic-specific SDK integration details for Spring Boot, layered under the provider-agnostic LLM skill.
category: integrations
tags: [anthropic, claude, llm, provider-specific]
priority: OPTIONAL
version: 1.0
---

# Anthropic Integration

## Purpose
Apply Anthropic (Claude)-specific SDK/API details correctly once
`ai/llm/llm-integration-fundamentals.md` has established the general integration shape.

## When to use
- The repository already depends on the Anthropic SDK (or Spring AI's Anthropic starter), or the
  user explicitly asks for Claude/Anthropic.

## When NOT to use
- No Anthropic dependency exists and the user hasn't named it — apply
  `ai/llm/llm-integration-fundamentals.md` first and treat provider choice as a deliberate
  decision, not a default.

## Inputs
- Whether integrating via Spring AI's Anthropic starter or the Anthropic Java SDK directly.
- Model identifier in use (verify current model IDs from the SDK/docs rather than assuming).

## Process
1. Configure the API key via externalized config, never inline (see
   `spring/configuration-and-profiles.md`).
2. Set `max_tokens` explicitly on every request — required by the API and a direct cost/latency
   control.
3. Use tool use (function calling) with a strict JSON schema for structured output needs rather
   than prompting for JSON and parsing hopefully — see `ai/llm/structured-output.md` and
   `ai/agents/tool-design.md` for schema design.
4. System prompts are a first-class, separate parameter — don't concatenate system instructions
   into the first user turn.
5. Handle rate limits (`429`) and overloaded (`529`) responses with backoff; these are expected
   operating conditions, not exceptional bugs.
6. For long documents/RAG context, be mindful of context window limits per model and use prompt
   caching where the SDK supports it to reduce repeated-context cost/latency on multi-turn or
   repeated-context calls.

## Rules
- Never hardcode a model version string where config is more appropriate.
- `max_tokens` must always be set deliberately, not left at an arbitrary default copied from an
  example.

## Anti-patterns
- Stuffing system instructions into the user message instead of the dedicated system parameter.
- Ignoring prompt caching opportunities on high-volume, repeated-context workloads, driving up
  cost unnecessarily.

## Validation
- API key sourced from config/environment, not committed.
- Tool-use/structured-output responses are validated against the expected schema before use.

## Related skills
`ai/llm/llm-integration-fundamentals.md`, `ai/llm/structured-output.md`,
`integrations/openai-integration.md`, `ai/cost/ai-cost-management.md`
