---
name: jpa-hibernate-patterns
description: Design entities, repositories, and fetch strategies correctly with JPA/Hibernate and Spring Data.
category: persistence
tags: [jpa, hibernate, spring-data, persistence]
priority: CORE
version: 1.0
---

# JPA / Hibernate Patterns

## Purpose
Design entities and queries that are correct, performant, and don't leak persistence concerns
into the API or domain layer.

## When to use
- Adding or modifying a JPA entity, repository, or query.
- Diagnosing N+1 queries, lazy-initialization exceptions, or unexpected query counts.

## When NOT to use
- Read-heavy, complex reporting queries better served by a native query, projection, or a
  separate read model than by forcing them through entity graphs.

## Inputs
- Existing entity relationships and fetch-type conventions in the codebase.
- Whether the codebase uses Spring Data derived queries, `@Query`, or a criteria/QueryDSL layer.

## Process
1. Default associations to `LAZY` fetch; use `EAGER` only with a specific, justified reason —
   `EAGER` is the most common source of accidental over-fetching.
2. When you know you'll need related entities, fetch them explicitly via `JOIN FETCH` or an entity
   graph rather than relying on lazy loading inside a loop (the classic N+1 pattern).
3. Never expose JPA entities directly through the API — map to DTOs (see
   `api/rest-api-design.md`). This also avoids `LazyInitializationException` outside the
   transaction/session.
4. Use `@Transactional` at the service layer, scoped to the smallest unit that needs atomicity —
   not on controllers, not spanning external calls (especially LLM calls, which can be slow and
   shouldn't hold a DB transaction open).
5. Use projections/DTO queries for read-only, large-result-set queries instead of loading full
   entity graphs.
6. Add indexes for columns used in `WHERE`/`JOIN`/`ORDER BY` on non-trivial tables; verify via
   `EXPLAIN` if performance is in question, don't guess.

## Rules
- Never call a lazy association's getter outside an active persistence context and expect it to
  work — either fetch eagerly for that use case or restructure the query.
- Don't hold a DB transaction open across a network call (HTTP, LLM API) — fetch/save separately.
- Bidirectional associations need a clearly designated owning side; don't let both sides manage
  the relationship independently.

## Anti-patterns
- `EAGER` fetch used as a blanket fix for `LazyInitializationException` instead of fixing the
  actual access pattern.
- Looping over a collection and triggering a query per iteration (N+1).
- Entities annotated with API serialization annotations (`@JsonProperty` etc.) instead of using DTOs.

## Validation
- Enable SQL logging (or Hibernate statistics) for the changed code path and confirm query count
  matches expectations — no surprise N+1.
- Integration test against a real database (see `testing/testcontainers-integration-testing.md`)
  covers the new query/entity behavior.

## Related skills
`persistence/transactions-and-locking.md`, `api/rest-api-design.md`,
`testing/testcontainers-integration-testing.md`
