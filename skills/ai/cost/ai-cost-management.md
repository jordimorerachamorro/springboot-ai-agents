---
name: ai-cost-management
description: Control token usage and LLM spend deliberately, including runaway-agent prevention.
category: ai/cost
tags: [cost, tokens, budget, agents]
priority: MEDIUM
version: 1.0
---

# AI Cost Management

## Purpose
Make LLM/agent cost a designed-for, observable, bounded quantity — not a surprise on the monthly
provider invoice or an unbounded liability from a misbehaving agent loop.

## When to use
- Designing any AI feature with meaningful call volume, long contexts, or agent loops.
- Diagnosing an unexpected cost spike (paired with `observability/ai-observability.md`).

## When NOT to use
- Low-volume, one-off internal tooling where cost is negligible — don't over-engineer budget
  controls for something that costs cents a month; note it and move on.

## Inputs
- Expected call volume and context size for the feature.
- Cost telemetry from `observability/ai-observability.md`, if available.

## Process
1. Choose the smallest/cheapest model that meets the quality bar for each specific task — verify
   with `ai/evaluation/llm-evaluation.md`, don't default to the largest available model out of
   caution. Route different sub-tasks to different model tiers where their difficulty differs
   (e.g. a cheap model for classification, a larger one only for the genuinely hard step).
2. Minimize context sent per call: relevant retrieved chunks only (not whole documents), recent/
   summarized history only (not full transcripts) — see `ai/rag/chunking-and-retrieval.md`,
   `ai/agents/agent-memory.md`.
3. Minimize the number of model calls: don't make a separate LLM call for something a single call
   with structured output could accomplish; don't loop an agent when a fixed 2-step chain would do
   (see `ai/agents/agent-architecture.md`).
4. Cache aggressively where correctness allows — exact-match caching for repeated identical
   requests, provider-side prompt caching for repeated context prefixes (see
   `performance/llm-performance-optimization.md`).
5. For agents specifically, enforce a hard step/token budget per run and terminate with a defined
   failure state when exceeded — an agent with no budget ceiling is an unbounded cost liability,
   especially if it can retry or spawn sub-tasks.
6. Set organization/application-level spend alerts and, where the provider supports it, hard
   spend caps — defense in depth against a bug or attack causing runaway usage.
7. Attribute cost to feature/endpoint (see `observability/ai-observability.md`) so cost trade-offs
   can be made per-feature, not just at the aggregate application level.

## Rules
- Every agent loop has a hard step/token budget, enforced in code, not just documented as an
  expectation.
- Model tier is chosen per task based on evaluated necessity, not by default to "the best model."
- Cost is attributable per feature/endpoint, not only visible in aggregate.

## Anti-patterns
- An agent loop with no step limit that can retry indefinitely on a persistently failing tool.
- Defaulting every call to the most capable (and most expensive) model regardless of task complexity.
- Sending full document/conversation history on every call when a fraction is relevant.

## Validation
- A simulated worst-case agent run (persistent tool failure, unsatisfiable goal) terminates within
  the defined budget instead of running unbounded.
- Cost telemetry can answer "what does feature X cost per typical usage" with real numbers, not
  an estimate.

## Related skills
`ai/agents/agent-architecture.md`, `performance/llm-performance-optimization.md`,
`observability/ai-observability.md`, `ai/evaluation/llm-evaluation.md`
