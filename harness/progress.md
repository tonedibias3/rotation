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
- Same day: removed the old Clear button in Log mode (Clear day replaces it). Plan mode keeps Clear for options. Tone's call.
Oct 16 bug pass (Tone, iPad): (1) adding or removing a piece while building a fit in Log sent the page back to the top; saveItem/delete now restore scroll (keepY, re-applied as layout settles). (2) Calendar > Stats "Share <month> recap" button did nothing: openRecap referenced an undefined `it` (ReferenceError); fixed. e2e.py now has regression checks for both (31/31; recap check fails on the old code). check.js 9/9. Open: scroll fix is verified in headless Chromium only; Tone to confirm on iPad (the exact long-press-to-view-shoe path was not reproduced separately).

## Oct 16: share patterns trimmed (Tone)
- Removed Camo, Duck camo and Paisley from share-card patterns (too many options, didn't render well). Saved camo/duck/paisley settings fall back to Houndstooth. Seven patterns remain. check.js 9/9, e2e 28/28.
- Same day: also removed the Olive/tan, Black/red and Red/white color presets (they were added for camo). Five presets remain. Tone's call.

## Oct 16: tartan follows chosen colors (Tone)
- Bug: tartan used hardcoded navy/black/green, so color swatches, presets and Subtle/Bold did nothing. Now built from the two chosen pattern colors (primary, secondary, darkened thin lines). Verified all 5 presets give different tiles. check.js 9/9, e2e 31/31.

## Oct 16: launch-readiness sweep (Claude, requested by Tone)
- Done: site privacy.html still described the retired Google photo search; removed. Both privacy pages (this repo and rotation-site) now have a "Feedback and backups" section (feedback email draft is editable, nothing sent automatically; backups saved by the user), dated Oct 16. Landing buttons "Follow on Instagram / X" got the Instagram and X icons (rotation-site 02f7764). App repo 1bdb0c1. check.js 9/9.
- Verified already fine: no @rotationcloset in either repo, footer social icons, hello@rotation.fit, privacy link, feedback in Settings, backup nudge, Add to Home Screen prompt, navigator.storage.persist.
- Weak points logged (see project doc "pending-handoff.md"): rotation-site privacy page can drift from this repo's copy again (two copies); no email capture; Desktop pitch deck files unchecked for old handle (folder grant refused); real-device tests; handle reservations.
- Next action: Tone connects ~/Desktop/rotation, decides email capture, then Stage 2 step 5 (App Store listing kit, no Mac needed).

## Oct 16 (later): backup tests + App Store kit (Claude, requested by Tone)
- Done: e2e.py now round-trips a rich backup (favorites, extra item fields, day outfit/tag/rating/shoe/scent/when, extra outfits, plans, scent-only day, looks, settings) through import, reload, export and a second device, plus idempotent re-import, the three conflict choices (keep phone, use backup, cancel) and a non-backup file. Reads persisted IndexedDB/localStorage, not app internals. 58/58. No app bug found. Commit 0cc9d48.
- Done: harness/appstore.md drafted (name, subtitle, keywords, description, privacy label reasoning, review notes, screenshot plan, checklist).
- Found: Info.plist location string says "never stored or shared" but the code stores a rounded position on device and sends it to Open-Meteo and BigDataCloud, and privacy.html says so. Needs Tone's OK to change the string (suggested text in appstore.md). Also decide whether to declare Coarse Location in the privacy label.
- Rollback points: app repo e16d1c9 (before tests), site repo 02f7764. Tag push was blocked by the proxy, so commit hashes are the checkpoints.
- Next action: Tone decides the location wording and label, connects ~/Desktop/rotation, decides email capture.

## Oct 16 (evening): tap = view, press and hold = edit (Tone)
- Tone: long press to view made no sense. Closet: tap a piece opens the view sheet (has Start outfit / Add to today, Edit, favorite), press and hold opens the edit form. Log picker: tap still selects a piece for today's outfit (that is the point of that screen), press and hold opens edit. Hints updated on both screens. Calendar day sheets (shoe/scent pickers) keep tap = choose, hold = edit. Held release no longer also fires a tap.
- Code: `view-item` action replaces `open-item`; `editFromCard()` (skips when a sheet, view or arrange is open). Wall tab already opened the view on tap.
- Tests: e2e 69/69 (new: closet tap, view Edit button, closet hold, no double open, Log tap selects, Log hold edits without selecting). check.js 9/9.
- Open: not tested on a real iPad/iPhone touch (hold length 450 ms, iOS may show its own callout on photos); Tone to confirm. If Log tap should also open the view, say so; selecting would then move to a different control.
- Same evening, separate commit: Escape key threw "FD is not defined" (leftover from the removed photo search, since Oct 14), so Escape never closed a view sheet or edit form on a keyboard. Removed the dead reference. e2e now 72/72 with a regression test that fails on the old code.

## Oct 16 (night): Add to today from the view sheet no longer jumps (Tone, screen recording)
- Cause: the earlier scroll fix (Oct 16 bug pass) covered only the edit sheet (saveItem/removeItem call keepY). The view sheet button (`view-wear`) is a separate path and deliberately did `S.tab='log'; render(); toTop()`, so every add switched to Log and scrolled to the top. The old test only covered adding a NEW piece from Log, so it never touched this path.
- Fix: `view-wear` now closes the view, adds the piece, keeps the current tab and scroll position (keepY), and toasts "Added to today" (or the selected date when already in Log on another day). No re-render.
- Test (fails on the old code: 1362 -> 0 and tab changed; passes now 1362 -> 1362): e2e 81/81, check.js 9/9.
- Not changed: "Look added to today" (saved look) still jumps to Log; calendar-day Edit and tab/filter/search navigation are intentional jumps. Ask Tone if the look flow should stay put too.
- Rollback point: d9afbd2.


Oct 17: "Lead with the back" (Tone, shorts where the back is the best part). Edit piece shows a switch (only when both photos exist) that swaps which photo is the main one; item stores `swap:true` and the two photo fields are physically swapped, so cards, Wall, Log and share all lead with the back with no other code touched. Piece view and item share labels flip (Back/Front) when swapped. Removing either photo resets the switch. e2e: 4 new checks (87/87), check.js 9/9. Open: Tone to try on the shorts.

Oct 17 backup log (Tone, working across computer, iPad and phone): Settings > Backup now shows Last export and Last import with date, time and device ("iPhone browser", "iPad app", "Mac browser"...), plus the source of the last imported file ("a backup saved Fri, Oct 16, 9:10 PM on iPad app"). Export files now carry exportedAt and device (older files fall back to the file's modified time). Importing a file older than the newest backup/import this device has seen asks first ("This backup is older", names the file's date and device; Cancel is the default). Import is still a merge (adds missing, asks which version wins on conflicts, never deletes). e2e 96/96, check.js 9/9. Open: device names are auto-detected, so two iPads look the same; add a rename if that matters. Pieces deleted on one device come back on import (merge); real two-way sync is the CloudKit plan (step 6b).
