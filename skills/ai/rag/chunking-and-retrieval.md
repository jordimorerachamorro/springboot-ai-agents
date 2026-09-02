---
name: chunking-and-retrieval
description: Chunk documents, generate embeddings, and design retrieval/reranking that surfaces the right context.
category: ai/rag
tags: [rag, chunking, embeddings, retrieval, reranking]
priority: HIGH
version: 1.0
---

# Chunking and Retrieval

## Purpose
Split source documents and retrieve from them in a way that actually surfaces the right context
for a given query — the quality bottleneck of most RAG systems is here, not in generation.

## When to use
- Implementing the ingestion and retrieval stages of a RAG pipeline (see
  `ai/rag/rag-architecture.md` for whether RAG is warranted at all).
- Diagnosing poor RAG answer quality — usually a retrieval problem, not a generation problem.

## When NOT to use
- N/A once RAG architecture is confirmed appropriate.

## Inputs
- Document structure (prose, code, tables, structured records) — chunking strategy should match it.
- Typical query shape (short keyword queries vs. full natural-language questions).

## Process
1. Chunk by semantic boundaries (sections, paragraphs) where possible, not fixed character
   counts alone — a fixed-size split that cuts mid-sentence or mid-table degrades retrieval
   quality. Use fixed-size with overlap as a fallback when structure isn't available.
2. Size chunks to balance specificity vs. context: too small loses surrounding context needed to
   understand the chunk; too large dilutes embedding relevance and wastes context budget. Tune
   empirically against real queries, not a fixed universal number.
3. Attach metadata to each chunk (source document, section, date, access-control tags) — needed
   for citation, filtering, and tenant isolation (see `ai/security/ai-security.md`).
4. Consider contextual chunking (prepending brief document/section context to each chunk before
   embedding) for corpora where chunks lose critical meaning in isolation.
5. Use hybrid retrieval (vector similarity + keyword/BM25) by default for general-purpose
   corpora — pure vector search misses exact-match/keyword-heavy queries (IDs, specific terms)
   that keyword search handles well.
6. Apply metadata filtering before/alongside similarity search when queries have a scoping
   dimension (tenant, date range, document type) — don't rely on the model to ignore irrelevant
   retrieved content; filter it out at retrieval.
7. Add a reranking step when initial retrieval returns a larger candidate set than you'll pass to
   generation — a cheaper first-pass retrieval plus a precise reranker often beats a single
   expensive high-k similarity search.
8. Consider query rewriting/expansion for user queries that are terse or ambiguous relative to
   how the corpus is written, and multi-query retrieval for questions that need synthesizing
   information from multiple distinct chunks.

## Rules
- Chunk metadata always includes enough to cite the source and enforce access control.
- Retrieval quality is measured (see `ai/evaluation/llm-evaluation.md`), not assumed from a
  handful of manual spot checks.
- Tenant/access-scoped corpora filter at retrieval time, never rely on the model to self-censor
  based on prompt instructions alone.

## Anti-patterns
- Fixed-size chunking with no regard for document structure, splitting tables/code mid-block.
- No metadata filtering on a multi-tenant corpus, relying on the prompt to say "only use tenant
  A's data" — this is not a security boundary.
- Retrieving a large k and passing all of it to generation with no reranking, diluting relevance
  and wasting context budget/cost.

## Validation
- Retrieval metrics (precision/recall on a labeled query set, or manual relevance judgment on a
  representative sample) are tracked, not assumed.
- A tenant-scoped query is verified not to retrieve another tenant's chunks.

## Related skills
`ai/rag/rag-architecture.md`, `ai/evaluation/llm-evaluation.md`, `ai/security/ai-security.md`,
`observability/ai-observability.md`
