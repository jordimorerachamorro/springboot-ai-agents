# Spring Boot + Generative AI Engineering Skills Library

A reusable, composable library of engineering skills for an AI coding assistant (e.g. Claude Code)
working inside Spring Boot codebases — including those that integrate Generative AI (LLMs, RAG,
agents). This library is **not** built for one project. It is a portable capability system meant
to be dropped into any Spring Boot repository.

## What this is

Each file in `skills/` is a self-contained unit of engineering judgment: when to apply it, how to
reason through the problem, what good and bad look like, and how to verify the result. Skills are
not code generators or boilerplate templates — they encode the reasoning an experienced Spring
Boot + GenAI engineer would apply, so the agent behaves consistently across unfamiliar repos.

## How an agent should use this library

1. **Orient before acting.** Start from `repository/repository-exploration.md` and
   `repository/architecture-discovery.md` before writing code in an unfamiliar repo.
2. **Match the skill to the task**, not the other way around. Read a skill's "When to use" /
   "When NOT to use" sections before applying it — activation should be narrow and deliberate.
3. **Compose, don't collapse.** Most real tasks touch multiple skills (e.g. adding an LLM-backed
   endpoint touches `api/rest-api-design.md`, `ai/llm/llm-integration-fundamentals.md`,
   `ai/prompting/prompt-engineering.md`, and `testing/llm-testing-strategies.md`). Follow the
   "Related skills" links rather than trying to find one skill that does everything.
4. **Prefer the conceptual skill, then the technology-specific one.** Conceptual skills
   (`ai/llm/llm-integration-fundamentals.md`) explain the engineering problem; technology skills
   (`integrations/openai-integration.md`, `integrations/anthropic-integration.md`) explain how a
   specific provider/library implements it. Don't reach for a vendor skill until the conceptual
   skill says you need vendor-specific behavior.
5. **Validate before declaring done.** Every skill has a "Validation" section — use it as an exit
   checklist, not a suggestion.

## Organizing principles

- **Reusable over project-specific.** No skill references a specific company, product, database
  instance, or cloud account. Provider-specific knowledge lives in `integrations/` and is optional.
- **Deterministic over agentic, by default.** The AI skills repeatedly apply the principle: *prefer
  a deterministic workflow to an autonomous agent whenever the workflow can solve the problem
  reliably.* Agentic skills exist for when that assumption genuinely breaks down.
- **LLM output is untrusted input.** Every AI skill treats model output as data to validate, not
  as a trusted instruction or fact.
- **Meaningful granularity.** Skills represent a reusable capability an experienced engineer would
  recognize by name — not a single code snippet (no `create-controller.md`) and not an entire
  discipline crammed into one file (no monolithic `springboot.md`).

## Directory structure

```
skills/
├── README.md
├── meta/                  # Skills for managing the skill system itself
├── repository/            # Understanding an unfamiliar codebase
├── architecture/          # Clean/hexagonal architecture, DDD, service boundaries
├── spring/                # Spring Boot core mechanics
├── api/                   # REST API design
├── persistence/           # JPA/Hibernate, transactions, migrations
├── messaging/             # Event-driven / async architecture
├── integrations/          # External clients, resilience, and vendor-specific AI integrations
├── security/              # Traditional backend security
├── testing/               # Spring Boot + AI testing strategy
├── observability/         # Logging, tracing, metrics, AI observability
├── performance/           # JVM, caching, LLM performance
├── reliability/           # Resilience patterns, AI failure handling
├── devops/                # Build, containerization, CI/CD, prod readiness
├── quality/               # Code review, refactoring, technical debt
├── git-workflow/          # Safe repository changes
├── debugging/             # Evidence-based investigation
├── decision-making/       # Trade-off / technology-selection reasoning
└── ai/
    ├── llm/               # LLM integration fundamentals, structured output, Spring AI
    ├── prompting/         # Prompt engineering, injection awareness
    ├── rag/               # RAG architecture, chunking, retrieval
    ├── agents/            # Agent architecture, tool design, memory
    ├── evaluation/        # LLM/RAG/agent evaluation as an engineering discipline
    ├── security/          # AI-specific threat model
    └── cost/              # Token/cost management
```

