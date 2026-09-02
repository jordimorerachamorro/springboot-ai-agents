---
name: transactions-and-locking
description: Scope transaction boundaries correctly and choose between optimistic and pessimistic locking.
category: persistence
tags: [transactions, locking, concurrency, jpa]
priority: HIGH
version: 1.0
---

# Transactions and Locking

## Purpose
Keep data consistent under concurrent access without over-serializing the system or holding locks
longer than necessary.

## When to use
- Any operation that reads-then-writes and must remain consistent under concurrent access.
- Diagnosing lost updates, deadlocks, or unexpected `OptimisticLockException`s.

## When NOT to use
- Single, atomic writes with no read-modify-write sequence generally don't need explicit locking
  beyond the database's own row-level guarantees.

## Inputs
- Existing `@Transactional` usage and isolation-level conventions in the codebase.
- Whether the entity in question already has a `@Version` field for optimistic locking.

## Process
1. Default to optimistic locking (`@Version`) for entities with low write contention — cheaper,
   no lock held, fails only on genuine conflict.
2. Use pessimistic locking (`SELECT ... FOR UPDATE` / `@Lock(PESSIMISTIC_WRITE)`) only under
   genuine high-contention read-modify-write scenarios (e.g. decrementing limited inventory)
   where retry-on-conflict from optimistic locking would thrash.
3. Keep `@Transactional` boundaries at the service layer, wrapping only the DB operations that
   must be atomic — never wrap an external HTTP/LLM call inside the same transaction as a DB write
   unless using a pattern that explicitly tolerates it (e.g. outbox).
4. Handle `OptimisticLockException` explicitly at the boundary that can meaningfully retry or
   inform the user — don't let it surface as a generic 500.
5. For cross-aggregate consistency (see `architecture/domain-driven-design.md`), prefer eventual
   consistency via domain events over widening a single transaction across aggregates.

## Rules
- Never hold a transaction open across a blocking network call.
- Choose isolation level deliberately when the default doesn't fit (e.g. read-committed causing
  phantom reads in a specific reporting query) — don't raise isolation globally to fix one query.
- Retry logic for optimistic lock conflicts belongs at the service layer with a bounded retry
  count, not an unbounded loop.

## Anti-patterns
- Wrapping an LLM or third-party API call inside `@Transactional` alongside DB writes.
- Defaulting to pessimistic locking everywhere "to be safe" — kills throughput.
- Catching and silently ignoring `OptimisticLockException`.

## Validation
- A concurrent-write test (two threads/transactions racing) behaves as expected — conflict
  detected and handled, not silently lost.
- Transaction spans are as small as functionally possible — confirm no external call sits inside one.

## Related skills
`persistence/jpa-hibernate-patterns.md`, `architecture/domain-driven-design.md`,
`messaging/event-driven-architecture.md`
