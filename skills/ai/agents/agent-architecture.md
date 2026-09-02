---
name: agent-architecture
description: Decide whether an autonomous agent is warranted, and if so design its loop, planning, and control boundaries.
category: ai/agents
tags: [agents, agentic, architecture, orchestration]
priority: HIGH
version: 1.0
---

# Agent Architecture

## Purpose
Apply agentic AI only where it earns its cost, and when it's warranted, design the agent loop
with explicit control boundaries rather than unrestricted autonomy.

## When to use
- The task genuinely requires dynamic, multi-step reasoning where the sequence of actions can't
  be determined in advance (the number and order of tool calls depends on intermediate results).
- Designing or reviewing an agent loop, its planning strategy, or its stopping condition.

## When NOT to use — read this first
- **Default assumption: prefer a deterministic workflow over an autonomous agent whenever the
  workflow can solve the problem reliably.** A fixed sequence of steps (even with conditionals,
  retries, and LLM calls at specific points) is more predictable, cheaper, easier to test, and
  easier to debug than an agent loop deciding its own steps. Reach for an agent only when the
  step sequence genuinely can't be predetermined.
- A single LLM call with structured output, or a short deterministic chain of 2-3 fixed LLM
  calls, is not an agent — don't add loop/planning machinery around something that doesn't need it.

## Inputs
- Confirmation the task's step sequence truly can't be fixed in advance (if it can, this skill
  doesn't apply — see `decision-making/architecture-decision-making.md`).
- The scope of tools/actions the agent genuinely needs (see `ai/agents/tool-design.md`).

## Process
1. **Justify the agent explicitly** before designing it: what makes this task's action sequence
   unpredictable enough that a fixed workflow can't handle it?
2. Bound the loop: maximum iterations/steps, explicit stopping conditions (goal reached, max
   steps hit, repeated failure), and a hard timeout — an unbounded agent loop is a cost and
   reliability risk (see `ai/cost/ai-cost-management.md`).
3. Grant the minimum set of tools needed for the task — least privilege applies to agents as much
   as to any other principal (see `ai/agents/tool-design.md`, `ai/security/ai-security.md`).
4. Design explicit state: what the agent tracks across steps (short-term/working memory) and
   what, if anything, persists beyond a single run (see `ai/agents/agent-memory.md`) — don't let
   state accumulate unbounded into the context window.
5. Add human-in-the-loop approval for actions with real-world side effects (sending
   communications, financial transactions, destructive operations, external writes) — the agent
   proposes, a human or a separate deterministic check confirms, for anything above a defined
   risk threshold.
6. Make every step observable: which tool was called, with what arguments, what it returned, and
   why the agent chose it, where the provider surfaces reasoning (see
   `observability/ai-observability.md`) — an agent that's a black box is not production-ready.
7. Design explicit failure recovery: what happens when a tool call fails, when the model produces
   an invalid next action, when the loop hits its step limit without reaching a goal — these are
   expected outcomes needing defined behavior, not edge cases to ignore.
8. Only reach for multi-agent orchestration when a single agent's context/tool surface genuinely
   can't handle the task's breadth — multi-agent systems multiply the coordination and failure
   surface and are rarely the first-choice design.

## Rules
- No unbounded agent loops — always a max step count and timeout.
- Tools granted are the minimum needed, not "everything that might be useful."
- Side-effecting actions above a defined risk threshold require approval, not silent autonomous execution.
- Every agent step is logged/traced individually.

## Anti-patterns
- Building an agent for a task with a fully predictable step sequence.
- An agent with broad tool access "in case it needs it."
- No step limit, relying on the model to "know when to stop."
- Treating the agent's internal reasoning as ground truth instead of validating its actions/outputs.

## Validation
- You can state, in one sentence, why this task couldn't be a deterministic workflow instead.
- The loop terminates (goal, step limit, or timeout) in all tested scenarios, including
  adversarial ones (a tool that always fails, a goal that's never satisfiable).
- Every tool call in a test run is traceable in logs/traces.

## Related skills
`ai/agents/tool-design.md`, `ai/agents/agent-memory.md`, `ai/security/ai-security.md`,
`ai/cost/ai-cost-management.md`, `decision-making/architecture-decision-making.md`
