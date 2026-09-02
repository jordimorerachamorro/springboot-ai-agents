---
name: testcontainers-integration-testing
description: Write integration tests against real infrastructure (DB, message broker) using Testcontainers.
category: testing
tags: [testing, testcontainers, integration-testing]
priority: HIGH
version: 1.0
---

# Testcontainers Integration Testing

## Purpose
Verify behavior against real infrastructure (actual database engine, actual broker) instead of an
in-memory substitute that can silently diverge from production behavior.

## When to use
- Testing repository/query behavior, migrations, or messaging consumer/producer behavior where
  correctness depends on the real engine's semantics (locking, constraint enforcement, SQL
  dialect quirks).

## When NOT to use
- Don't reach for Testcontainers for logic that doesn't touch the infrastructure it spins up —
  use a unit or slice test instead; container startup cost isn't free.
- Don't use an in-memory DB substitute (e.g. H2 for a Postgres-targeting app) as a Testcontainers
  replacement — that reintroduces the exact divergence risk this skill exists to avoid.

## Inputs
- The real infrastructure technology and version used in production (match it in the container
  image, don't default to "latest" or an arbitrary version).

## Process
1. Spin up the same database/broker technology and a close-to-production version via
   Testcontainers, not an in-memory or lightweight substitute.
2. Scope container lifecycle appropriately — reused across a test class (or suite, via a shared
   static container / Spring context caching) to avoid the cost of a fresh container per test.
3. Let migrations (Flyway/Liquibase) run against the container the same way they run in
   production, rather than manually creating schema in the test.
4. Assert on real behavior differences that matter: constraint violations, actual locking
   behavior under concurrency, actual message delivery/ordering semantics.
5. Keep test data setup explicit and minimal per test — avoid a shared mutable fixture that makes
   tests order-dependent.

## Rules
- Container version should track the production dependency version, not drift independently.
- Tests must be able to run in CI without special host configuration beyond Docker availability.

## Anti-patterns
- Using H2 in "Postgres compatibility mode" to avoid the cost of a real Postgres container — the
  compatibility gaps are exactly where bugs hide.
- One giant shared container across the entire suite with tests that leak state into each other.

## Validation
- Tests pass against the real technology and fail if you deliberately break the assumption being
  tested (e.g. remove a constraint and confirm the test catches it).
- CI runs these tests successfully, not just locally.

## Related skills
`testing/spring-boot-testing-strategy.md`, `persistence/jpa-hibernate-patterns.md`,
`messaging/event-driven-architecture.md`
