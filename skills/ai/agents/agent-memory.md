---
name: agent-memory
description: Design conversation, session, and long-term memory for AI agents without leaking data across boundaries.
category: ai/agents
tags: [agents, memory, context, privacy]
priority: MEDIUM
version: 1.0
---

# Agent Memory

## Purpose
Give an agent or conversational AI feature the right amount of persistent context — enough to be
coherent across turns/sessions, without unbounded context growth, cross-user leakage, or
retaining data longer than justified.

## When to use
- Building a multi-turn conversational feature or an agent whose behavior should be informed by
  past interactions.
- Deciding what, if anything, should persist beyond a single request/session.

## When NOT to use
- Stateless, single-turn interactions need no memory design — don't add a memory layer
  speculatively for a feature that doesn't yet need multi-turn context.

## Inputs
- Whether continuity is needed within a session only, or across sessions (user-level long-term
  memory) — these have very different privacy and design implications.
- Data retention requirements/constraints already governing the application.

## Process
1. Distinguish memory tiers explicitly: **short-term/working memory** (the current
   conversation/agent-loop's active context, lives only for the request/session), **session
   memory** (persists for a user's session, cleared on session end), and **long-term memory**
   (persists across sessions, tied to a user/account) — each has different storage, retention, and
   privacy handling.
2. For conversation history, summarize/compress older turns rather than letting context grow
   unbounded — both a cost concern (see `ai/cost/ai-cost-management.md`) and, past a point, a
   quality concern as relevant signal gets diluted.
3. Store long-term memory scoped strictly per-user/tenant, with the same access-control rigor as
   any other user data — memory is stored PII/behavioral data, not a special AI-only concern
   exempt from normal data handling rules (see `ai/security/ai-security.md`).
4. Make retrieval into memory (what past context gets pulled into the current prompt) explicit
   and bounded — don't dump an entire history into context; retrieve what's relevant, similar to
   RAG retrieval (see `ai/rag/chunking-and-retrieval.md`).
5. Define retention and deletion: memory tied to a user must be deletable (account
   deletion/GDPR-style requests) and should have a stated retention policy, not persist indefinitely
   by default.
6. Treat memory content as untrusted on read, same as any other stored data flowing back into a
   prompt — a poisoned/manipulated past interaction shouldn't gain elevated trust just because
   it's "the agent's own memory."

## Rules
- Long-term memory is strictly scoped per-user/tenant — never shared across users implicitly.
- Memory has a defined retention/deletion policy, not indefinite retention by default.
- Context window growth from accumulated memory is bounded (summarization/retrieval), not unbounded.

## Anti-patterns
- Concatenating full conversation history into every prompt indefinitely, growing cost and
  latency unboundedly.
- Long-term memory with no deletion mechanism, conflicting with data retention/privacy requirements.
- Memory shared across a multi-tenant system with no isolation, risking cross-tenant data leakage.

## Validation
- A test confirms one user's long-term memory is never retrievable in another user's context.
- Context size stays bounded across a long conversation (verify with a multi-turn test, not
  assumption).

## Related skills
`ai/agents/agent-architecture.md`, `ai/rag/chunking-and-retrieval.md`,
`ai/security/ai-security.md`, `ai/cost/ai-cost-management.md`
