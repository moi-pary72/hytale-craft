# Offline JSON importer — contract version1

`scripts/import_catalog.py` is independent of third-party websites. It uses only Python standard library, opens one supplied local JSON file and never makes network requests, extracts game files, changes the website or publishes data. This stage runs it only on original synthetic fixtures.

## Input contract

Exactly six root fields: `schema_version:1`, `snapshot`, `sources`, `items`, `stations`, `recipes`. Original example: `tests/fixtures/catalog-synthetic.json`. That fixture is authored for these tests, CC0-1.0, not a Hytale recipe or station. example.invalid URLs are placeholders, not a real data provider.

| Entity | Required fields |
|---|---|
| snapshot |game_version, channel, source_revision, updated_at (ISO timestamp with timezone) |
| sources[] |id, url (HTTPS without credentials), revision, license |
| source.license |id, url; commercial_use and redistribution each allowed/prohibited/unknown |
| items[] |id (original opaque ID), names (language→text/null), category, status, source_id, source_record |
| stations[] |id, names, status, source_id, source_record |
| recipes[] |id, inputs[], outputs[], stations[] (explicit, possibly empty), status, source_id, source_record |
| input/output |item_id, quantity (positive integer≤999999; bool/string/fraction rejected) |

Original IDs are not translated; names and interface translations are separate. Optional per-record game_version must match snapshot. The date applies to the snapshot; source_record identifies the originating record/path, source_id links to explicit licence/version provenance. Multiple recipes for one output are not deduplicated away. Multiple outputs are preserved with a warning; the current public planner is not declared to support by-products.

Declared states: verified, unverified, tutorial, incomplete, blocked. They describe the input's claims, not an approval by this importer. Incomplete material structure is rejected rather than guessed; a structurally complete row marked incomplete retains that declaration. `declared_state_counts` summarizes all three record collections. Future explicit material groups, metadata semantics, localized-name provenance and station any/all constraints require a reviewed schema extension; no assumptions are made here.

## Command and output

```
python3 scripts/import_catalog.py tests/fixtures/catalog-synthetic.json
```

Default output: ignored `.private/catalog-candidate.json`; report: `.private/catalog-import-report.json`. Both must remain inside project `.private` (symlink/public-output paths rejected). `--expected-sha256 HASH` verifies supplied bytes. `--allow-version-change` explicitly permits replacing a different game_version candidate, retaining a hash-named previous copy. The input file is never overwritten; failing imports leave the prior candidate intact. Reports contain errors/warnings/counts/checksums, not full recipe bodies. Deterministic encoding produces the same candidate hash for identical inputs.

Validation covers schema/version, bounded file/list/material sizes, timezone date, duplicate JSON keys and record/material/station IDs, quantity types, item/source/station references and recipe dependency cycles. Iterative traversal avoids recursion crashes. The graph conservatively joins alternative recipes: a cycle on any possible path blocks automatic acceptance, even if a future recipe-selection policy could avoid it. Limits:10MB input,10000 rows per table,100 terms per material list,256 dependency depth. No guarantee of a globally optimized crafting plan is implied.

Every successful result includes `publication.status=blocked`, `approval_required=true`, input SHA-256, filename and importer version. A source declaring allowed rights or verified status cannot authorize publication automatically. The synthetic fixture contains such declarations only to exercise structure. Rights verification, owner consent and future integration remain separate gates.

## Relationship to existing systems

Current UI/planner/storage and its four labelled learning examples are unchanged. Existing Assets.zip importer remains local-review-only; no licensed archive is used here. Legacy HySphere/OpenHytale network import functions and collection workflow entry points are paused pending permission. Their pure normalization helpers remain solely for synthetic regressions. The historical export_preview.py entry point now delegates to the existing safe educational export_beta.py and cannot embed community snapshots.
