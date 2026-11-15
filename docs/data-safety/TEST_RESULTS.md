# PR11 re-review — 2026-11-15

See [PR11_MERGE_REVIEW.md](PR11_MERGE_REVIEW.md). Fresh tests now38Python/17JS/25browser after correcting malformed-existing-candidate error reporting. Previous results below describe the original cee5314 draft and remain historical. No UI/build output changes, merge or deployment.

# Test results — 2026-11-15

Local branch codex/data-safety; baseline a972e4d. No deployment, merge or history rewrite performed.

| Verification | Result |
|---|---|
|Python unit suite|37 passed, including13new offline JSON importer tests |
|JavaScript suites|17 passed:11planner,4preview/localization,2beta |
|Actual Chromium suites|25 passed:legacy1,preview9,public boundary1,art4,beta9,GitHub project path1 |
|Mobile / languages|320/360/393/430px; EN/RU/ES/PT-BR; no horizontal overflow; approved10card layout and two pose sequences preserved |
|Existing mechanisms|Recursive recipes/yields, inventory, leftovers, batch plan, missing/corrupt data, editor, import/export, backup/restore, language reload, Back/Escape/swipe/focus and data persistence passed |
|Importer|Original3item/2recipe/1station JSON accepted; no real disputed dataset used. Output publication blocked; SHA recorded. Negative tests cover duplicate keys/records/materials, references, cycles, quantity types, version changes, malformed/oversize JSON, output restrictions, symlinks and expected-hash mismatch |
|Failure preservation|Prior candidate unchanged on errors; changing game version requires explicit flag and creates hash-named previous copy |
|Build boundary|Both user-only builds reproduce all39prior approved content hashes (40files including manifest). No UI/code/style/art/localization file changed |
|Tracked-tree policy guard|Passed. Exact risky snapshot removed from this branch; neutral pointers/empty catalogue; no private candidate or ZIP tracked |
|GitHub inventory|11branches,2tags,10PR head refs;91reachable commits. Releases empty;46accessible artifacts read locally (ZIP/tar). No full item/recipe JSON snapshot member found; historical HTML/sample/metadata caveats recorded |
|Physical Android|Unavailable; mobile Chromium emulation only. Existing owner's browser/localStorage not touched |

An initial legacy browser test exposed one leftover real-game search string after synthetic fixture conversion. It was corrected to Fixture_Product; then all suites passed. No production code change was needed. Existing tests were not dropped; third-party-bound assertions now use clearly synthetic fixtures with the same calculation/error paths.

The baseline approved UI build comparison checks bytes, not merely screenshot similarity. New synthetic data is intercepted only inside legacy browser tests; it is not served by the public builder. Old export_preview now emits the existing standalone educational beta, verified with one HTML request and a working calculation.

Final Draft PR URL, exact CI head and Cloudflare skip verification are recorded in the PR description and the existing Google Drive passport after creation. A draft does not change main's existing schedules or erase historical copies. Snapshot/backups/artifacts were not deleted server-side. No claimed legal approval follows from tests passing.
