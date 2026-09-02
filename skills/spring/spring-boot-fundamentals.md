---
name: spring-boot-fundamentals
description: Core Spring Boot mechanics — DI, bean lifecycle, component scanning, auto-configuration.
category: spring
tags: [spring-boot, dependency-injection, beans]
priority: CORE
version: 1.0
---

# Spring Boot Fundamentals

## Purpose
Apply Spring's dependency injection, bean lifecycle, and auto-configuration model correctly, so
new components integrate cleanly rather than fighting the container.

## When to use
- Adding a new component, service, or configuration class.
- Diagnosing bean wiring issues (`NoSuchBeanDefinitionException`, circular dependencies,
  unexpected bean overrides).
- Deciding how a piece of functionality should be exposed to the container.

## When NOT to use
- Pure business-logic questions with no framework involvement.

## Inputs
- The component's role (stateless service, stateful component, infrastructure adapter).
- Existing bean definition style in the codebase (constructor injection vs. field injection,
  `@Component` vs. `@Bean` in `@Configuration`).

## Process
1. Prefer constructor injection over field/setter injection — it makes dependencies explicit,
   enables `final` fields, and fails fast at context startup if a dependency is missing.
2. Use `@Component`/stereotype annotations for classes you own; use `@Bean` in `@Configuration`
   for third-party classes or when construction needs logic.
3. Default to singleton scope; only reach for `prototype`/`request`/`session` scope with a
   concrete reason (stateful per-request objects).
4. Use `@ConditionalOn*` only when building genuinely optional/pluggable behavior (e.g. a
   starter); don't use conditionals to route normal application logic.
5. For AI-integrated apps, wrap provider SDK clients as beans configured from
   `configuration-and-profiles.md`-style externalized properties, not hardcoded values.
6. Check for circular dependencies by tracing constructor parameters, not just trusting Spring's
   error message — the error location isn't always the root cause.

## Rules
- Constructor injection by default; field injection is an anti-pattern outside of test classes.
- Don't use `@Autowired` on fields in new code unless matching an established codebase convention.
- Keep `@Configuration` classes focused — one area of concern (e.g. `AiClientConfig`,
  `SecurityConfig`), not a catch-all.

## Anti-patterns
- Circular dependencies papered over with `@Lazy` instead of fixing the actual design issue.
- Business logic embedded in `@PostConstruct`/lifecycle callbacks where a plain constructor or
  service method would do.
- Static/global state used to avoid DI.

## Validation
- New beans are constructor-injected and the context starts without warnings about circular
  dependencies or unexpected bean definitions.
- `mvn spring-boot:run` / `./gradlew bootRun` (or equivalent) starts cleanly.

## Related skills
`spring/configuration-and-profiles.md`, `architecture/clean-hexagonal-architecture.md`,
`testing/spring-boot-testing-strategy.md`
