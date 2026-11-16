# Real Data Lab — 16 November 2026

Research candidate only. Based on Draft PR16; no main change, merge or deployment. No source dump, derived catalogue or game artwork is included in Git or public CI artifacts. The existing Seeker/Maker design and production storage keys are unchanged.

## Sources and access

| Source | Checked evidence | Actual scope / revision | Decision |
|---|---|---|---|
| [HySphere exports](https://hysphere.app/data) | [manifest](https://hysphere.app/data/v1/manifest.json), [README](https://hysphere.app/data/v1/README.md), [terms](https://hysphere.app/about#data-license), [robots](https://hysphere.app/robots.txt) | 3,219 items; 2,109 recipe rows (1,706 craft +403 salvage), extracted 2026-08-12T11:09:57.625Z; Early Access, exact game build unknown | Documented allowlisted /data export, personal/educational noncommercial attribution. /api is disallowed and was not used. Private technical research only; no commercial clearance or general redistribution permission inferred. Underlying game IP remains with the studio. |
| [OpenHytale metadata](https://openhytale.org/api/meta.json), [counts](https://openhytale.org/api/catalogs.json) | Small metadata responses only | 3,641 item IDs,403 recipe IDs; generated2026-07-06T11:57:22.295504Z | ID counts are not full recipes. No full dump fetched or merged with August data; commercial data licence unconfirmed. |
| [Hytale recipe documentation](https://docs.hytale.com/assets/item/recipes/) | Schema reference reachable | Not a complete vanilla recipe export | Existing resource importer retained. Owner has no licensed Assets.zip; no archive, account bypass or asset download attempted. |

Previous source investigations were reused. This is a bounded practical extraction/QA pass, not a claim to have searched all sources anew. HTTP availability is not proof of licensing. No external enquiry sent; the owner's studio request remains pending.

### Reproducibility and source quality

The freshly downloaded raw SHA-256 values match the earlier project snapshot:

- manifest: `12709143ba45909056aa7fc7ce782d15c5a78a41165b5dd0d42234e4b918bc6c`
- items: `2ca40b7ec9ea78869cabdac579c3787c40a9728b0f492e88d3629f42dea7ad59`
- recipes: `d007c9f482198d6353acba43af9142736bcc0f446235b60f418a01e9f208d09e`

These are source-backed dated records, not independently verified current game facts. **638 supported material recipes =623 previous single-output +15 multi-output**. An initial structural count642 also included4 TODO-station rows; these4 are quarantined. Thus the extra19 rows are NOT19 usable multi-output recipes.

**1,471 rows remain quarantined**, including all403 salvage records.393 salvage rows repeat output IDs; no guessed summation or deduplication is performed. Many craft inputs contain only quantities with no item/group selector. Missing selectors, references, quantities and station identifiers are never invented.1,100 item production paths remain blocked/incomplete.17station IDs are preserved; unknown tiers, relationships and unlock conditions remain unknown. One target has alternative supported methods. Unsupported group data cannot be recovered from absent source fields.

## Working private build

The offline builder reuses existing source-contract checks, canonical-v2 validation and engines. It preserves original IDs, English names, source revision, hashes, unresolved metadata and separate technical/rights flags. No automatic network collector is enabled. Missing translations are not fabricated. This dedicated research viewer is English-only; the existing four-language production UI is untouched.

```sh
python3 scripts/build_real_data_lab.py .private/real-data-lab --output .private/real-data-lab/research-build --local-research-only
python3 scripts/serve_real_data_lab.py .private/real-data-lab/research-build --port 8765
```

Use a new output directory if it already exists. Input must be a lawfully obtained manifest/items/recipes export in the ignored private directory. The acknowledgement is not a licence. Existing raw/historical snapshots are not overwritten. The complete local viewer is at `.private/real-data-lab/research-build`; detailed arithmetic and screenshots stay under `.private/real-data-lab`.

Server binds127.0.0.1, rejects external Host/Origin, directory listing and symlinks; browser refuses nonloopback hosts. SHA-256 is checked before rendering. No analytics, third-party scripts or downloaded item images. Noindex is not access control: do not tunnel, upload or serve this directory publicly. This is not a phone-accessible HTTPS preview; use the trusted workspace browser or reproduce locally with authorized inputs.

## Visual and functional result

Existing original logo, fantasy workshop/background scenes, metallic frames, palette and deep panels are reused. Two-column item/inventory cards, mobile sheet, nested craft path, co-products, used-in, station badges and material panels replace database tables. Category scenes are explicitly category illustrations, NOT official item thumbnails. Accurate item-specific illustrations remain unavailable without rights.

100/1,000/3,219-item catalogue samples retain the full dependency snapshot; search is indexed and only24cards or inventory slots are rendered per page. Inventory supports quick +/- and all3,219 entries, isolated local persistence. Shared multi-goal plans preserve stock and show missing amounts and leftovers. What Can I Craft checks paginated candidates with independent maxima, distinguishes direct/intermediate production, and warns independent results cannot be summed as one simultaneous plan. Add-to-plan performs a shared check.

Cycles are blocked by default. Some real recipes create materials participating in recycling loops. A player may **explicitly select external inputs** to stop expanding selected materials; no acquisition method is inferred. This is not an automatic cycle solver or global optimization algorithm. Target stock is reserved for newly requested copies; seeded recycling capacity is conservative. Station/knowledge eligibility is never silently promised: material-only estimates are labelled; strict unknown requirements block.

## Actual verification

[Aggregate machine evidence](AGGREGATE_QA.json) contains counts/timing only. Detailed real rows/formulas remain private.

-354 independent legacy/canonical arithmetic comparisons (quantity3, partial inventory, leftovers):0 mismatches.131 complete source paths;223 incomplete paths labelled partial.183 cycles blocked;86 cases skipped because method coverage differs.
- With explicit external cut selections:620 comparisons matched,0 remaining cycles in that selection; deepest checked production uses8 distinct craft steps. This is not a claim of8 tree levels or every possible route.
-15 actual multi-output batches,150 real station-level checks, one alternative-method target and a3-goal shared plan checked. No official in-game verification.
- Mobile Chromium320/360/393/430: search,100/1000/full samples, direct card/detail, calculation, inventory, plan, disclosure, incomplete paths, cycle blocking, strict requirements, Back/Escape and persistence.0 JavaScript errors and no horizontal overflow. Physical Android not available.
- About2.10MB decoded JSON (~113KB gzip). Initial measured readiness0.43–0.70s unthrottled;3.214s at150ms latency,150KB/s download and4x CPU slowdown. These are desktop emulation measurements, not universal phone guarantees. Candidate discovery is chunked/paginated; not an exhaustive global optimiser.
- Synthetic CI covers loader corruption, private/public boundaries, external Host/Origin, compatibility, persistence and original engine mechanics. Public build audit:0community snapshots,0internal files;4classic+4advanced original learning methods only. Real-data harness is opt-in locally and is not run or uploaded in public CI.

## Publication boundary

**May publish:** own code, synthetic fixtures, original artwork, aggregate counts/hashes, source links and this report. Public Draft PR contains only these.

**Do not publish:** raw exports, normalized real bundle, private build or detailed formula reports; no full data backup to public GitHub/Cloudflare/Drive archives. Underlying game assets were not downloaded. Limited attributed UI review screenshots may be kept in the existing verified owner-only Drive artifact folder as private noncommercial citation, not a commercial dataset licence. No sharing settings are changed.

Commercial use, unrestricted mirroring, exact current build and missing group/salvage semantics remain unresolved. The fastest next step is a source-owner clarification/complete export with selectors and precise build, alongside the studio reply already pending; alternatively an authorized licensed archive with the necessary reuse rights. The project is technically useful for real-source research now, but the supported638 are not permission to publish a commercial game catalogue.
