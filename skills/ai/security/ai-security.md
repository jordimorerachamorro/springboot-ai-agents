---
name: ai-security
description: Apply the AI-specific threat model — prompt injection, excessive agency, data leakage, RAG poisoning — to LLM/agent features.
category: ai/security
tags: [ai-security, prompt-injection, excessive-agency, owasp-llm]
priority: CORE
version: 1.0
---

# AI Security

## Purpose
Apply a threat model specific to LLM-integrated features, extending (not replacing) standard
application security, since LLMs introduce failure modes traditional security review misses.

## When to use
- Any feature where an LLM processes untrusted content (user input, retrieved documents, web
  content, tool results) or has tool/agent access to take actions.
- Security review of an AI-integrated feature (paired with `security/api-security.md`).

## When NOT to use
- N/A — some subset applies to essentially every LLM feature; scope which specific risks are live
  for the feature at hand.

## Inputs
- What untrusted content the model processes, and what authority/tools it has access to.

## Process
1. **Prompt injection (direct and indirect)**: any content the model reads that wasn't authored
   by the system/developer — user input, retrieved RAG chunks, tool call results, web content —
   can contain text attempting to override the system's instructions. Never grant instruction-level
   trust to such content; keep system instructions structurally separate (system prompt / dedicated
   parameter, see `ai/prompting/prompt-engineering.md`) and treat everything else as data to
   process, not commands to follow.
2. **Excessive agency**: an agent's tool access should be the minimum needed (see
   `ai/agents/tool-design.md`) and scoped to the calling user's actual authority — never grant an
   agent broader permissions than the least-privileged human on whose behalf it acts, and require
   approval for consequential actions (see `ai/agents/agent-architecture.md`).
3. **Data leakage**: an LLM can be induced (via injection or by ordinary conversation) to repeat
   sensitive content from its context (system prompt secrets, other users' data pulled into
   context, retrieved documents outside the caller's access scope). Never put anything in a
   prompt the caller shouldn't be able to extract — including in the system prompt.
4. **RAG/tool poisoning**: a malicious or compromised document in a retrieval corpus, or a
   malicious tool response, is attacker-controlled input the same as any user input — apply the
   same untrusted-input handling (see `ai/rag/chunking-and-retrieval.md` for corpus access control).
5. **Tenant isolation**: in multi-tenant systems, verify retrieval, memory, and tool access are
   scoped per-tenant at the data layer — never rely on prompt instructions ("only use this
   tenant's data") as the isolation boundary; that's advisory to the model, not enforced.
6. **Output validation**: model output is untrusted output as much as input is untrusted input —
   never render model output as executable content (HTML/script injection risk), never execute it
   as code/commands, without the same validation/encoding you'd apply to any other untrusted source.
7. **Audit logging**: log tool calls, retrieved sources, and consequential actions with enough
   detail to reconstruct what happened after the fact (see `observability/ai-observability.md`) —
   essential for investigating a suspected injection or misuse incident.

## Rules
- Untrusted content (user input, retrieved documents, tool results, web content) never carries
  instruction-level authority — only the system-authored prompt does.
- Tenant/access-scoping for retrieval, memory, and tools is enforced at the data/authorization
  layer, never only by prompt instruction.
- Model output is validated/encoded before being rendered, executed, or trusted, exactly like any
  other untrusted input.

## Anti-patterns
- A system prompt containing secrets or instructions the model shouldn't be able to be tricked
  into revealing.
- An agent tool that executes with full service-account privilege rather than the calling user's
  actual scope.
- Relying on "the prompt tells the model not to" as the only defense against a real security boundary.

## Validation
- A test injects adversarial instructions into retrieved/user content and confirms the system
  prompt's actual constraints still hold (tool restrictions, tenant scoping) — not just that the
  model "says" it won't comply.
- Tenant isolation is verified at the data layer independent of prompt content.

## Related skills
`ai/agents/tool-design.md`, `ai/agents/agent-architecture.md`, `ai/rag/chunking-and-retrieval.md`,
`security/api-security.md`, `observability/ai-observability.md`
