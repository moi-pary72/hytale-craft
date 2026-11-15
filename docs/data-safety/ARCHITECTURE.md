# Independent catalogue architecture

Prepared technical foundation, not a connected real-game database. The input contract is in IMPORTER.md; implementation is offline and isolated from the approved UI.

The canonical model has versioned snapshots, original item/recipe/station IDs, language maps, categories, quantity-bearing inputs/outputs, stations, source references, source-record locators, explicit licence terms and snapshot update dates. Craft chains are graph relationships through original item references, not invented lists. Different builds/channels stay separate; source replacement happens at an adapter, not in card artwork or navigation.

Maintain five explicit declared buckets: verified, unverified, tutorial, incomplete and blocked. Separately record calculation support and publication approval. These axes must never collapse: a structurally valid or source-declared verified record may still be blocked for rights/version/accuracy review. The universal importer always creates a blocked candidate. It has no path from a JSON `allowed` flag to production.

Workflow after separate owner approval: authorized local input → source-specific adapter → private canonical candidate → schema/reference/cycle report → accuracy and rights review → deliberately authorized release snapshot → existing audited public-build boundary. Neither scraping nor OAuth/token use is added. Third-party restricted records are not copied into the new model, including as a hidden fallback. Current public source snapshots remain a separate remediation problem until owner-reviewed merge and any separately authorized history cleanup.

Possible future extensions: confirmed material-group membership, alternative ingredient choices, per-field localization provenance, exact engine inheritance semantics, multiple-output arithmetic and station requirement semantics. They must be based on authorized real-version evidence and tests, not guesses. Current single-output calculator remains unchanged and is tested independently of the new importer.
