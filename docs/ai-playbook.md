# AI Playbook

This is my personal playbook for using AI on this Task Tracker. The goal is to use AI where it speeds up engineering work while keeping repository evidence, deterministic verification, and human judgment in control.

## When I reach for AI first

I reach for AI first when the task benefits from fast inspection, comparison, or drafting but still has a clear way to verify the result. Examples in this project include reviewing a diff for likely edge cases, proposing regression tests for an already identified bug, checking documentation against the actual repository structure, and drafting a small CI or Docker change from explicit requirements.

I also use AI early when I need to turn evaluator feedback into a concrete checklist. For example, after the null-title issue was reported, a useful prompt was:

> Inspect the task-update model and tests. Explicit `title: null` must return 422, while omitting title in a partial update must remain valid. Make the smallest fix, add a regression test that confirms the stored title is unchanged, then run the test suite.

## When I do not reach for AI first

I do not reach for AI first when a deterministic tool or the repository itself can answer the question more reliably. I inspect source code for the real architecture, use pytest to decide whether tests pass, use Git/Docker/runtime commands for execution evidence, and inspect configuration files directly for secrets or tracked artifacts.

I also avoid asking AI to make the final decision on high-impact or irreversible actions. AI can suggest a change, but I should understand the business rule, review the diff, and verify the behavior before accepting it.

## My non-negotiables

- Never claim a test, Docker build, container run, health check, or command passed unless it actually ran successfully.
- Never commit real secrets, `.env` files, tokens, passwords, credentials, private keys, production logs, or personal/customer data.
- Never accept an architectural rewrite only because AI proposed it; first inspect what the repository actually implements.
- Preserve existing intended functionality and make the smallest justified change for a verified problem.
- Add or update tests for behavior changes and important failure cases.
- Keep code understandable enough that I can explain it during evaluation.

## My review rules

Before I accept AI-generated or AI-assisted code, I check:

1. **Repository fit:** Does the suggestion match the actual FastAPI/Pydantic/in-memory architecture?
2. **Requirement fit:** Is the change required by the project or evaluator feedback, rather than unnecessary scope expansion?
3. **Behavior:** Does it preserve existing routes, response shapes, and business rules unless a documented requirement says otherwise?
4. **Failure cases:** Is there regression coverage for the bug or risky edge case?
5. **Execution:** Did pytest and any relevant runtime checks actually execute successfully?
6. **Security:** Does the change introduce secrets, unsafe configuration, weakened validation, or unnecessary exposure?
7. **Documentation:** Do README and required evidence files describe what the repository really does?
8. **Explainability:** Can I explain why the change exists and how it was verified?

## What I am still figuring out

I am still improving how I decide the right amount of AI assistance for a task: enough to speed up review and implementation, but not so much that I lose understanding of the code. I also want more experience distinguishing useful AI review findings from plausible-sounding noise, especially around security and architecture. Another area I am still learning is how to design stronger CI evidence without making a small learning project unnecessarily complicated. Finally, I want to become faster at turning AI suggestions into focused, deterministic tests instead of relying on the suggestion itself as proof.

## Decision Card

I use this card before accepting a meaningful AI-assisted change.

| Question | Decision for this final project |
| --- | --- |
| **What problem am I solving?** | Make the existing Task Tracker submission satisfy exact course requirements and fix verified defects without adding unrelated features. |
| **Why use AI here?** | AI is useful for repository review, identifying edge cases, drafting focused fixes/tests, and checking documentation completeness. |
| **What evidence do I inspect myself?** | Actual source files, `AGENTS.md`, evaluator feedback, tests, Git diff/tree, security-sensitive configuration, Docker build/run output, and `/health` response. |
| **What will I not delegate to AI?** | Deciding whether tests passed, inventing runtime evidence, approving secrets/security risks, or making unexplained architectural rewrites. |
| **What is the smallest acceptable change?** | A focused change that addresses the verified requirement or bug while preserving existing behavior. |
| **How will I verify it?** | Relevant regression tests, full pytest run, import check, manual API checks when appropriate, and actual Docker build/run plus HTTP 200 health verification for the container requirement. |
| **What would make me reject the AI output?** | It conflicts with repository evidence, expands scope without need, weakens validation/security, cannot be tested, fabricates evidence, or is too complicated to explain. |
| **Who owns the final decision?** | I do; AI provides assistance, but I review and accept or reject the final change. |

### Decision Card template

For future changes, I can reuse this shorter version:

- **Problem:** What exact requirement or defect am I addressing?
- **AI role:** What do I want AI to help with?
- **Evidence:** What source, test, or runtime output will I inspect myself?
- **Non-delegated decision:** What must remain human/deterministic?
- **Smallest change:** What is the minimum justified edit?
- **Verification:** What commands/tests/manual checks must pass?
- **Reject if:** What would make the AI output unacceptable?
- **Owner:** Who makes the final call? Me.
