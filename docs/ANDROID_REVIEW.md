# Owner mobile review — Stage4

No hosted preview was deployed. The standalone `hytale-craft-stage4-mobile.html` in the existing Drive artifacts folder is an owner-review file, including the restricted noncommercial snapshot; do not redistribute it as a commercially cleared database.

1. Download the HTML from the Stage4 Drive link; Drive's built-in HTML viewer may show source instead of running JavaScript.
2. Try opening the downloaded file with Chrome on Android. File-viewer policies differ. If scripts are blocked or the app cannot open it, report the exact behavior; this stage did not test a physical Android and does not claim this path always works. Do not disable browser security settings.
3. Check EN/RU/ES/PT-BR; choose Fight → weapons → Crude Shortbow, quantity2; add inventory `Ingredient_Stick: 3`, calculate, add to plan and reload. Item ID and English source names intentionally remain English.
4. Verify two columns, all ten buttons, large targets, readable labels and no side scrolling. Explore/enemy/skills guidance explicitly remains planned where data are absent.
5. Try a clearly marked custom recipe, export it and reload. Downloaded-file storage is separate from GitHub Pages/any future Pages hostname. Current JSON export covers recipes only; manually preserve inventory and plans before changing origins.

Screenshots for widths320/360/393/430 are stored alongside the file and do not require JavaScript. They show the approved-direction SVG prototypes, not final rendered artwork. See the Stage4 Drive manifest for exact artifact URLs, bytes, local SHA-256 and source commit.

For a developer's local HTTP review after checking out PR4:

```
python3 scripts/build_pages.py
python3 -m http.server 8000 --directory dist
```

This serves the safer user-only packaging on the developer machine, not a public URL. Full-data review: source `preview.html` through a local repository server, or the explicit noncommercial-review build mode with the same rights limits. Do not expose the repository-root server publicly. An actual Cloudflare preview requires a separate owner publishing decision.
