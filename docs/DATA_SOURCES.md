# Hytale Craft — source synchronization policy

- Site repository: `moi-pary72/hytale-craft` (never modify `moi-pary72/moi-pary`).
- Primary discovery: OpenHytale JSON API (meta + catalog index).
- Independent fallback/checks: Hytale Source and HytaleDB.
- Automatic check: twice daily UTC, plus on workflow changes; manual dispatch available.
- Diagnostics: workflow artifact `hytale-source-health`, retained 30 days.
- IMPORTANT: Current monitor **does not** import or publish recipes. Source HTML and JSON are inspected only.
- Recipe promotion requires documented endpoint, explicit item IDs, positive quantities, complete outputs, supported resource/tag references, and matching game build.
- Never merge different game versions silently; report source/version and disagreements.
- If a source fails or is outdated, keep last verified production snapshot.
- Next milestone: identify a complete, machine-readable recipe dataset, implement version-aware normalization, validate representative recipes, then connect the UI.
