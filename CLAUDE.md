# Rotation: working rules (read first, every session)

Passion project by Tone (Antonio Isaac): a closet + outfit-log + wear-calendar app. Goal is not revenue; goal is a useful app that lives in the App Store and that people actually use and share.

## How to work (the harness)
- Batch the work. Read harness/plan.md, take every ready step, run independent steps in parallel, ship one combined result. No one-change-per-message loops.
- Ask Tone only when a missing answer changes the outcome. Batch questions into ONE message.
- Every step has a check. Run `node scripts/check.js` before saying anything is done. Never weaken a check to get a pass.
- Update harness/progress.md after each stage (done, outputs, decisions, open issues, next action). On resume read CLAUDE.md, plan.md, progress.md first.
- Ask before publishing, sending, or spending. Push to main only after checks pass.
- After every change, send the live URL: https://tonedibias3.github.io/rotation/

## Code map
- app/index.html is the whole app (single file, vanilla JS, ~2400 lines). Edit this; it is the source of truth.
- Data: IndexedDB `rotation` plus localStorage keys `rotation.settings`, `rotation.v1`, `rotation.wx`. Local only; export/import exists. The old Claude-artifact cloud sync (window.claude db/assets) was removed Oct 14; do not reintroduce it.
- index.html (root) = public landing page (uses shots/); installed/standalone users are redirected to app/. landing/ is a tiny redirect stub to rotation.fit. The live rotation.fit site is built from the separate rotation-site repo.
- ios/ = Capacitor wrapper. `npm run sync` copies app/ into www/ and syncs iOS. See IOS.md.
- scripts/check.js = deterministic checks. scripts/make-www.js = iOS copy step.

## Hard rules (learned, do not repeat the mistakes)
- Brand: ROTATION.fit wordmark (caps ROTATION, lowercase .fit). Handles: Instagram @rotation.fit, X @rotationfit. @rotationcloset is retired; it must never appear.
- Public pages never link the beta app URL. App link only goes to beta testers on request.
- Say Tone "vibe coded" Rotation, never "hand-coded".
- Design: modern, must not look like a Claude app, no emoji. Pill nav sits at the bottom of the screen (thumb reach, moved Oct 16), with search and add flanking it, and shrinks on scroll. Share images always carry the ROTATION.fit watermark (position movable, never off).
- Colors are not saved for scents. Changing a day's scent resets its rating.
- Git: attach tonedibias3/rotation with push access, then `git push origin HEAD:main`. Commit messages end with the Claude co-author trailer.
- Keep user data on device. Any new network call must be added to the host allowlist in scripts/check.js on purpose.
