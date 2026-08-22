# AI Playbook

This playbook defines how AI coding tools should be used on this repository so that assistance improves the project without replacing engineering judgment.

## Three AI Usage Rules

1. **Inspect before changing.** AI must read the relevant code, tests, dependencies, and documentation before proposing architecture or behavior changes. Repository evidence is more important than assumptions from an assignment description or prompt.
2. **Verify every meaningful change.** AI-generated code is not accepted because it looks correct. Add or update tests where appropriate, run the available validation commands, and perform a focused manual check for important behavior changes.
3. **Reject unsafe, unverifiable, or out-of-scope output.** Never commit secrets, never fabricate command/test/Docker results, and do not add major features or infrastructure merely because AI suggested them. Keep changes small and consistent with the current Task Tracker architecture unless there is a documented reason to change it.

## Recommended AI Workflow

1. Read `README.md`, `AGENTS.md`, and the relevant implementation files.
2. State the intended change and identify the business rule it affects.
3. Inspect existing tests before editing implementation code.
4. Make the smallest change that solves the verified problem.
5. Add regression coverage for bugs and failure cases.
6. Run pytest and an import/application check.
7. For behavior that is easy to verify manually, perform a direct API check as well.
8. Review the final diff for accidental features, secrets, generated files, and documentation drift.

## Prompting Guidance

Useful prompts should contain the specific repository path, branch, current behavior, desired behavior, constraints, and the validation expected after the change. Avoid prompts such as "rewrite everything" or "make it production ready" because they encourage unnecessary scope expansion.

A good bug-fix prompt is closer to:

> Inspect the task-update model and tests. Explicit `title: null` must return 422, while omitting title in a partial update must remain valid. Make the smallest fix, add a regression test that confirms the stored title is unchanged, then run the test suite.

## Verification Standard

For a code change to be accepted:

- the behavior must match an existing requirement or documented correction;
- relevant automated tests must pass;
- failure cases must be covered when practical;
- documentation must match the actual implementation;
- any environment limitation must be stated instead of hidden.

## Human Review Questions

Before accepting AI output, ask:

- Did the AI inspect the real repository or assume an architecture?
- Is this change required, or is it unnecessary scope expansion?
- Is there a test proving the behavior?
- Could the suggestion weaken validation or security?
- Is any claimed evidence based on a command that was actually run?
- Can a teammate explain and maintain the resulting code?
