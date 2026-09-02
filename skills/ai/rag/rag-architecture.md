---
name: rag-architecture
description: Decide when and how to architect a Retrieval-Augmented Generation system versus simpler alternatives.
category: ai/rag
tags: [rag, retrieval, architecture, embeddings]
priority: HIGH
version: 1.0
---

# RAG Architecture

## Purpose
Design a RAG system's overall shape correctly — and, just as importantly, decide when RAG is the
right tool at all versus a simpler alternative.

## When to use
- The task needs the model to answer using specific, current, or proprietary knowledge not
  reliably present in its training data (documentation, internal knowledge, user content).
- Answers need citations/grounding back to source material.

## When NOT to use
- Small, static, fully-enumerable knowledge that fits comfortably in a prompt — just include it
  directly; RAG's retrieval machinery is unneeded overhead.
- Knowledge that should shape the model's general behavior/style rather than be looked up per
  query — that's closer to fine-tuning or a system prompt concern, not retrieval.
- Don't reach for RAG as a default for "the app needs to know about X" without checking whether
  the data fits directly in context.

## Inputs
- The corpus: size, update frequency, format (structured vs. unstructured), sensitivity.
- Whether answers need citations/source attribution.

## Process
1. Confirm RAG is warranted (see When NOT to use) before designing anything — this is the most
   commonly skipped, most valuable step.
2. Design the pipeline as explicit stages: ingestion → chunking → embedding → indexing →
   retrieval → (optional reranking) → generation. Each stage is independently testable and
   observable (see `ai/rag/chunking-and-retrieval.md` for the retrieval-side details).
3. Choose a vector store based on actual requirements (scale, existing infra, hybrid
   search/metadata filtering needs) — don't default to a specific vector database without
   checking what the project already has available (a relational DB with a vector extension may
   be sufficient and avoid a new infra dependency).
4. Decide retrieval strategy: pure vector similarity, hybrid (vector + keyword/BM25), or
   filtered-by-metadata — hybrid search consistently outperforms pure vector search for
   keyword-heavy or exact-match-sensitive queries.
5. Design for grounding and citation: retrieved chunks should carry enough metadata (source,
   location) to cite back, and the generation prompt should instruct the model to answer only
   from retrieved context and say so when context is insufficient — this is the primary
   hallucination-mitigation lever.
6. Plan for retrieval failure (no relevant chunks found) as an explicit, handled case — a defined
   "I don't have information about that" response, not a hallucinated answer or empty context
   passed silently into generation.
7. Treat the corpus as a security surface: documents can contain content aimed at manipulating
   the model (RAG poisoning/indirect prompt injection) — see `ai/security/ai-security.md`.

## Rules
- RAG is chosen for a stated reason (freshness, scale, need for citations) — never by default.
- Every generation grounded in retrieved context should be traceable back to which chunks were used.
- No-relevant-results is an explicit, tested case, not an implicit fallthrough.

## Anti-patterns
- Building a full RAG pipeline for a knowledge base small enough to fit directly in the prompt.
- Retrieval with no citation/traceability, making hallucination indistinguishable from grounded output.
- Ignoring the corpus as an untrusted input surface.

## Validation
- A query with no relevant corpus content produces the defined "insufficient information"
  behavior, not a fabricated answer (verify with a real test case, see
  `ai/evaluation/llm-evaluation.md`).
- Retrieval and generation are independently observable (see `observability/ai-observability.md`).

## Related skills
`ai/rag/chunking-and-retrieval.md`, `ai/evaluation/llm-evaluation.md`,
`ai/security/ai-security.md`, `decision-making/architecture-decision-making.md`
