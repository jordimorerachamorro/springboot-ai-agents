---
name: configuration-and-profiles
description: Externalized configuration, Spring profiles, and safe handling of secrets/config across environments.
category: spring
tags: [spring-boot, configuration, profiles, secrets]
priority: HIGH
version: 1.0
---

# Configuration and Profiles

## Purpose
Keep environment-specific values (endpoints, credentials, feature flags, model names) out of code
and correctly scoped per environment, so the same artifact runs correctly across dev/test/prod.

## When to use
- Adding any new externally-configurable value (API keys, base URLs, model identifiers, timeouts,
  feature toggles).
- Introducing environment-specific behavior (e.g. a mock LLM client for tests, a real one in prod).

## When NOT to use
- Values that are true build-time constants, not environment-dependent (e.g. a fixed enum set).

## Inputs
- Existing `application.yml`/`.properties` structure and active profile naming convention.

## Process
1. Bind configuration via `@ConfigurationProperties` classes (typed, validated) rather than
   scattering `@Value("${...}")` across the codebase, once more than a couple of related
   properties exist.
2. Use profiles (`dev`, `test`, `prod`, or the codebase's existing set) to vary implementation,
   not to duplicate entire config trees — override only what differs.
3. Never commit real secrets (API keys, DB passwords) to `application.yml`; use environment
   variables, a secrets manager, or `.env` files excluded from version control — match whatever
   mechanism the codebase already uses.
4. For AI provider configuration specifically: externalize model name, base URL, and timeouts —
   these change far more often than code, and differ between environments (e.g. a smaller/cheaper
   model in dev).
5. Validate configuration at startup (`@Validated` on `@ConfigurationProperties`) so misconfig
   fails fast instead of at first use in production.
6. Use feature flags for functionality that needs to be toggled without a redeploy — but don't
   introduce a flagging framework for a single boolean; a profile-scoped property may suffice.

## Rules
- Secrets never live in source control, ever — no exceptions for "just for now."
- Fail fast on missing required configuration at context startup, not on first request.
- Don't read the same property with `@Value` in ten different places — bind it once.

## Anti-patterns
- Hardcoded API keys or model names in Java source.
- Profile-specific YAML files that duplicate the entire base config instead of overriding deltas.
- Feature flags that are never cleaned up after the feature is fully rolled out.

## Validation
- `grep` for hardcoded secrets/URLs before finishing the change.
- The app fails to start (not fails at request time) if a required property is missing.

## Related skills
`spring/spring-boot-fundamentals.md`, `security/secrets-management.md` (backlog),
`devops/containerization-and-cicd.md`
