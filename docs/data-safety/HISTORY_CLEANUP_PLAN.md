# History cleanup — plan only, NOT executed

Deleting files in a new commit changes that branch's current tree only. The prior blobs remain reachable through parent commits, main, other branches, tags, PR refs, cached diffs, forks/clones and possibly Actions/deployment artifacts. A Draft PR is not remediation of those older copies. This PR deliberately does not claim complete erasure.

## Current non-destructive action

Withhold the large HySphere JSON from this branch's tree, neutralize its manifest and the unnecessary OpenHytale bulk catalogue, pause collection/republication entry points and use original synthetic regression fixtures. Original bytes are still in existing Git refs/backups; a local ignored quarantine copy is preserved during review. Private storage is not automatically licensed and is not a legal solution by itself. No tag, backup, artifact, old branch or commit is removed.

## Decisions requiring explicit owner approval

1. Obtain/record source and game rights decisions, including whether public Git retention and redistribution are permitted. Seek legal review of scope where needed. Do not assume all IDs/factual counts are copyrighted or that every factual mention must be purged.
2. Agree the exact removal scope: blob IDs/paths, historic recipe examples, affected refs, artifacts and hosting deployments. Decide retention/access conditions for existing backups; do not erase the only recovery copy or publish an additional disputed backup.
3. Inventory collaborators, forks, PR references, releases, caches and Cloudflare deployment history. Pause relevant automation at the account/default-branch level only with owner approval; changes in an unmerged PR do not disable main's schedules.
4. If the owner explicitly authorizes a coordinated rewrite, use a separate controlled clone and a reviewed git-filter-repo removal specification, dry-run it, compare retained trees and prepare a recovery plan. This document does NOT execute the tool, give permission to force-push, or delete tags.
5. Only after that separate approval decide handling of branch/tag rewrites, protected branches, old PR refs and GitHub support/cache remediation. Request assistance from GitHub if required; a local rewrite cannot erase third-party clones. Communicate recloning instructions before restoring writes.
6. Separately review Actions artifacts and Cloudflare deployment versions. Do not delete backups/artifacts or existing previews under this PR. Dashboard access is required to comprehensively inventory all Cloudflare versions; GitHub check links alone are incomplete.
7. Re-run the ref/artifact/live audit and record residual externally held copies. State remaining limitations rather than claiming complete removal.

For Android: Cloudflare → Workers & Pages → hytale-craft → Deployments lists retained versions. Inspect first; do not click Delete, Retry deployment or Rollback under this task. Main and the existing production site must remain intact until the owner approves a concrete next action.
