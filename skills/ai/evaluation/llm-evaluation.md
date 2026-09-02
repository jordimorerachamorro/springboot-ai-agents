---
name: llm-evaluation
description: Evaluate prompts, RAG, and agent behavior as a continuous engineering discipline, not a one-off manual check.
category: ai/evaluation
tags: [evaluation, llm-as-judge, rag-evaluation, agent-evaluation]
priority: HIGH
version: 1.0
---

# LLM Evaluation

## Purpose
Know, with evidence, whether an AI feature actually works — before shipping a prompt/model
change and on an ongoing basis in production — rather than relying on a handful of manual spot checks.

## When to use
- Before shipping any change to a prompt, model, retrieval strategy, or agent tool set.
- Establishing baseline quality for a new AI feature.
- Investigating a reported quality regression (paired with `debugging/bug-investigation.md`).

## When NOT to use
- Trivial, low-stakes AI features with no downstream consequence of imperfect output may not
  justify a full evaluation harness — but even then, a small smoke-test set costs little.

## Inputs
- A representative set of real or realistic inputs, including edge cases and known failure modes.
- What "correct" means for this task — deterministic-checkable properties vs. genuinely
  subjective quality.

## Process
1. Build a golden dataset: representative inputs with either exact expected outputs
   (deterministic tasks: classification, extraction) or documented acceptance criteria
   (open-ended generation). Grow it over time as new edge cases/regressions are discovered.
2. Use deterministic checks wherever the task allows: schema validity, exact field match,
   presence/absence of required content, format compliance — cheaper, faster, and more reliable
   than model-based judging, and should be preferred whenever the property is checkable directly.
3. Use LLM-as-a-judge only for genuinely subjective qualities (tone, helpfulness, coherence) that
   can't be checked deterministically — and validate the judge itself against a small
   human-labeled sample before trusting its scores at scale.
4. For RAG systems, evaluate retrieval and generation separately: retrieval metrics
   (precision/recall/relevance of retrieved chunks against a labeled query set) and generation
   metrics (groundedness — does the answer only use retrieved content; faithfulness; relevance to
   the query) — a good answer from bad retrieval is luck, not a working system.
5. For agents, evaluate the trajectory, not just the final outcome: were the right tools called,
   in a sensible sequence, with correct arguments — not only whether the end state looks correct,
   since a wrong path can accidentally reach a correct-looking result.
6. Run the evaluation suite in CI on prompt/model/retrieval changes as a regression gate, the same
   way you'd run tests for any other code change.
7. In production, sample and evaluate real traffic (with privacy safeguards) to catch drift that
   the offline golden set doesn't cover — offline evaluation alone gives a false sense of completeness.
8. Compare models/prompts on the same evaluation set when making a selection decision (see
   `decision-making/architecture-decision-making.md`) rather than an informal side-by-side glance.

## Rules
- No prompt/model/retrieval change ships without running it against the evaluation set.
- Prefer deterministic checks over LLM-as-a-judge wherever the property is directly checkable.
- An LLM-as-a-judge is itself validated against human judgment before being trusted as a metric.

## Anti-patterns
- Shipping prompt changes based on "it looked better in the few examples I tried."
- Using LLM-as-a-judge for properties that could be checked deterministically (e.g. valid JSON,
  presence of a required field).
- Evaluating only final RAG answers, never retrieval quality in isolation — makes it impossible
  to tell whether a bad answer is a retrieval problem or a generation problem.

## Validation
- A regression in the golden dataset is caught before merge, not after a user reports it.
- Evaluation results are tracked over time (even a simple log/spreadsheet) so drift is visible.

## Related skills
`ai/prompting/prompt-engineering.md`, `ai/rag/chunking-and-retrieval.md`,
`ai/agents/agent-architecture.md`, `testing/llm-testing-strategies.md`,
`debugging/bug-investigation.md`
