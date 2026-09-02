---
name: resilience-and-fault-tolerance
description: Apply retries, timeouts, circuit breakers, and graceful degradation for dependency failures, including AI providers.
category: reliability
tags: [reliability, resilience, circuit-breaker, degradation]
priority: HIGH
version: 1.0
---

# Resilience and Fault Tolerance

## Purpose
Keep the service functioning — even if degraded — when a dependency (database, external API, LLM
provider) fails or slows down, instead of cascading into a full outage.

## When to use
- Any critical-path dependency on an external system, including LLM providers, which have their
  own outages, rate limits, and latency variance.
- Designing what should happen when a non-essential enhancement (e.g. an AI-generated summary)
  fails — should the whole request fail, or degrade gracefully?

## When NOT to use
- Purely internal, in-process logic with no network/external dependency.

## Inputs
- Which dependencies are critical-path (request fails without them) vs. enhancing (request can
  degrade without them).
- Existing resilience library in use (Resilience4j, Spring Retry, or none yet).

## Process
1. Classify each external dependency as critical or non-critical to the request. Non-critical
   dependencies (e.g. "also generate an AI summary") should fail open — return the core result
   without the enhancement — rather than failing the whole request.
2. Apply timeouts and bounded retries per `integrations/external-api-clients-resilience.md`.
3. Use a circuit breaker for dependencies prone to clustered failures (provider outages): after a
   failure threshold, stop calling for a cooldown period and fail fast instead of piling up slow
   failing calls.
4. Define an explicit fallback for each critical dependency's failure: cached/stale data, a
   simpler non-AI code path, or a clear error — never an undefined behavior that happens to be
   whatever the exception unwinding does.
5. For LLM-specific failures: a content-filter rejection, a context-length error, and a timeout
   are different failure classes needing different handling — don't collapse them into one
   generic "AI failed" fallback if the caller could act differently on each.
6. Use bulkheads (separate thread/connection pools) to stop one failing dependency from starving
   resources needed by unrelated request paths.

## Rules
- Every critical dependency has a defined, tested failure behavior — not "whatever exception
  propagation happens to do."
- Non-critical/enhancement calls degrade the response, they don't fail the request.
- Circuit breaker thresholds and fallback behavior are visible in config/code, not implicit.

## Anti-patterns
- A single AI enhancement call failing and taking down an otherwise-successful request.
- No circuit breaker on a dependency with a history of clustered outages, causing retry storms
  that worsen the outage.
- Fallback behavior that's actually just "return null and hope callers check."

## Validation
- Simulate the dependency failing (test double, fault injection) and confirm the defined fallback
  behavior actually triggers — not an unhandled exception.
- Non-critical dependency failure is verified not to fail the overall request.

## Related skills
`integrations/external-api-clients-resilience.md`, `api/validation-and-error-handling.md`,
`ai/llm/llm-integration-fundamentals.md`
