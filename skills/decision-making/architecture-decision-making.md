---
name: architecture-decision-making
description: Compare technology/architecture alternatives explicitly by trade-off before committing to one.
category: decision-making
tags: [architecture, trade-offs, decision-making]
priority: HIGH
version: 1.0
---

# Architecture Decision Making

## Purpose
Make (and be able to explain) engineering decisions — technology choice, architecture pattern,
sync vs. async, workflow vs. agent — as an explicit trade-off comparison, not an unstated default.

## When to use
- Introducing a new dependency, architectural pattern, or significant design choice.
- The user asks "what should we use for X" or "how should we approach X."
- A choice has meaningful downstream cost if wrong (hard to reverse, affects multiple systems).

## When NOT to use
- Decisions already made by existing codebase convention — match the convention (see
  `repository/architecture-discovery.md`) rather than re-litigating it without cause.
- Low-stakes, easily-reversible choices don't need a formal comparison.

## Inputs
- The actual constraints: team size/expertise, existing stack, latency/consistency requirements,
  operational maturity (who's on call, what's already monitored).

## Process
1. State the decision being made precisely (not "how should we build this" but "should this be
   synchronous or event-driven," "should this use RAG or fine-tuning," "should this be an agent
   or a deterministic workflow").
2. List 2-3 real alternatives, not a strawman vs. the preferred option.
3. Compare on the dimensions that actually matter for this decision: correctness/reliability,
   operational complexity, cost, latency, team familiarity, reversibility.
4. State the recommendation with the specific trade-off being accepted — every choice gives up
   something; name it.
5. For AI-specific decisions, apply the library's standing defaults unless there's a concrete
   reason to deviate: prefer deterministic workflows to autonomous agents when a workflow can
   solve it reliably (see `ai/agents/agent-architecture.md`); prefer RAG over fine-tuning for
   knowledge that changes or needs citations (see `ai/rag/rag-architecture.md`); don't abstract a
   model provider unless a second provider is genuinely likely.
6. Note what would change the recommendation (a growth threshold, a new requirement) so the
   decision isn't treated as permanent regardless of context.

## Rules
- Never present a single option as "the" solution without naming what was compared against it.
- Reversibility matters: prefer the reversible choice when trade-offs are otherwise close.
- Don't let novelty/interest bias the recommendation toward the more complex option (a new agent
  framework, a new database) without a concrete requirement driving it.

## Anti-patterns
- Recommending microservices, a new agent framework, or a new datastore by default without a
  requirement that specifically demands it.
- A "trade-off comparison" that's actually just justification for a predetermined choice.

## Validation
- The recommendation names the specific trade-off accepted, not just the benefits.
- Someone unfamiliar with the discussion could read the comparison and understand why this choice
  was made over the alternatives.

## Related skills
`repository/architecture-discovery.md`, `ai/agents/agent-architecture.md`,
`ai/rag/rag-architecture.md`
