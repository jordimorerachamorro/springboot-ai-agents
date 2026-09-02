---
name: event-driven-architecture
description: Design asynchronous, event-driven flows with reliable delivery and idempotent consumers.
category: messaging
tags: [messaging, events, async, idempotency]
priority: HIGH
version: 1.0
---

# Event-Driven Architecture

## Purpose
Decouple services/components via events without silently losing messages or double-processing
them — the two failure modes that make async systems unreliable in practice.

## When to use
- Work that doesn't need an immediate synchronous response (notifications, downstream
  projections, long-running AI processing pipelines).
- Coordinating consistency across aggregates/services without a distributed transaction.

## When NOT to use
- The caller genuinely needs a synchronous result to proceed — don't force an async event flow
  onto a request/response need just for architectural purity.
- Low-volume, simple flows where a direct call is easier to reason about and debug.

## Inputs
- Existing broker/technology in use (if any) — verify via `repository/repository-exploration.md`
  rather than assuming Kafka/RabbitMQ/etc.
- Existing event schema/versioning conventions.

## Process
1. Design events as facts that happened ("OrderPlaced"), not commands ("PlaceOrder") — commands
   imply a specific handler; events can have zero or many consumers.
2. Make consumers idempotent: process each event by a stable identifier so redelivery (which
   at-least-once delivery guarantees, and most brokers default to) doesn't cause duplicate effects.
3. For consistency between a DB write and publishing an event, use the outbox pattern (write the
   event to an outbox table in the same transaction as the business write, publish it via a
   separate relay) rather than publishing directly inside the transaction, which risks the
   classic "commit succeeded, publish failed" (or vice versa) inconsistency.
4. Version event schemas additively; consumers should tolerate unknown new fields.
5. Design a dead-letter path for events that repeatedly fail processing — don't let a poison
   message block the whole consumer indefinitely, and don't silently drop it either.
6. For AI-triggered async flows (e.g. "document uploaded → generate embeddings"), treat the LLM/
   embedding call as a step that can fail and needs retry/backoff, not a guaranteed-succeed step.

## Rules
- At-least-once delivery is the default assumption; consumers must be idempotent, not "usually fine."
- Never publish an event and commit the triggering DB write as two independent, unguarded steps.
- Dead-lettered messages must be visible/alertable, not silently discarded.

## Anti-patterns
- Events named as commands, coupling the publisher to a specific consumer's behavior.
- Consumers that assume exactly-once delivery.
- Retrying a failing message forever with no dead-letter escape hatch.

## Validation
- A duplicate delivery of the same event produces the same end state as a single delivery
  (verified by test, not assumption).
- Publish-and-persist consistency is verified under a simulated failure (e.g. kill the process
  between DB commit and publish, in a test or by code inspection of the outbox relay).

## Related skills
`architecture/domain-driven-design.md`, `reliability/resilience-and-fault-tolerance.md`,
`observability/structured-logging-and-tracing.md`
