---
name: containerization-and-cicd
description: Containerize a Spring Boot app and structure CI/CD pipelines for build, test, and safe deployment.
category: devops
tags: [docker, cicd, devops, github-actions]
priority: HIGH
version: 1.0
---

# Containerization and CI/CD

## Purpose
Package and ship the application in a way that's reproducible, secure, and fast to build/deploy,
with CI enforcing the quality gates the rest of this library assumes exist.

## When to use
- Adding/modifying a `Dockerfile`, Compose file, or CI pipeline definition.
- A change needs a new environment variable, secret, or build step reflected in CI/deployment config.

## When NOT to use
- Local-only development scripts with no bearing on the built artifact or pipeline.

## Inputs
- Existing `Dockerfile`/multi-stage build setup, CI provider (GitHub Actions, etc.), deployment
  target conventions.

## Process
1. Use multi-stage Docker builds: build stage with the full JDK/build tool, runtime stage with
   only a JRE and the built artifact — smaller image, smaller attack surface.
2. Don't run the container as root; use a non-root user in the runtime stage.
3. Externalize all environment-specific config via env vars/secrets (see
   `spring/configuration-and-profiles.md`) — never bake secrets or environment-specific values
   into the image.
4. CI pipeline stages should mirror the quality bar: build → unit tests → integration tests
   (Testcontainers needs Docker-in-CI) → static analysis/lint → build image → (optionally)
   security/dependency scan → deploy. Fail fast on the cheapest checks first.
5. Pin dependency versions (build tool, base images) deliberately; don't float on `latest` for
   anything that ships to production.
6. Configure health/readiness probes (`/actuator/health`) so orchestrators can make correct
   traffic and restart decisions — verify liveness vs. readiness semantics aren't conflated.

## Rules
- Secrets are injected at deploy/runtime, never baked into the image or committed to the
  pipeline config in plaintext.
- CI must run the same test suite locally reproducible developers would run — no
  CI-only-passing, unreproducible steps.
- Base images and runtime dependencies are pinned, not `latest`.

## Anti-patterns
- Running the application container as root.
- A single-stage Docker build that ships build tools and source into the runtime image.
- CI that only builds but doesn't run tests before "passing."

## Validation
- Image builds successfully and runs with a non-root user — verify, don't assume.
- `/actuator/health` (or equivalent) reflects real readiness, not just "process is up."

## Related skills
`spring/configuration-and-profiles.md`, `testing/testcontainers-integration-testing.md`,
`security/api-security.md`
