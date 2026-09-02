---
name: code-review
description: Review code changes for correctness, design fit, test coverage, and unnecessary complexity.
category: quality
tags: [code-review, quality, maintainability]
priority: CORE
version: 1.0
---

# Code Review

## Purpose
Catch correctness bugs, design mismatches, and unnecessary complexity before a change ships —
whether reviewing your own change before finishing a task, or reviewing another change.

## When to use
- Before declaring any non-trivial task complete — self-review the diff.
- When explicitly asked to review a PR/branch/diff.

## When NOT to use
- Don't use this for reviewing skill files themselves — use `meta/skill-review.md`.

## Inputs
- The diff/changeset, and the context of what problem it's meant to solve.
- Output of `repository/architecture-discovery.md` for whether the change fits existing patterns.

## Process
1. Correctness first: does the change do what it claims, including edge cases (empty input,
   null, concurrent access, partial failure)? For AI-integrated code, does it handle malformed/
   unexpected model output (see `testing/llm-testing-strategies.md`)?
2. Check it fits existing conventions and architecture rather than introducing a parallel style
   or reinventing something that already exists elsewhere in the codebase.
3. Check test coverage matches the actual risk of the change — new logic has tests, changed logic
   has updated tests, and failure paths are covered, not just the happy path.
4. Look for unnecessary complexity: added abstractions with no current second use case,
   speculative generality, error handling for scenarios that can't occur. Flag it.
5. Check security-sensitive surfaces explicitly: input validation, authz, injection risk, SSRF
   risk, secrets handling (see `security/api-security.md`).
6. For AI-related changes: check prompts/tool schemas are validated, provider calls have
   timeouts/error handling, and structured output is validated before use, not trusted blindly.
7. Check observability: does a failure in this new code path produce enough log/trace signal to
   diagnose without a debugger (see `observability/structured-logging-and-tracing.md`)?

## Rules
- Don't approve/finish a change with unhandled edge cases in the primary flow, even if "unlikely."
- Flag unnecessary abstraction and scope creep as seriously as you'd flag a bug — both cost the
  codebase long-term.
- A change without tests for new behavior is incomplete, not merely "could be improved."

## Anti-patterns
- Reviewing only the diff's additions and missing what it should have changed but didn't (e.g. a
  related doc, a sibling test).
- Nitpicking style while missing a correctness or security issue.
- Rubber-stamping AI-generated code without checking it against real project conventions.

## Validation
- Every finding is concrete: file, line, the specific failure scenario — not a vague "consider
  improving X."
- You've verified the change against the actual current state of the file, not an assumption.

## Related skills
`testing/spring-boot-testing-strategy.md`, `security/api-security.md`,
`quality/refactoring-and-technical-debt.md` (backlog), `git-workflow/safe-repository-changes.md`
