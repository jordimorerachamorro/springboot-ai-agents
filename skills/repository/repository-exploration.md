---
name: repository-exploration
description: Systematically orient in an unfamiliar Spring Boot repository before making changes.
category: repository
tags: [onboarding, discovery, spring-boot]
priority: CORE
version: 1.0
---

# Repository Exploration

## Purpose
Build an accurate, evidence-based picture of a codebase's structure, stack, and conventions
before proposing or making changes — replacing assumption with observation.

## When to use
- At the start of any task in a repository you haven't worked in during this session.
- Before implementing a feature that might already exist in some form.
- When a task's scope is unclear and needs grounding in what actually exists.

## When NOT to use
- For a repository you've already explored earlier in the same session — reuse that context
  instead of re-scanning from scratch.
- For trivial, fully-specified single-file edits.

## Inputs
- Repository root path.
- The task description, to focus exploration (don't read everything — read what's relevant).

## Process
1. Read build files first: `pom.xml`/`build.gradle` — Java version, Spring Boot version, key
   dependencies (Spring AI? Kafka? Testcontainers? a specific vector store?). This tells you the
   real stack before you guess at it.
2. Read `application.yml`/`.properties` and any profile-specific variants to understand runtime
   configuration and externalized settings.
3. Scan top-level package structure to infer the architectural style in use (layered, hexagonal,
   modular-by-feature) — don't assume; confirm with `architecture-discovery`.
4. Identify existing conventions: naming, exception handling style, DTO/mapper patterns, test
   structure, logging style. New code should match these, not introduce a competing style.
5. Search for existing implementations of adjacent functionality before building new
   abstractions — duplication is a common failure mode of ungrounded agents.
6. Check for CI config, Docker/Compose files, and README/CONTRIBUTING docs for stated practices.
7. Note anything ambiguous or contradictory to flag rather than silently resolve.

## Rules
- Never assume a technology (Spring AI, a specific LLM provider, a specific message broker) is in
  use — verify from the build file and code, every time, for every repository.
- Prefer targeted `grep`/`find` over exhaustively reading every file.
- Read before you write: don't create a class/config/service without first checking one doesn't
  already exist under a different name.

## Anti-patterns
- Proposing an architecture change based on one file's structure.
- Assuming conventions from a previous, unrelated project.
- Skipping this step because the task "sounds simple."

## Validation
- You can name the actual framework versions, key dependencies, and architectural style in use.
- You've confirmed (not assumed) whether similar functionality already exists.

## Related skills
`repository/architecture-discovery.md`, `git-workflow/safe-repository-changes.md`,
`decision-making/architecture-decision-making.md`
