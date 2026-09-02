---
name: external-api-clients-resilience
description: Design resilient HTTP clients (WebClient/RestClient) for external and LLM provider APIs.
category: integrations
tags: [http-client, resilience, webclient, restclient]
priority: CORE
version: 1.0
---

# External API Clients and Resilience

## Purpose
Call external services (REST APIs, LLM providers) in a way that survives transient failures,
degrades predictably, and doesn't cascade a downstream outage into your own service.

## When to use
- Integrating any external HTTP dependency, including LLM provider SDKs that wrap HTTP under the
  hood.
- Diagnosing timeouts, connection pool exhaustion, or cascading failures involving an external call.

## When NOT to use
- Purely internal, in-process calls — resilience patterns here are about crossing a process/
  network boundary.

## Inputs
- Existing HTTP client conventions (`WebClient`, `RestClient`, `RestTemplate` — note
  `RestTemplate` is legacy; prefer `RestClient`/`WebClient` for new code).
- The external dependency's documented rate limits, timeout behavior, and error semantics.

## Process
1. Set explicit connect and read/response timeouts on every client — never rely on defaults,
   which are often unbounded or too generous for a request-serving thread.
2. Configure a bounded connection pool sized to expected concurrency, not left unbounded.
3. Add retries only for idempotent operations and only for transient failure classes (timeouts,
   5xx, connection resets) — never blindly retry a 4xx or a non-idempotent write.
4. Use exponential backoff with jitter for retries, capped at a small number of attempts.
5. Wrap calls with a circuit breaker (see `reliability/resilience-and-fault-tolerance.md`) when
   the dependency is critical-path and failures are expected to cluster (provider outage).
6. For LLM provider clients specifically: rate limits and token-based throttling are normal
   operating conditions, not exceptional errors — handle `429`s with backoff, and make timeouts
   generous enough for realistic generation latency but still bounded.
7. Isolate the external client behind an interface (see
   `architecture/clean-hexagonal-architecture.md`) so it can be mocked in tests and swapped.

## Rules
- Every outbound call has an explicit timeout — no exceptions.
- Retries are bounded and only for idempotent, transient-failure cases.
- Don't let a single slow dependency exhaust the thread pool serving unrelated requests —
  isolate with bulkheads/dedicated pools if the dependency is high-volume or unreliable.

## Anti-patterns
- Default/unbounded timeouts "because it usually responds fast."
- Retrying a `POST` that isn't idempotent, causing duplicate side effects.
- Catching and logging an external call failure without any resilience strategy, letting it
  silently degrade the caller.

## Validation
- A simulated slow/failing dependency (e.g. via a test double or fault injection) doesn't hang
  or crash the caller — verify with a test, not inspection alone.
- Timeout, retry, and circuit-breaker config values are visible in configuration, not buried
  magic numbers.

## Related skills
`reliability/resilience-and-fault-tolerance.md`, `ai/llm/llm-integration-fundamentals.md`,
`architecture/clean-hexagonal-architecture.md`
