---
name: llm-testing-strategies
description: Test code that calls LLMs despite non-deterministic output — mocking, contract tests, and regression tests.
category: testing
tags: [testing, llm, ai, mocking, regression]
priority: HIGH
version: 1.0
---

# LLM Testing Strategies

## Purpose
Get real test coverage for LLM-integrated code without either (a) calling a real model in every
test run (slow, costly, flaky) or (b) skipping testing because "the output is non-deterministic."

## When to use
- Any code path that calls an LLM provider, directly or via Spring AI.
- Testing prompt changes, structured-output parsing, tool-calling logic, or RAG retrieval code.

## When NOT to use
- Don't use this in place of `testing/spring-boot-testing-strategy.md` for the non-AI parts of
  the same feature — apply that skill to everything else.

## Inputs
- The port/interface boundary around the LLM call (see
  `architecture/clean-hexagonal-architecture.md` — this is what makes the rest possible).

## Process
1. **Unit-test business logic against a mocked LLM port.** The port returns fixed responses;
   assert on how your code handles them (including malformed/unexpected ones) — this is most of
   your coverage and runs fast, deterministically, with no API cost.
2. **Structured output contract tests**: feed the parser/validator a set of fixture responses
   (valid, malformed, missing fields, wrong types) and assert correct handling of each — this is
   where most real production bugs in AI features actually occur.
3. **Prompt regression tests**: maintain a small, versioned set of representative inputs and
   expected properties of the output (not exact string match — check for required fields,
   absence of forbidden content, adherence to format). Run these against a real model in a
   separate, explicitly-gated test suite (nightly/CI-optional), not the default fast suite.
4. **Tool-calling tests**: verify the model is offered the correct tool schema and that your code
   correctly executes/validates whatever tool call comes back — mock the model's tool-call
   response, don't mock away the execution/validation logic being tested.
5. **Semantic assertions over exact-match** when a live-model test is warranted: assert properties
   (contains X, doesn't contain Y, valid JSON matching schema, length within bounds) rather than
   asserting exact text, which will flake with any model/prompt update.
6. Never let the default/fast test suite make real network calls to an LLM provider — gate those
   behind a separate profile/tag so CI cost and flakiness stay bounded.

## Rules
- Business logic tests never depend on live model output.
- Structured-output/tool-call parsing is tested with adversarial fixtures (malformed, truncated,
  wrong schema) — not just the happy path.
- Live-model tests (if any) are isolated, explicitly tagged, and never block the default suite.

## Anti-patterns
- Skipping tests for AI features entirely because "the model is non-deterministic."
- Asserting exact string equality on LLM output.
- Calling a real paid API in every CI run for basic unit-level coverage.

## Validation
- The AI-integrated code's tests run fully offline (mocked port) with no network calls, and pass
  reliably in CI.
- Malformed-response fixtures are handled gracefully (validated/rejected, not silently accepted).

## Related skills
`ai/llm/structured-output.md`, `ai/evaluation/llm-evaluation.md`,
`architecture/clean-hexagonal-architecture.md`, `testing/spring-boot-testing-strategy.md`
