---
name: llm-performance-optimization
description: Reduce LLM-driven latency and cost via streaming, batching, caching, and context/model sizing.
category: performance
tags: [performance, llm, latency, caching, streaming]
priority: MEDIUM
version: 1.0
---

# LLM Performance Optimization

## Purpose
Keep AI-backed features responsive and affordable — LLM calls are the dominant latency and cost
factor in most GenAI features, and naive integration is usually both slow and expensive.

## When to use
- An AI-backed endpoint has noticeable latency (multi-second) or the feature is high-volume
  enough for per-call cost to matter.
- Designing a new AI feature where latency/cost characteristics should shape the design upfront.

## When NOT to use
- Low-volume, non-latency-sensitive internal tools rarely justify this optimization effort —
  correctness and simplicity first; optimize once there's a real signal (see
  `observability/ai-observability.md`).

## Inputs
- Actual latency/cost telemetry (see `observability/ai-observability.md`) — optimize from
  measurement, not guesswork.

## Process
1. Stream responses to the client where the UI can consume a stream — perceived latency drops
   dramatically even if total generation time is unchanged.
2. Reduce context size: send only the context actually needed (relevant retrieved chunks, not
   entire documents; recent conversation turns, not full history) — smaller input directly
   reduces both latency and cost.
3. Choose the smallest/cheapest model that meets the quality bar for a given task; reserve larger
   models for tasks that demonstrably need them (see `ai/cost/ai-cost-management.md` for the
   cost side of this trade-off).
4. Batch independent LLM calls where the provider supports batch APIs and latency isn't
   per-request-critical (e.g. offline processing jobs).
5. Use prompt/response caching for repeated or near-duplicate requests (exact-match cache for
   identical inputs; semantic caching only with a clear, tested similarity threshold and
   awareness of staleness/correctness risk).
6. Set concurrency limits/bulkheads on LLM calls so a burst of requests doesn't exhaust the
   provider's rate limit or your own thread pool (see
   `integrations/external-api-clients-resilience.md`).

## Rules
- Never optimize (cache, batch, downsize model) without a measurement showing the optimization is
  needed and actually helps — premature optimization here trades correctness/simplicity for
  unclear benefit.
- Caching LLM output must account for staleness and correctness — don't cache personalized or
  time-sensitive responses without a clear invalidation strategy.

## Anti-patterns
- Defaulting to the largest available model for every task regardless of complexity.
- Sending an entire document/history as context on every call when only a fraction is relevant.
- Semantic caching with no evaluation of false-positive (wrong cached answer) rate.

## Validation
- Latency/cost telemetry shows measurable improvement after the change.
- Cached responses are verified not to serve stale/incorrect answers for the cases that matter.

## Related skills
`observability/ai-observability.md`, `ai/cost/ai-cost-management.md`,
`integrations/external-api-clients-resilience.md`
