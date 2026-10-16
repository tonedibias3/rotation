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

Oct 15 favorites + calendar save look: items get `fav` (heart toggle in piece view and Edit piece; small heart badge on cards). Closet: Favorites filter chip (combines with type), new Wall tab (photo grid of favorites, most worn first, Share button -> share card mode 'wall', up to 9 square / 12 story, header FAVORITES, caption #favorites). Log: Favorites only chip, favorites sort first. Calendar day view: Save look button per outfit (2+ pieces) that becomes "In your looks" (opens the existing look; adds the outfit photo to it if missing); same duplicate rule as the Log button. check.js 8/8; headless test of all flows passed. Open: Tone to judge look of Wall and heart badge; cost-per-wear already exists in piece view.

Oct 15 quality audit (harness/quality.md): bundled fonts (no Google call), offline service worker, accessibility fixes (labels, contrast, touch targets), 5-day backup nudge for browser-tab users. check.js 9/9, e2e 28/28, axe clean on Closet and Log. Open: real first-run observation, iPad picker bug notes, HEIC/VoiceOver/large-text tests, landing page fonts.

Oct 15 phone calendar (Tone's iPhone vs iPad screenshots): on phones (<=520px) day cells with a photo are now full-bleed portrait (1/1.3), date as a small chip top-left, badge (+N / N fits) above the bars, occasion bars as a chip along the bottom; gutters tighter. Empty days no longer show a dark pill in dark mode (`.hero.none` was losing to the dark `.hero` rule; fixed for all sizes). Calendar header buttons shrink to 36px and the header wraps, so the page no longer scrolls sideways at 375px. iPad/desktop layout unchanged. check.js 9/9, e2e 28/28. Next: Month/Week toggle (big photos per day) and a Fits/Shoes/Scents filter on the calendar.

## Oct 15: calendar week view + kind filter
- Done: Month/Week toggle (SET.cmode), All/Fits/Shoes/Scents filter (SET.ckind), week list rows with photo, filter-aware empty hint.
- Decision: calendar mode action is `calmode` (`cmode` already used by closet view toggle).
- Checks: check.js 9/9, e2e 28/28, no overflow at 375/402, no page errors.
- Next: none open.

## Oct 15: share card fixes
- Done: no pieces selected now shows the whole outfit photo (fitted, not cropped to the square box). Scent/shoe cards lead with "SCENT OF THE DAY" / "SHOE OF THE DAY" as the title, date + rating underneath.
- Checks: check.js and e2e.py pass.
- Share cards: every layout (square with pieces, story, on-feet) now scales the whole photo to fit instead of cropping. Zoom/drag still crops on purpose.
- Landing page (root index.html): nav and footer wordmark now ROTATION.fit (caps ROTATION, lowercase .fit). Live app link is /rotation/app/, root is the landing page.
- Saved looks sheet: tiles wrap inside the card (no overlap with Change photo / delete), piece-name text removed (tag label kept). Share photo hint now says whole photo shows by default, zoom then drag to move.
- Fix: my phone calendar header wrap (.head flex-wrap) hit every tab and pushed the weather block under the title on Closet. Now scoped to the calendar header only (.head:has(.mnav)). Settings button icon changed from a sun-like icon to a real gear.

## Oct 16: iOS review fixes (from ios-review pass on screenshots)
- Done: nav pill moved to a bottom bar with a fade behind it (content no longer shows through the nav); Log tray and toast sit above it; --navh variable holds the bar height. Mono labels and tiny text raised to 11-12px (was 9-10px). Touch targets: round icon buttons 44px (calendar header, close X), chip remove X has a larger hit area. Add to Home Screen prompt on Closet for iPhone/iPad Safari tab users (3+ pieces, dismissible with Got it, setting a2hs); shows instead of the backup nudge until dismissed.
- Already fine, no change: backup nudge (5 days in browser, 14 in app), navigator.storage.persist, aria-labels on icon buttons, calendar header at 375 (no overflow).
- Decision: accent colors vary by the Accent setting on purpose (not a bug).
- Checks: check.js 9/9, e2e 28/28, no horizontal overflow at 375 and 440, light and dark. Not tested: real iPhone safe area in the Capacitor app (contentInset always), large Dynamic Type sizes, VoiceOver.

## Oct 16: closet flow requests (Tone)
- Done: tap outside closes the saved look, saved looks list, scent and shoe sheets (looks-bg); piece view (long press) has a primary "Start outfit" button ("Add to today" when today already has pieces; hidden for scents) that jumps to Log with the piece added to today's outfit; favorites sort to the front of their closet row/grid (next to the Add tile) in both Brand and Most worn sorts.
- Checks: check.js 9/9, e2e 28/28, headless test of fav order (move to front, unfavorite restores), tap-outside, tap-inside-stays-open.

## Oct 16 (later): UX evaluation fixes (intent:evaluate P1-P3)
Done: Undo toast (7s) for piece, look, shoe and erase-all removal. Backup restore now compares rows, asks only when something differs (keep phone / use backup / cancel), always adds new rows, bad file gets a clear message. In-app ask() sheet replaces native confirm/prompt in the weather flow. All CSS font sizes moved to rem; root size follows iOS text size (Dynamic Type probe, capped at 1.35x; `?tz=1.5` forces it for tests). Global reduced motion. Error toasts say what to do next. Empty closet hides search, filters and Arrange. Footer feedback link removed (Settings has it). Tray "Done" is now "View day".
Decisions: no new network calls. Probe only scales on Apple devices.
Open: not tested on a real iPhone (Dynamic Type probe in WKWebView, bottom bar above home indicator, VoiceOver). /intent:investigate not run.
Next: Xcode build on a Mac (Stage 2).

## Oct 16: day view order + Clear day (Tone)
- Done: day view sections now run Outfit, Shoe of the day, Scent of the day (was scent, shoe, outfit). New "Clear day" button in the day view and on the Log screen (log mode) wipes outfits, photos, shoe and scent for that day, keeps planned options, 7s Undo toast. Log "Clear" still clears just the current outfit.
- Checks: check.js 9/9, e2e 28/28, headless test of order, clear, undo, disabled-when-empty.
