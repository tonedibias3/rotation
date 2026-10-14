# Progress (updated Oct 14, 2026)
Plan: Stage 1 done. Own-photos-only decision made and built. Stage 2 (App Store) waits on Xcode space (USB-A to C adapter + external drive, or M3 Mac).
Outputs: app/index.html (Get started checklist, Share this fit, Send feedback, backup nudge, Quick add many photos, Google photo search removed), scripts/check.js (8 checks), scripts/e2e.py (28 headless checks), privacy.html (photo-search section removed).
Decisions: feedback = email only, no tracking. Own photos only; Google/online photo search removed (Tone, Oct 14). Fully flesh out the app before the App Store push; no rush.
Open issues:
- Backup export uses a browser download (a[download]); likely does nothing inside the iOS wrapper. Needs Capacitor Filesystem + Share before TestFlight.
- No background removal on photos; Quick add fits each photo on a white square. Real background removal needs an on-device model (heavy) - decide later.
- Export/import round trip tested for closet pieces; logged days and looks not covered by e2e yet.
- Real new-user timing (first logged outfit under 60s) still unmeasured; needs watching 3-5 real people.
Cleanup Oct 14: removed dead cloud-sync/asset-upload code (window.claude, ASSETS, store flags), unused constants and a dead helper; app/index.html 195 KB -> 192 KB, 2454 -> ~2390 lines. Audit found no unused CSS, icons, keyframes, TODOs or console logs.
Next action: Tone picks the next batch (ideas: photo cleanup/auto-trim, share card polish, calendar/stats depth, iOS-native export).
