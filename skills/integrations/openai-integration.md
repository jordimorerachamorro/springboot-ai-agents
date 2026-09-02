---
name: openai-integration
description: OpenAI-specific SDK integration details for Spring Boot, layered under the provider-agnostic LLM skill.
category: integrations
tags: [openai, llm, provider-specific]
priority: OPTIONAL
version: 1.0
---

# OpenAI Integration

## Purpose
Apply OpenAI-specific SDK/API details correctly once `ai/llm/llm-integration-fundamentals.md` has
established the general integration shape — this skill covers only what's specific to OpenAI.

## When to use
- The repository already depends on the OpenAI SDK (or Spring AI's OpenAI starter), or the user
  explicitly asks for OpenAI.

## When NOT to use
- No OpenAI dependency exists in the repo and the user hasn't named it — apply
  `ai/llm/llm-integration-fundamentals.md` and let provider choice be a deliberate decision (see
  `decision-making/architecture-decision-making.md`), not a default.
- Don't duplicate general LLM integration guidance here — only OpenAI-specific specifics belong
  in this file.

## Inputs
- Whether integrating via Spring AI's OpenAI starter or the OpenAI Java SDK directly.
- Model family in use (chat completions vs. responses API) — API shape differs between them.

## Process
1. Configure API key and org/project ID via externalized config (see
   `spring/configuration-and-profiles.md`), never inline.
2. Set `max_tokens`/`max_completion_tokens` explicitly — an unbounded generation is both a cost
   and latency risk.
3. Use the structured output / JSON schema response format features (function-calling-based or
   native structured output) rather than asking the model to "return JSON" in the prompt and
   parsing hopefully — see `ai/llm/structured-output.md`.
4. Handle OpenAI-specific error codes: `429` (rate limit — backoff), `400` with content-policy
   rejections (don't retry, surface distinctly), context-length-exceeded errors (truncate/chunk
   upstream, don't retry blindly).
5. Be deliberate about model choice per use case — cheaper/faster models for simple
   classification-style tasks, larger models reserved for tasks that need them (see
   `ai/cost/ai-cost-management.md`).

## Rules
- Never hardcode a model name where config is more appropriate for something likely to change.
- Content-policy and context-length errors are not transient — don't apply generic retry logic to
  them.

## Anti-patterns
- Parsing free-text model output for JSON instead of using structured output features.
- Silently swallowing content-filter rejections instead of surfacing them distinctly to the caller.

## Validation
- API key sourced from config/environment, not committed.
- Structured output calls are validated against the expected schema before use (see
  `ai/llm/structured-output.md`).

## Related skills
`ai/llm/llm-integration-fundamentals.md`, `ai/llm/structured-output.md`,
`integrations/anthropic-integration.md`, `ai/cost/ai-cost-management.md`
