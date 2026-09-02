---
name: structured-logging-and-tracing
description: Implement structured logging, correlation IDs, and distributed tracing in a Spring Boot service.
category: observability
tags: [observability, logging, tracing, opentelemetry]
priority: CORE
version: 1.0
---

# Structured Logging and Tracing

## Purpose
Make production behavior diagnosable after the fact — every request traceable end-to-end, every
log line searchable and correlated, without logging sensitive data.

## When to use
- Adding a new request-handling path, especially one involving external calls (DB, HTTP, LLM,
  messaging) where failures need to be traceable across boundaries.
- Investigating a production issue (paired with `debugging/bug-investigation.md`).

## When NOT to use
- Don't add logging to every internal method call — log at meaningful boundaries (request entry,
  external call, error), not everywhere.

## Inputs
- Existing logging framework/config (Logback/SLF4J conventions) and correlation ID propagation
  mechanism already in place (MDC, header-based).

## Process
1. Use structured (key-value/JSON) logging, not free-text string concatenation, so logs are
   queryable in aggregation tools.
2. Propagate a correlation/trace ID through the whole request path (MDC, and through any async
   boundary — message consumers, background jobs — where it doesn't propagate automatically).
3. Use distributed tracing (OpenTelemetry/Spring's tracing support) for cross-service and
   cross-external-call visibility — a trace should show a request's full path including any LLM
   call latency, not just this service's internal time.
4. Log at appropriate levels: `ERROR` for genuine failures needing attention, `WARN` for
   recoverable/degraded conditions, `INFO` for significant business events, `DEBUG` for
   diagnostic detail not needed in normal production operation.
5. Never log secrets, full request/response bodies containing PII, or — for AI features — raw
   prompts/completions containing user data without an explicit, deliberate privacy decision (see
   `observability/ai-observability.md` for what's safe to log about AI calls).
6. Include enough context in error logs to diagnose without reproducing: relevant IDs, the
   operation being attempted, the failure cause — not just a stack trace.

## Rules
- Every external call boundary logs enough to reconstruct what was attempted and what happened.
- No secrets or unredacted PII in logs, ever.
- Correlation ID present on every log line for a given request, including across async/messaging
  boundaries.

## Anti-patterns
- `e.printStackTrace()` or bare `System.out.println` instead of the logging framework.
- Logging entire request/response payloads indiscriminately.
- Losing correlation ID across an async boundary (e.g. a message consumer that doesn't propagate it).

## Validation
- A simulated failure produces a log entry sufficient to diagnose the cause without a debugger.
- Correlation ID is present and consistent across a multi-hop trace (including into a
  message consumer or LLM call, if applicable).

## Related skills
`observability/ai-observability.md`, `debugging/bug-investigation.md`,
`ai/security/ai-security.md`
