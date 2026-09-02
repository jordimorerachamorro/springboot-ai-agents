---
name: validation-and-error-handling
description: Validate requests and produce consistent, informative error responses across a Spring Boot API.
category: api
tags: [api, validation, error-handling, exceptions]
priority: CORE
version: 1.0
---

# Validation and Error Handling

## Purpose
Reject invalid input early with clear, consistent error responses, and ensure unexpected failures
don't leak internal details or produce inconsistent error shapes across endpoints.

## When to use
- Adding any endpoint that accepts input.
- Introducing a new failure mode (external call, DB constraint, LLM call) that needs to surface
  as a defined error response rather than an unhandled exception.

## When NOT to use
- Internal, non-boundary code shouldn't re-validate what's already validated at the API boundary
  (see Rules — validate at boundaries, trust internal code).

## Inputs
- Existing exception hierarchy and `@ControllerAdvice`/`@ExceptionHandler` setup.
- Existing error response shape (problem-detail/RFC 7807, custom envelope, etc.).

## Process
1. Validate request DTOs with Bean Validation (`@NotNull`, `@Size`, custom validators) at the
   controller boundary — don't hand-roll validation that the framework already provides.
2. Centralize exception-to-response mapping in a `@ControllerAdvice`/global exception handler
   rather than try/catch blocks scattered through controllers.
3. Map domain/business exceptions to appropriate HTTP status codes explicitly — don't let a
   generic `Exception` handler decide status codes for known failure types.
4. Never expose stack traces, internal class names, or raw exception messages from
   infrastructure (DB, LLM provider) in API responses — log the detail, return a sanitized message.
5. For LLM-backed endpoints: treat provider errors (rate limits, timeouts, content filtering) as
   distinct, expected failure modes with their own mapped responses — not generic 500s (see
   `reliability/resilience-and-fault-tolerance.md`).
6. Keep error response shape consistent across the whole API (same field names for
   code/message/details) so clients can handle errors generically.

## Rules
- Validate at system boundaries (controller input, external API responses); trust internal code
  and already-validated data — don't add defensive checks for states that can't occur.
- Never let raw exception messages containing sensitive data reach the client.
- One consistent error response shape for the whole API.

## Anti-patterns
- try/catch in every controller method instead of centralized exception handling.
- Returning `500` for client errors (bad input) or `400` for genuine server faults.
- Swallowing exceptions silently instead of mapping or rethrowing meaningfully.

## Validation
- A request with invalid input returns a `4xx` with a clear, structured error body — verify with
  an actual failing request, not just reading the code.
- No stack trace or internal detail appears in a response body.

## Related skills
`api/rest-api-design.md`, `reliability/resilience-and-fault-tolerance.md`,
`observability/structured-logging-and-tracing.md`
