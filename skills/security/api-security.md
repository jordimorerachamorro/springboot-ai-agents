---
name: api-security
description: Apply OWASP API security practices — input validation, injection prevention, SSRF, output encoding.
category: security
tags: [security, owasp, api, injection, ssrf]
priority: HIGH
version: 1.0
---

# API Security

## Purpose
Prevent the OWASP-class vulnerabilities most common in backend APIs: injection, SSRF, broken
object-level authorization, and sensitive data exposure.

## When to use
- Any endpoint accepting user input, especially input that flows into a query, external call, or
  file path.
- Endpoints that accept a URL or identifier used to fetch a resource (SSRF risk).
- Reviewing code for security issues (also see `quality/code-review.md`).

## When NOT to use
- N/A — some subset of this skill applies to nearly every API-facing change; scope which specific
  checks apply to the change at hand rather than skipping the skill entirely.

## Inputs
- The specific input surface being added/modified and where that data flows next.

## Process
1. Use parameterized queries/JPA criteria — never string-concatenate user input into SQL/JPQL.
2. Validate and canonicalize any user-supplied identifier used for object lookup, and check
   authorization on the specific object (not just that the caller is authenticated) — prevents
   broken object-level authorization (BOLA/IDOR).
3. For any server-side request that includes a user-influenced URL or host (webhooks, fetch-by-URL
   features, and notably LLM tool calls that fetch external resources), validate against an
   allowlist and block internal/private IP ranges — this is the SSRF risk, and it's a live concern
   for AI agents with tool access to HTTP fetch.
4. Encode output appropriately for its context (HTML-escape for web rendering) to prevent XSS,
   even in API responses that might be rendered client-side without their own escaping.
5. Don't include sensitive fields (password hashes, internal IDs meant to stay internal, full
   stack traces) in API responses or logs.
6. Rate-limit endpoints that are expensive or abusable (including any LLM-backed endpoint, which
   is also a cost-control concern — see `ai/cost/ai-cost-management.md`).

## Rules
- Never build a query, shell command, or file path via string concatenation with user input.
- Any feature that lets the server fetch a user-supplied URL needs SSRF protection — no exceptions
  for "internal tool" or "admin-only" features, since those still cross a trust boundary.
- Object-level authorization is checked per-request, per-object — not inferred from role alone.

## Anti-patterns
- Trusting a client-supplied object ID without verifying the caller owns/can access it.
- A "fetch URL and summarize" AI tool with no host allowlist.
- Logging full request bodies that may contain PII or secrets.

## Validation
- Parameterized queries used throughout — `grep` for string concatenation near query construction.
- A test attempts to access another user's resource by ID and is rejected.
- Any URL-fetching capability rejects internal/private-range targets.

## Related skills
`security/spring-security-fundamentals.md`, `ai/security/ai-security.md`,
`ai/agents/tool-design.md`
