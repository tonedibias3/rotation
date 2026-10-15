# Quality brief: a deeper Rotation, not a bigger one (Oct 15)

Method: Tone's prompt of four questions, applied to the app. Re-run this before each release.

## 1. What a top professional would do that Tone has not asked for
- Treat first-run as the product: watch real people, time them, fix the first 60 seconds before adding features.
- Make the app work with no network and no third parties, so the privacy promise is literally true.
- Test on the real device (iPad/iPhone Safari and the Capacitor build), not just a desktop browser.
- Protect user data from the platform: backup reminders matched to how the browser can delete data.
- Accessibility and touch size as a release gate (44 pt targets, WCAG AA contrast, labelled controls).
- A written release checklist and a regression test that runs on every change.

## 2. Rawest material to start from (not opinions)
- Real usage: screen recordings of 3-5 people (not friends who already know the app) doing: add 5 pieces, log today, share.
- The user's own export file (real photos, real wear history) as the stress dataset.
- Automated measurements run on Oct 15: axe-core accessibility scan on every tab, 300-piece/200-day load test, offline reload test, network request log, tap-target sizes.
- Real devices: iPad (Tone has it), iPhone, one Android phone from a tester.

## 3. Methods and tools
- axe-core (WCAG 2 A/AA) via Playwright; Playwright e2e (scripts/e2e.py, 28 checks); scripts/check.js (9 checks).
- Stress: seed 300 pieces + 200 days, measure reload and render time.
- Offline: install service worker, reload with network off.
- Real-device pass using the checklist below; TestFlight for iOS once the Mac exists.
- Still to add: HEIC and very large photo imports, timezone/DST day-boundary test, Dynamic Type / large text, VoiceOver pass.

## 4. What outside of Claude and Tone proves it is right
- A stranger completes first-run unaided in under 60 seconds (watched, timed).
- Zero axe violations; zero requests to any host not in the allowlist; app loads offline.
- Data round trip: export on device A, import on device B, identical.
- Apple review passes (guideline 4.2 needs the native value-adds in plan step 6).
- Retention: beta testers still logging a week later (ask them; there is no tracking by design).

## Results of the Oct 15 audit
Good: 300 pieces and 200 days load in about 0.7 s, render in 15 ms; 28/28 e2e; no page errors; storage persist requested.
Fixed in this pass:
- Fonts loaded from Google at runtime (a privacy contradiction and a broken look offline in the iOS app). Now bundled in app/fonts; check.js fails if Google Fonts returns.
- No offline support on the web version. Added app/sw.js (page network-first, fonts/icons cached).
- 6 unlabelled file inputs (critical accessibility), low-contrast inactive buttons and "optional" text, touch targets under 40 px (chips, Pieces/Looks/Wall switch, See all, links).
- Backup reminder for browser-tab users now 5 days (Safari can clear unused site data after 7); installed/App Store users stay at 14.
Not fixed, needs Tone or a device:
- Watch 3-5 real first-run sessions (nothing automated replaces this).
- iPad Photos-picker blank preview and before/after-save differences (screens e and f): need Tone's notes.
- Landing page (index.html at repo root, and rotation-site) still loads Google Fonts; fix when the analytics decision is made.
- HEIC/huge photo test, VoiceOver pass, large-text test.

## Release checklist (run before every App Store build)
1. node scripts/check.js and python3 scripts/e2e.py all pass.
2. Fresh install on a real iPhone: first outfit shared in under 60 s.
3. Airplane mode: open, log, share, export all work.
4. Export, wipe, import: identical closet.
5. Dark mode and the largest text size look right.
