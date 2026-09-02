---
name: architecture-discovery
description: Reverse-engineer the actual architectural style, boundaries, and conventions of a Spring Boot codebase.
category: repository
tags: [architecture, discovery, spring-boot]
priority: CORE
version: 1.0
---

# Architecture Discovery

## Purpose
Determine how a codebase is actually architected — as opposed to how it might look at a glance —
so new work fits the real boundaries instead of a guessed or idealized structure.

## When to use
- Before adding a new module, service, or significant class to an unfamiliar codebase.
- Before proposing an architectural change or refactor.
- When a task requires knowing where business logic vs. infrastructure concerns belong.

## When NOT to use
- Already established for this repo earlier in the session and nothing structural has changed.
- Trivial, localized bug fixes that don't cross architectural boundaries.

## Inputs
- Output of `repository/repository-exploration.md`.
- Package/module layout, dependency graph between modules.

## Process
1. Identify the layering style in use: classic layered (controller/service/repository),
   package-by-feature, hexagonal/ports-and-adapters, or modular monolith with explicit module
   boundaries. Infer from actual package structure and import directions, not naming alone.
2. Trace dependency direction for a few representative flows: does domain/business logic depend
   on infrastructure (JPA, HTTP clients), or is it the other way around? This tells you whether
   the codebase actually follows hexagonal/clean architecture or just uses the vocabulary.
3. Identify where cross-cutting concerns live (validation, error handling, security, logging) —
   centralized (e.g. `@ControllerAdvice`) or scattered.
4. For AI-integrated codebases, identify how model/provider access is isolated: is it behind a
   port/interface, or called directly from business logic? This matters for testability and
   provider swaps.
5. Note deviations and inconsistencies rather than picking one file as "the pattern" — real
   codebases are inconsistent; state what's dominant vs. what's an outlier.
6. Decide: does new work fit the dominant pattern (default), or does it need
   `decision-making/architecture-decision-making.md` because the dominant pattern doesn't fit?

## Rules
- Never impose a "better" architecture uninvited — match what exists unless asked to change it.
- Treat inferred boundaries as hypotheses; verify with a second example flow before committing.

## Anti-patterns
- Assuming hexagonal architecture because a `domain` package exists, without checking dependency
  direction.
- Introducing a new architectural style for one feature while the rest of the codebase uses another.

## Validation
- You can describe the dependency direction with a concrete example (file A depends on interface
  B, implemented by C in an outer layer).
- You can state where a new piece of logic should live and why, referencing existing examples.

## Related skills
`repository/repository-exploration.md`, `architecture/clean-hexagonal-architecture.md`,
`architecture/domain-driven-design.md`, `decision-making/architecture-decision-making.md`
