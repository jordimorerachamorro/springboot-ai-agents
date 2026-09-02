---
name: domain-driven-design
description: Model bounded contexts, aggregates, and domain language for a Spring Boot service.
category: architecture
tags: [architecture, ddd, domain-modeling]
priority: MEDIUM
version: 1.0
---

# Domain-Driven Design

## Purpose
Model the business domain explicitly enough that code vocabulary matches the language domain
experts use, and that consistency boundaries (aggregates) are enforced in code.

## When to use
- The domain has genuine complexity: multiple entities with invariants that must hold together,
  or a codebase already organized around bounded contexts.
- Introducing a new bounded context that shouldn't leak its internal model into others.

## When NOT to use
- Simple CRUD domains — DDD's ceremony (aggregates, value objects, repositories-per-aggregate)
  isn't worth it for a handful of straightforward entities. Use plain JPA entities and services.
- Don't apply DDD vocabulary as decoration over what is otherwise a transaction-script codebase.

## Inputs
- Domain glossary/ubiquitous language if documented; otherwise infer from entity and method names.
- Output of `architecture/clean-hexagonal-architecture.md` if the codebase separates domain from
  infrastructure.

## Process
1. Identify aggregates: clusters of entities/value objects that must be consistent together,
   with one aggregate root controlling access and enforcing invariants.
2. Keep aggregate boundaries aligned with actual transaction boundaries — an aggregate should be
   loadable/saveable in one transaction (see `persistence/transactions-and-locking.md`).
3. Use value objects for concepts with no identity (money, date ranges) instead of primitives —
   only where it clarifies intent, not universally.
4. Identify bounded contexts where the same term means different things (e.g. "Order" in
   fulfillment vs. billing) and keep their models separate, translating at the boundary.
5. Name classes, methods, and fields using the domain's actual vocabulary, not generic CRUD terms.

## Rules
- One aggregate root per transaction; cross-aggregate consistency is eventual, not immediate
  (coordinate via domain events, see `messaging/event-driven-architecture.md`).
- Don't let a repository return or accept entities that aren't aggregate roots directly.

## Anti-patterns
- "Anemic domain model": entities with only getters/setters and all logic in service classes —
  fine for CRUD, a smell in a codebase claiming DDD.
- Modeling one giant aggregate that spans the whole domain — kills concurrency and clarity.

## Validation
- Each aggregate can state its invariant in one sentence, and the code enforces it (not just
  convention).
- Cross-context boundaries have an explicit translation/anti-corruption point.

## Related skills
`architecture/clean-hexagonal-architecture.md`, `persistence/transactions-and-locking.md`,
`messaging/event-driven-architecture.md`
