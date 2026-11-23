# Hytale Craft — Codex and ChatGPT team instructions

Read the current README and repository-specific test/deployment workflows first. Work only in this repo; never modify other projects.

## GitHub Actions efficiency — owner directive 2026-11-23
- For every task, group development work locally, perform focused smoke/tests before pushing, and open one coherent PR for the final CI gate.
- Do not run full browser/Playwright pipelines on every speculative small edit, create empty CI-trigger commits or rerun identical failed Actions without code changes. Inspect logs, batch fixes, then push once.
- Do not silently loosen required validation, delete source checks or disable official-source monitoring to optimize cost. Preserve scheduled data refresh and real user-facing behavior; changes to schedules must be individually justified.
- This is a PUBLIC GitHub repository: standard hosted CI is generally free to the account owner. Savings here protect CI efficiency rather than necessarily reducing the personal private-repo quota.
- Never claim a successful CI run proves real user-device behavior. Report PR, exact HEAD SHA, test status and unverified browser/device checks.
- Every new Codex or ChatGPT worker should load this file and the current project docs before starting.