## Skill dependency chains (illustrative, not exhaustive)

```
repository-exploration → architecture-discovery → architecture-decision-making
    → feature implementation (spring/*, api/*, persistence/*, messaging/*)
    → testing (spring-boot-testing-strategy, testcontainers-integration-testing)
    → code-review → documentation

llm-integration-fundamentals → prompt-engineering → structured-output
    → llm-testing-strategies → llm-evaluation

rag-architecture → chunking-and-retrieval → embeddings/vector store (technology-specific)
    → llm-evaluation (retrieval metrics)

agent-architecture → tool-design → agent-memory → llm-evaluation (agent evaluation)
    → ai-security (guardrails, least privilege)
```

## Skill file structure

Every skill uses the same template (sections omitted when not applicable):

```
---
name: kebab-case-id
description: One-line, specific description used for activation matching
category: one of the top-level directories above
tags: [free-form]
priority: CORE | HIGH | MEDIUM | OPTIONAL
version: 1.0
---

# Skill Name
## Purpose
## When to use
## When NOT to use
## Inputs
## Process
## Rules
## Patterns
## Anti-patterns
## Examples
## Validation
## Related skills
```

## Skill inventory

| Skill | Category | Purpose | Depends on | Priority |
|---|---|---|---|---|
| skill-discovery | meta | Find the right skill(s) for a task | — | CORE |
| skill-creation | meta | Author a new skill correctly | skill-discovery | HIGH |
| skill-review | meta | Validate a skill before it's added | skill-creation | HIGH |
| repository-exploration | repository | Orient in an unfamiliar codebase | — | CORE |
| architecture-discovery | repository | Reverse-engineer the real architecture | repository-exploration | CORE |
| clean-hexagonal-architecture | architecture | Ports/adapters, dependency direction | architecture-discovery | HIGH |
| domain-driven-design | architecture | Domain modeling, bounded contexts | clean-hexagonal-architecture | MEDIUM |
| spring-boot-fundamentals | spring | DI, beans, lifecycle, component scanning | — | CORE |
| configuration-and-profiles | spring | Externalized config, profiles, feature flags | spring-boot-fundamentals | HIGH |
| rest-api-design | api | Resource design, HTTP semantics, versioning | spring-boot-fundamentals | CORE |
| validation-and-error-handling | api | Request validation, error responses | rest-api-design | CORE |
| jpa-hibernate-patterns | persistence | Entities, repositories, N+1, fetch strategy | spring-boot-fundamentals | CORE |
| transactions-and-locking | persistence | Transaction boundaries, optimistic/pessimistic locking | jpa-hibernate-patterns | HIGH |
| event-driven-architecture | messaging | Async processing, outbox, idempotent consumers | architecture-discovery | HIGH |
| external-api-clients-resilience | integrations | WebClient/RestClient, retries, circuit breakers | spring-boot-fundamentals | CORE |
| openai-integration | integrations | OpenAI SDK specifics | llm-integration-fundamentals | OPTIONAL |
| anthropic-integration | integrations | Anthropic SDK specifics | llm-integration-fundamentals | OPTIONAL |
| spring-security-fundamentals | security | Authn/authz, filter chain, method security | spring-boot-fundamentals | CORE |
| api-security | security | OWASP API risks, input validation, SSRF | spring-security-fundamentals | HIGH |
| spring-boot-testing-strategy | testing | Unit/slice/integration test pyramid | spring-boot-fundamentals | CORE |
| testcontainers-integration-testing | testing | Real infra in tests | spring-boot-testing-strategy | HIGH |
| llm-testing-strategies | testing | Testing non-deterministic AI behavior | spring-boot-testing-strategy, llm-integration-fundamentals | HIGH |
| structured-logging-and-tracing | observability | Correlation IDs, structured logs, tracing | spring-boot-fundamentals | CORE |
| ai-observability | observability | Token/latency/cost telemetry for AI calls | structured-logging-and-tracing, llm-integration-fundamentals | HIGH |
| llm-performance-optimization | performance | Latency, streaming, batching, caching for LLMs | llm-integration-fundamentals | MEDIUM |
| resilience-and-fault-tolerance | reliability | Retries, timeouts, circuit breakers, degradation | external-api-clients-resilience | HIGH |
| containerization-and-cicd | devops | Docker, CI/CD, environment config | spring-boot-fundamentals | HIGH |
| code-review | quality | Reviewing correctness, design, tests | architecture-discovery | CORE |
| safe-repository-changes | git-workflow | Minimal, safe, reviewable changes | repository-exploration | CORE |
| bug-investigation | debugging | Evidence-based root cause analysis | structured-logging-and-tracing | CORE |
| architecture-decision-making | decision-making | Comparing alternatives with explicit trade-offs | architecture-discovery | HIGH |
| llm-integration-fundamentals | ai/llm | Provider-agnostic LLM integration | spring-boot-fundamentals | CORE |
| structured-output | ai/llm | Reliable structured/JSON generation | llm-integration-fundamentals | CORE |
| prompt-engineering | ai/prompting | Designing and versioning prompts | llm-integration-fundamentals | CORE |
| rag-architecture | ai/rag | When/how to build a RAG system | llm-integration-fundamentals | HIGH |
| chunking-and-retrieval | ai/rag | Chunking, embeddings, retrieval, reranking | rag-architecture | HIGH |
| agent-architecture | ai/agents | When an agent is justified vs. a workflow | llm-integration-fundamentals | HIGH |
| tool-design | ai/agents | Designing tools an LLM can call safely | agent-architecture | HIGH |
| agent-memory | ai/agents | Conversation/session/long-term memory | agent-architecture | MEDIUM |
| llm-evaluation | ai/evaluation | Evaluating prompts, RAG, agents as an engineering discipline | llm-integration-fundamentals | HIGH |
| ai-security | ai/security | Prompt injection, data leakage, excessive agency | llm-integration-fundamentals | CORE |
| ai-cost-management | ai/cost | Token/cost control, runaway-agent prevention | llm-integration-fundamentals, agent-architecture | MEDIUM |

