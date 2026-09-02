---
name: llm-integration-fundamentals
description: Provider-agnostic principles for integrating an LLM into a Spring Boot application — the base skill for all AI features.
category: ai/llm
tags: [llm, ai, integration, spring-ai]
priority: CORE
version: 1.0
---

# LLM Integration Fundamentals

## Purpose
Establish how an LLM call fits into a Spring Boot application's architecture — as an untrusted,
fallible external dependency behind a clean boundary — independent of which provider or SDK is used.

## When to use
- Starting any feature that calls an LLM, before reaching for a specific provider or Spring AI.
- Deciding whether to use Spring AI, a direct provider SDK, or a thin custom client.

## When NOT to use
- Purely deterministic logic with no genuine need for a language model — don't reach for an LLM
  where a rule/lookup would be simpler, more reliable, and cheaper (a recurring temptation in
  GenAI-heavy codebases; resist it).

## Inputs
- The task's actual requirement: generation, classification, extraction, summarization,
  conversation, tool-using agent — this shapes model choice and integration pattern.
- Existing provider/SDK already in use in the repo, if any (verify, don't assume).

## Process
1. **Treat the LLM as an external dependency**, architecturally: behind a port/interface (see
   `architecture/clean-hexagonal-architecture.md`), with timeouts, retries, and fallback behavior
   (see `integrations/external-api-clients-resilience.md`,
   `reliability/resilience-and-fault-tolerance.md`) — not a special-cased call sprinkled through
   business logic.
2. **Treat LLM output as untrusted input.** Validate structured output against a schema (see
   `ai/llm/structured-output.md`) before using it in business logic, persistence, or as input to
   another system call. Never execute, render, or trust model output without validation.
3. Decide Spring AI vs. direct SDK vs. thin custom wrapper based on real need: Spring AI's value
   is in cross-cutting abstractions (advisors, portable `ChatClient` API, vector store
   abstraction) — worth it when you want provider portability or its ecosystem integrations. A
   thin direct-SDK wrapper is often simpler and more transparent for a single-provider, focused
   use case. Don't add Spring AI as a dependency purely out of habit if the app only ever needs
   one provider's specific features.
4. Choose the model deliberately per task (see `decision-making/architecture-decision-making.md`)
   — capability, latency, and cost differ substantially between model tiers; don't default to the
   largest/newest model for every call.
5. Set generation parameters (temperature, max tokens) deliberately based on the task: near-zero
   temperature for extraction/classification needing consistency, higher for creative generation.
6. Design for streaming vs. non-streaming based on the UX (see
   `performance/llm-performance-optimization.md`) — don't default to blocking synchronous calls
   for multi-second generations without considering it.
7. Only abstract across providers if there's a concrete reason to expect a provider swap or
   multi-provider routing — a single, well-isolated adapter behind a port is enough for most
   single-provider applications; a full provider-abstraction layer is extra cost, not automatic value.

## Rules
- LLM calls always have timeouts and defined failure behavior — never an unbounded, unhandled call.
- Structured output is validated before use, always.
- Business logic never depends on exact wording of model output — depend on structured fields or
  explicit classification results, not string matching on free text.
- API keys/credentials are externalized (see `spring/configuration-and-profiles.md`), never inline.

## Anti-patterns
- Calling the provider SDK directly from a controller or domain service with no port boundary.
- Parsing free-text model output with regex instead of using structured output features.
- Using an LLM for a task with a fully deterministic, reliable non-AI solution.
- Blindly trusting model output to be safe to log, render, or pass to another system unvalidated.

## Validation
- The LLM call is unit-testable via a mocked port (see `testing/llm-testing-strategies.md`).
- A simulated provider failure/timeout produces the defined fallback behavior, not an unhandled
  exception.

## Related skills
`architecture/clean-hexagonal-architecture.md`, `ai/llm/structured-output.md`,
`ai/prompting/prompt-engineering.md`, `integrations/external-api-clients-resilience.md`,
`ai/security/ai-security.md`, `decision-making/architecture-decision-making.md`
