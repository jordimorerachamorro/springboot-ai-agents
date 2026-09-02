---
name: spring-boot-testing-strategy
description: Choose the right test type (unit, slice, integration) and structure for Spring Boot code.
category: testing
tags: [testing, junit5, mockito, spring-boot-test]
priority: CORE
version: 1.0
---

# Spring Boot Testing Strategy

## Purpose
Test at the right level — most tests fast and isolated, fewer tests broad and realistic — so the
suite gives confidence without becoming slow or brittle.

## When to use
- Adding new behavior that needs test coverage.
- Reviewing whether existing tests actually exercise the change (see `quality/code-review.md`).

## When NOT to use
- Don't write a full Spring context integration test for logic with no framework dependency —
  a plain unit test is faster and just as valid.

## Inputs
- Existing test structure/conventions (JUnit 5, Mockito, AssertJ, test naming).
- Whether the change touches persistence, HTTP, messaging (favors slice/integration tests) or is
  pure logic (favors unit tests).

## Process
1. Default to plain JUnit 5 unit tests with Mockito for logic that doesn't need a Spring context —
   fastest feedback loop, most of the test pyramid should live here.
2. Use Spring slice tests (`@WebMvcTest`, `@DataJpaTest`) when testing framework integration
   (controller request mapping/validation, repository query behavior) without booting the full
   context.
3. Reserve `@SpringBootTest` for genuine end-to-end flows where wiring the full context adds real
   value — it's the slowest test type, use it sparingly.
4. For code involving LLM calls, mock the provider client/port at the unit level (see
   `testing/llm-testing-strategies.md`) — don't call a real LLM API in unit or slice tests.
5. Structure tests Arrange-Act-Assert; one behavior per test; descriptive names stating the
   scenario and expected outcome.
6. Use parameterized tests for the same logic across multiple input variations instead of
   copy-pasted near-duplicate test methods.

## Rules
- Unit tests never hit the network, a real database, or a real LLM provider.
- A test suite that only tests the happy path is incomplete — cover the primary failure modes too.
- Flaky tests get fixed or removed, not retried into passing — a flaky test is a signal of a real
  concurrency/timing bug or a bad test design.

## Anti-patterns
- `@SpringBootTest` used by default for everything, making the suite slow.
- Tests that assert on implementation details (mock interaction counts) instead of observable
  behavior, becoming brittle to refactors.
- Skipping tests for "simple" changes that turn out to have edge cases.

## Validation
- New/changed behavior has a test that fails without the change and passes with it.
- The full suite still runs in reasonable time — check whether a new test type distribution is
  skewing toward slow, broad tests unnecessarily.

## Related skills
`testing/testcontainers-integration-testing.md`, `testing/llm-testing-strategies.md`,
`quality/code-review.md`
