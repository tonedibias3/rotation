# Rotation plan (status: APPROVED Oct 14; Stage 1 done, Stage 2 waits on a Mac)

End goal: Rotation is live in the App Store, people who try it keep using it, and shared images bring new people in. Passion project, so paid store fees are fine; no revenue target.

Legend: P = can run in parallel. Each step: reads/writes | output | check.

## Stage 1: Ship-ready foundation (P)
1. Harness files + check script. Writes CLAUDE.md, harness/*, scripts/check.js | committed | `node scripts/check.js` 7/7. DONE.
2. First-run experience. DONE Oct 14. Reads app/index.html (seed, init, viewCloset) | writes app/index.html | empty state offers "Add 5 pieces in a minute" + sample closet toggle; first outfit logged in under 60s | manual walkthrough screenshot + check.js.
3. Share-first loop. DONE Oct 14. Reads share sheet code | writes app/index.html | one-tap "Share today's fit" from the Log tab, after logging prompt to share | screenshot of the share card from a fresh install.
4. Feedback + backup safety net. DONE Oct 14. Writes app/index.html | Settings: "Send feedback" (mailto hello@rotation.fit with app version), backup reminder after 14 days (data is device-only) | check.js + test export/import round trip.

## Stage 2: App Store path (after Tone gets the Mac) (P with Stage 1 where noted)
5. App Store listing kit (P). Writes harness/appstore.md | name/subtitle/keywords/description, privacy nutrition label answers, review notes, screenshot list using shots/ | checklist complete.
6. Native value-adds so review does not see a plain web wrapper (guideline 4.2): haptics, home-screen widget, local reminder opt-in. Writes ios/ + app | builds in Xcode | needs the Mac.
7. TestFlight build to friends. Needs Apple Developer ($99/yr) | build uploaded | Tone confirms install.

## Stage 3: Brand leftovers (P, small)
8. Social icons beside handles on landing + beta card (Tone confirms spots). 
9. Old-handle cleanup in the Desktop pitch deck/one-pager files (needs computer linked) and bios.
10. Facebook page decision recorded.

## Stop conditions
All checks pass and Tone approves, or a blocker (Mac, Apple account, Tone decision) is hit; then return partial status with exact steps left.
