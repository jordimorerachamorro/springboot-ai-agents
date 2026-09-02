---
name: bug-investigation
description: Investigate bugs and production issues through evidence — logs, traces, reproduction — not guesswork.
category: debugging
tags: [debugging, root-cause-analysis, incident]
priority: CORE
version: 1.0
---

# Bug Investigation

## Purpose
Find the actual root cause of a defect through evidence, before proposing a fix — a fix based on
a guess risks papering over the symptom while the real cause remains.

## When to use
- Any reported bug, unexpected behavior, or production incident.
- A test is failing and the cause isn't immediately obvious from the failure message alone.

## When NOT to use
- Trivial, self-evident bugs (a clear typo, an obviously wrong constant) don't need the full
  process — fix directly, but still verify the fix addresses the actual reported symptom.

## Inputs
- The reported symptom (exact error, exact steps, exact input) — not a paraphrase.
- Logs/traces from the actual failure if available (see
  `observability/structured-logging-and-tracing.md`).

## Process
1. Reproduce first, if at all possible — a fix for an unreproduced bug is a guess. If it can't be
   reproduced, gather the maximum evidence from logs/traces for the actual failure instance.
2. Read the actual stack trace/error fully — the root cause is often several frames away from
   where the exception was thrown or caught.
3. Form a specific hypothesis about the cause, then look for evidence that would confirm or
   refute it — don't jump to a fix before the hypothesis is evidence-backed.
4. Check recent changes (`git log`/`git blame` on the affected code) if the bug is a regression —
   correlate with when it started occurring.
5. For AI-related bugs: check whether the cause is in your code's handling (parsing, validation)
   or genuinely in model behavior (a prompt eliciting a bad response) — these need different
   fixes; don't assume "the model is just wrong" without checking your own handling first.
6. Once root cause is confirmed, fix the cause, not just the observed symptom — check for other
   places the same root cause might also manifest.
7. Add a regression test that would have caught this bug, where practical.

## Rules
- Never ship a fix for an unreproduced, unexplained bug based purely on a plausible-sounding guess.
- Distinguish symptom from cause explicitly before fixing — state the causal chain.
- A production incident investigation is evidence-based (logs, traces, metrics) — not
  speculation about what "probably" happened.

## Anti-patterns
- Adding a null check or try/catch around a crash without understanding why the null/exception
  occurred — this hides the bug rather than fixing it.
- Fixing the first plausible-looking cause without verifying it against the actual evidence.
- Declaring a bug fixed without a way to verify it (reproduction, test, or log confirmation).

## Validation
- The fix is verified against the original reproduction/evidence — the failure no longer occurs
  for the same input/conditions that caused it.
- A regression test exists (or its absence is explicitly justified) covering this case.

## Related skills
`observability/structured-logging-and-tracing.md`, `testing/spring-boot-testing-strategy.md`,
`ai/evaluation/llm-evaluation.md`