**Documented backlog (MEDIUM/OPTIONAL, not yet generated — add via `meta/skill-creation.md`
when a concrete project need arises):** service-boundaries, architecture-decision-records,
autoconfiguration-and-starters, api-versioning-and-openapi, database-migrations,
query-performance, kafka-messaging-patterns, outbox-and-idempotency, aws-bedrock-integration,
oauth2-oidc-jwt, secrets-management, test-data-builders, metrics-and-actuator,
jvm-and-concurrency-performance, caching-strategies, ai-failure-handling,
production-readiness, refactoring-and-technical-debt, legacy-modernization,
technical-documentation, ai-specific-debugging, spring-ai-architecture,
prompt-injection-awareness (folded into `ai/security/ai-security.md` for now),
multi-agent-orchestration.

## Adding a new skill

Use `meta/skill-creation.md`. In short: check the inventory above first — extend an existing
skill rather than forking a near-duplicate. New skills must be technology-neutral unless they
live under `integrations/` or are explicitly a vendor-specific skill, must state narrow
activation conditions, and must include a Validation section.

## Evolving the library

- When a skill is invoked and turns out to be missing a case, extend that skill file directly —
  don't create a parallel skill that half-overlaps it.
- When a skill grows unwieldy (covers two distinct decisions), split it and update the
  dependency chain and inventory table.
- When a skill's guidance is contradicted by a validated project pattern, update the skill —
  skills should reflect the current best practice, not accumulate historical advice.
- Deprecate rather than delete: mark `priority: DEPRECATED` and note the replacement so agents
  that still reference it by name aren't silently broken.
