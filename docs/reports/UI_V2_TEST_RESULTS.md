# Hytale Craft 2.0 — verified local QA, 2026-11-14

Baseline main232b9c4f1da592e415245d0144c1d7acb1e7b845; single codex/ui-v2 branch. Physical Android was not available. The owner authorized merge/publication after these checks plus green GitHub CI; live deployment verification must follow merge, not be inferred from these local results. The single PR and appended Drive passport hold exact CI/head/merge/live evidence.

| Check | Actual result |
|---|---|
| Python unit tests | 23 passed; includes new artwork corruption rejection / exact published asset set |
| JavaScript tests | 17 passed (11 planner,4 preview,2 beta): quantities, recursive yields/shared inventory, cycles, locale key completeness, educational provenance |
| Actual Chromium browser suites | 25 passed: legacy1, preview9, publication boundary1, art review4, beta9, GitHub project-path1 |
| Mobile sizes / languages | 320/360/393/430px; EN/RU/ES/PT-BR, all10 goals, two columns, no horizontal overflow |
| New UI tests | All10 full scenes decode; original brand; native modal's own navigation operates inventory→plan→home; saved inventory unchanged after reload |
| Existing behavior | Quantity calculation, inventory deficits, nested craft yields, plan persistence, editor/import/export/full backup, cycles, malformed user data retained, no game-data requests |
| Navigation/accessibility | Back item→list→home, close, handle swipe, Escape, Tab stays in dialog, focus return and scroll position retained; native modal keeps background inert |
| Failure handling | Invalid/missing examples and malformed locale JSON; storage quota failure; all artwork404 leaves ten labelled functional buttons, no fake glyph illustrations |
| Standalone export | One HTML request only; scenes/background/logo/frame/icons embedded; calculate works |
| Animations | Existing fight/gather pose atlases load on demand, one-shot action, repeated selection bypasses wait; reduced-motion/Save-Data safeguards retained; other8 are still illustrations |
| Performance sample | Final local run: 4.339s ready under4× CPU slowdown,150ms latency,150,000B/s downstream. This includes test-forced decoding of all10 scenes, beyond normal first viewport lazy loading. Timing is environment-specific, not a Lighthouse score. |
| Public build | 40 files /913,528 bytes;39 SHA-256 content entries. Includes both desktop/mobile backgrounds and both on-demand pose atlases; not initial network payload. Exact source-art checks; deterministic repeated build. |
| Restricted content |0 community snapshots,0 real game recipes,4 clearly labelled original learning examples. No internal docs/tests/archives/masters, ads or application analytics. Noindex preserved. |

Fresh screenshots: local `.private/ui-v2/home-ru-393.png`, `home-ru-1170.png`, `sheet-ru-393.png`; existing beta suite also records four Russian mobile widths. They are uploaded to the existing Drive artifacts folder and CI stores mobile screenshot/metrics artifacts. Exact attachment bytes were not available for a pixel-difference test; a visual comparison with the visible owner attachment was performed. Own artwork intentionally differs in scene details while following its composition/material/lighting direction. Reference's untrue “full guide” subtitle is not reproduced.

First pass corrected: cropped-away castles caused by background-cover; tight caption spacing; updated missing-art coverage when expanding from2 to10 scenes. No calculator or browser storage key changes. Native Android Back/IME/TalkBack and a human review on a real low-end phone remain follow-ups. No claim of ten fully animated characters or commercially licensed Hytale database.

Rollback source tag: backup/pre-ui-v2-20261114 →232b9c4. CI must be checked again on the actual PR head before normal merge; no force/main reset. Post-merge checks compare every served manifest asset and test both real HTTPS hosts. Drive preserves PNG masters, changed code and previous-main ZIP with local SHA-256; upload verification checks returned file ID/name/size/parent. Remote checksum is not claimed unless the connector returns it.
