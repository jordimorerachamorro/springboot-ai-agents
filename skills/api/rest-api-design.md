---
name: rest-api-design
description: Design REST resources, HTTP semantics, and versioning consistent with an existing Spring Boot API.
category: api
tags: [api, rest, http, spring-mvc]
priority: CORE
version: 1.0
---

# REST API Design

## Purpose
Design endpoints that follow correct HTTP semantics and match the existing API's conventions, so
consumers get a predictable, coherent surface rather than a patchwork of styles.

## When to use
- Adding a new endpoint or resource.
- Reviewing whether an existing endpoint's design (verbs, status codes, resource shape) is sound.

## When NOT to use
- Internal-only RPC-style calls that intentionally don't follow REST conventions (be explicit
  about this rather than applying REST rules to a non-REST endpoint).

## Inputs
- Existing controllers for naming, URL structure, and response envelope conventions.
- Whether the API is versioned, and how (`/v1/...`, header-based, none).

## Process
1. Model resources as nouns; use HTTP methods for actions (`GET` read, `POST` create,
   `PUT`/`PATCH` update, `DELETE` remove). Avoid verbs in URLs (`/createOrder`) unless the
   codebase already establishes an RPC-style convention.
2. Use correct status codes: `201` with `Location` header on create, `204` on delete with no
   body, `200` on successful read/update, `4xx` for client errors, `5xx` only for genuine server
   faults — never `200` with an error payload.
3. Design request/response DTOs separate from persistence entities — never expose JPA entities
   directly (see `persistence/jpa-hibernate-patterns.md`).
4. Support pagination for any collection endpoint that can grow unbounded; agree on
   limit/offset vs. cursor-based pagination with the existing API's convention.
5. For AI-backed endpoints (e.g. "summarize this document"), decide synchronous vs. streaming vs.
   async-with-polling based on expected latency — don't default to a long-blocking synchronous
   call for multi-second LLM operations without considering streaming (see
   `ai/llm/llm-integration-fundamentals.md`) or an async job pattern.
6. Version deliberately: only introduce a breaking change behind a new version; prefer additive,
   backwards-compatible changes to existing versions.

## Rules
- Never leak internal entity/persistence types through the API layer.
- Idempotent methods (`GET`, `PUT`, `DELETE`) must actually be idempotent in implementation.
- Every endpoint that can fail needs a defined error contract (see
  `api/validation-and-error-handling.md`).

## Anti-patterns
- Verb-based URLs mixed with resource-based URLs in the same API.
- Returning `200 OK` for business-logic failures instead of an appropriate `4xx`.
- Unbounded collection endpoints with no pagination.

## Validation
- New endpoint follows the same status-code and envelope conventions as neighboring endpoints.
- OpenAPI/Swagger spec (if present) reflects the change.

## Related skills
`api/validation-and-error-handling.md`, `persistence/jpa-hibernate-patterns.md`,
`ai/llm/llm-integration-fundamentals.md`, `security/api-security.md`
