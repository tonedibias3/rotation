# Progress (updated Oct 14, 2026)
Plan: Stage 1 done. Own-photos-only decision made and built. Stage 2 (App Store) waits on Xcode space (USB-A to C adapter + external drive, or M3 Mac).
Outputs: app/index.html (Get started checklist, Share this fit, Send feedback, backup nudge, Quick add many photos, Google photo search removed), scripts/check.js (8 checks), scripts/e2e.py (28 headless checks), privacy.html (photo-search section removed).
Decisions: feedback = email only, no tracking. Own photos only; Google/online photo search removed (Tone, Oct 14). Fully flesh out the app before the App Store push; no rush.
Open issues:
- Backup export now uses Capacitor Filesystem + Share inside the iOS app (falls back to web share, then download). Code-complete but UNTESTED on a device; verify on first TestFlight build.
- Xcode: add a PrivacyInfo.xcprivacy to the App target on the Mac (not in repo yet; Apple asks for it).
- No background removal on photos; Quick add fits each photo on a white square. Real background removal needs an on-device model (heavy) - decide later.
- Export/import round trip tested for closet pieces; logged days and looks not covered by e2e yet.
- Real new-user timing (first logged outfit under 60s) still unmeasured; needs watching 3-5 real people.
Cleanup Oct 14: removed dead cloud-sync/asset-upload code (window.claude, ASSETS, store flags), unused constants and a dead helper; app/index.html 195 KB -> 192 KB, 2454 -> ~2390 lines. Audit found no unused CSS, icons, keyframes, TODOs or console logs.
iOS prep Oct 14: added NSLocationWhenInUse string (weather), ITSAppUsesNonExemptEncryption=false, @capacitor/share dependency.
Next action: Tone picks the next batch (ideas: photo cleanup/auto-trim, share card polish, calendar/stats depth, iOS-native export).

Oct 15 bug pass (iPad screenshots): crop dialog canvas now extends 14px past the frame so edge handles are never clipped; empty Back slot is a dashed camera tile (was a blank tinted square with undefined --c); share sheet locks page scroll and scrolls itself (overscroll-behavior contain); hex field styled. check.js 8/8. Open: screenshots (c) blank Photos-picker preview is iOS-side; (e)/(f) before/after-save differences need Tone's notes.

Oct 15: Settings > Sort closet by (Brand | Most worn), within each section; persisted and restored on import. check.js 8/8.

Oct 15: Added plan step 6b (CloudKit iCloud sync, native only, after Mac). Tone likes the idea; nothing built yet.

Oct 15: Share-card patterns added: Camo, Duck camo, Paisley (Checker renamed Checkerboard); presets Olive/tan, Black/red, Red/white. check.js 8/8.
