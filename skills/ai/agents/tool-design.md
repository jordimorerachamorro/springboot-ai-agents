---
name: tool-design
description: Design safe, well-scoped tools/functions that an LLM or agent can invoke.
category: ai/agents
tags: [agents, tools, function-calling, tool-schemas]
priority: HIGH
version: 1.0
---

# Tool Design

## Purpose
Design tools an LLM can call that are unambiguous to select correctly, safe to execute, and
impossible to misuse beyond their intended scope.

## When to use
- Defining any function/tool exposed to an LLM via tool-calling/function-calling, whether in a
  single-call structured-interaction or a full agent loop.

## When NOT to use
- Exposing internal implementation details as tools instead of business-meaningful operations —
  design tools at the level the model should reason about, not raw CRUD/SQL access.

## Inputs
- The specific business operation the tool performs and its real-world side effects (if any).

## Process
1. Give each tool a single, clear responsibility with a name and description precise enough that
   the model reliably picks the right tool among similar ones — ambiguous tool boundaries cause
   wrong-tool selection.
2. Define the input schema strictly: required fields, types, enums for constrained values,
   explicit descriptions per parameter — the model relies entirely on the schema/description to
   know how to call it correctly.
3. Validate every tool input server-side before execution, exactly as you would for any external
   API input (see `security/api-security.md`) — the model can and will produce malformed or
   adversarial-looking arguments, whether from error or from injected content it processed.
4. Scope tool authorization to the calling context (user/session permissions), not to whatever
   the backing service account can technically do — a tool must not grant the agent more
   authority than the requesting user actually has.
5. Design tool outputs to be concise and structured — return what the model needs to proceed, not
   a raw dump of an entire API response, which wastes context and can bury the relevant fields.
6. Make side-effecting tools (writes, sends, deletes) idempotent where feasible (accept an
   idempotency key, or make repeated calls safe) — agent loops can and do retry/repeat calls.
7. Log every tool invocation with its arguments and result (redacting sensitive fields) for
   observability and after-the-fact audit (see `observability/ai-observability.md`).
8. For tools that fetch external resources (URLs, files) apply the same SSRF/allowlist
   protections as any server-side fetch (see `security/api-security.md`).

## Rules
- Tool inputs are validated server-side, always — never trusted because "the model generated them."
- A tool never has more authority than the least-privileged principal on whose behalf it's called.
- Side-effecting tools above a defined risk level require explicit approval (see
  `ai/agents/agent-architecture.md`) before executing, not just before the agent decides to call them.

## Anti-patterns
- A generic "run this SQL" or "execute this shell command" tool — far too broad, effectively
  ceding full system access to whatever the model decides to generate.
- Tools with overlapping, ambiguous responsibilities causing unreliable tool selection.
- Trusting tool arguments the model produced without the validation you'd apply to any other
  external input.

## Validation
- A test calls the tool with adversarial/malformed arguments and confirms it's rejected, not
  executed.
- Tool authorization is verified to be scoped to the calling user/session, not the service
  account's full permission set.

## Related skills
`ai/agents/agent-architecture.md`, `security/api-security.md`, `ai/security/ai-security.md`,
`observability/ai-observability.md`
