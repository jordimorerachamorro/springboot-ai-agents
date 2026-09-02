---
name: clean-hexagonal-architecture
description: Apply and evaluate ports-and-adapters / clean architecture boundaries in a Spring Boot service.
category: architecture
tags: [architecture, hexagonal, clean-architecture, ports-and-adapters]
priority: HIGH
version: 1.0
---

# Clean / Hexagonal Architecture

## Purpose
Keep business logic independent of frameworks, databases, and external providers (including LLM
providers) so it can be tested and evolved without dragging infrastructure along.

## When to use
- Designing a new module/service where domain logic should be provider/framework-independent.
- The codebase already uses ports-and-adapters and new code needs to fit that boundary.
- Business logic needs to call an LLM, database, or external API, and you want that call
  swappable/mockable.

## When NOT to use
- Small CRUD services or internal tools where the indirection cost outweighs the benefit — a
  thin, well-tested layered service is often the right call. Don't impose hexagonal architecture
  on a codebase that isn't already moving that direction, without an explicit decision to do so
  (see `decision-making/architecture-decision-making.md`).

## Inputs
- Output of `repository/architecture-discovery.md` for the current codebase's existing pattern.

## Process
1. Define the domain model and use cases independent of Spring, JPA annotations, and any AI SDK.
2. Define ports (interfaces) for anything the domain needs from the outside world: persistence,
   messaging, external APIs, LLM calls. The domain depends on the port, never the adapter.
3. Implement adapters in an outer layer: JPA repositories, HTTP clients, an
   `LlmClient`/`ChatModel` adapter wrapping a specific provider's SDK.
4. Wire adapters to ports via Spring DI at the composition edge (configuration classes), keeping
   the domain package free of `@Autowired`/framework imports where practical.
5. For AI use cases specifically: define the port in terms of the business operation (e.g.
   `SummarizeDocument(text) -> Summary`), not in terms of the SDK's method signature — this is
   what makes provider swaps and mocking in tests possible.

## Rules
- Dependency direction is always inward: adapters depend on ports/domain, never the reverse.
- Don't leak infrastructure types (JPA entities, provider-specific response objects) across the
  port boundary — map to domain types at the adapter.
- Only introduce this pattern where the domain logic is non-trivial enough to benefit; don't
  wrap a single pass-through call in three layers of indirection.

## Anti-patterns
- "Anemic hexagonal": ports and adapters exist but the domain package still imports
  `jakarta.persistence` or a vendor SDK directly.
- Over-abstracting a port that only ever has one implementation and no realistic second one —
  weigh against `ai/llm/llm-integration-fundamentals.md`'s guidance on when provider abstraction
  earns its cost.

## Validation
- Domain/use-case code compiles without framework or SDK imports.
- A port has at least one alternate implementation (or a clear, stated reason to expect one soon,
  e.g. a planned provider swap) — otherwise reconsider whether the abstraction is warranted.

## Related skills
`repository/architecture-discovery.md`, `architecture/domain-driven-design.md`,
`ai/llm/llm-integration-fundamentals.md`, `decision-making/architecture-decision-making.md`
