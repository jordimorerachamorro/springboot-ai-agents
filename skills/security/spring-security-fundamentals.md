---
name: spring-security-fundamentals
description: Apply Spring Security's filter chain, authentication, and authorization model correctly.
category: security
tags: [spring-security, authentication, authorization]
priority: CORE
version: 1.0
---

# Spring Security Fundamentals

## Purpose
Secure endpoints and method calls with correct authentication/authorization, matching the
codebase's existing security model rather than introducing a parallel one.

## When to use
- Adding a new endpoint that needs access control.
- Reviewing whether existing security configuration correctly protects a resource.

## When NOT to use
- Purely internal, non-network-exposed code paths that don't cross a trust boundary.

## Inputs
- Existing `SecurityFilterChain`/`WebSecurityConfigurerAdapter`-successor configuration.
- Authentication mechanism in use (session, JWT, OAuth2/OIDC) — verify, don't assume.

## Process
1. Identify the existing security configuration's default posture (deny-by-default vs.
   permit-by-default) and match it — new endpoints should be explicit either way.
2. Prefer method-level security (`@PreAuthorize`) for fine-grained, role/permission-specific
   checks close to the business logic, and URL-based rules in the filter chain for broad,
   structural access control.
3. Never implement custom authentication/crypto logic (password hashing, token verification) —
   use Spring Security's built-in mechanisms and vetted libraries.
4. For AI-backed endpoints, apply the same authz as any other endpoint — an LLM call is not a
   security boundary; access control happens before the call, not by relying on prompt content.
5. Ensure CORS and CSRF configuration matches the API's actual consumption pattern (browser
   session-based clients need CSRF protection; stateless token-based APIs typically disable CSRF
   but need careful CORS).

## Rules
- Deny by default; explicitly allow, not the reverse.
- Never write custom cryptography or token validation — use the framework/library primitives.
- Authorization decisions happen server-side, never trusting client-supplied role/permission claims
  without verification.

## Anti-patterns
- Security checks duplicated ad-hoc in controller methods instead of centralized configuration.
- Disabling CSRF/CORS broadly "to make it work" without understanding the actual trust model.
- Relying on an LLM's response to gate access control decisions.

## Validation
- A request without required authentication/authorization is rejected — verify with an actual
  unauthenticated/under-privileged request, not just reading the config.
- New endpoints are covered by the existing security integration tests, or new ones are added.

## Related skills
`security/api-security.md`, `api/rest-api-design.md`, `ai/security/ai-security.md`
