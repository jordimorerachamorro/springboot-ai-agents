---
name: ai-observability
description: Instrument LLM/agent calls with latency, token, and cost telemetry without logging sensitive prompt content.
category: observability
tags: [observability, ai, llm, tracing, cost]
priority: HIGH
version: 1.0
---

# AI Observability

## Purpose
Make AI-integrated behavior — model latency, token consumption, tool calls, retrieval steps —
visible enough to debug and cost-manage in production, while respecting that prompts/completions
often contain user data.

## When to use
- Any code path that calls an LLM, performs retrieval (RAG), or runs an agent loop with tool calls.
- Diagnosing unexpected latency, cost spikes, or quality regressions in an AI feature.

## When NOT to use
- Don't duplicate general tracing setup — this skill extends
  `observability/structured-logging-and-tracing.md` with AI-specific signals, not a replacement.

## Inputs
- Existing tracing/metrics stack (OpenTelemetry, Micrometer/Actuator).

## Process
1. Emit a span per LLM call (and per retrieval step, per tool call in an agent loop) with:
   model/provider identifier, prompt token count, completion token count, latency, and
   success/failure/error-class — not the raw prompt/completion content by default.
2. Track cost as a first-class metric derived from token counts and known per-model pricing, so
   spend is visible per feature/endpoint, not just in the provider's monthly bill (see
   `ai/cost/ai-cost-management.md`).
3. For RAG systems, trace retrieval separately from generation: what query was issued (or a hash/
   redacted form if sensitive), how many chunks retrieved, retrieval latency, and — ideally —
   which chunks were actually cited/used, to diagnose relevance problems.
4. For agents, trace each step of the loop (which tool was called, with what arguments-shape,
   how long it took, whether it succeeded) so a runaway or misbehaving loop is diagnosable, not a
   black box.
5. Only log/trace raw prompt or completion text behind an explicit, environment-scoped debug flag
   — never unconditionally in production — since prompts frequently contain user-supplied content.
6. Alert on anomalies: latency spikes (provider degradation), error-rate spikes (auth/rate-limit/
   content-filter issues), and cost spikes (runaway loops, unexpectedly large contexts).

## Rules
- Token counts, latency, and cost are always captured; raw prompt/completion content is captured
  only behind an explicit opt-in, scoped and time-limited.
- Every agent tool call is individually traceable — "the agent did something" is not sufficient
  observability.

## Anti-patterns
- No visibility into token/cost consumption until the provider invoice arrives.
- Logging full prompts/completions unconditionally, including any user PII they contain.
- Treating an agent loop as an opaque black box with only a final result logged.

## Validation
- A dashboard/log query can answer "how much did feature X spend on LLM calls this week" without
  guesswork.
- A single agent run's tool-call sequence can be reconstructed from traces after the fact.

## Related skills
`observability/structured-logging-and-tracing.md`, `ai/cost/ai-cost-management.md`,
`ai/agents/agent-architecture.md`, `ai/security/ai-security.md`
