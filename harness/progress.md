# Progress (updated Oct 14, 2026)
Plan: Stage 1 steps 1-4 done. Stage 2 (App Store) waits on Tone's Mac storage/new Mac. Stage 3 leftovers not started.
Outputs: app/index.html (Get started checklist, Share this fit button, Send feedback in Settings + footer, 14-day backup nudge), scripts/check.js (7 checks), scripts/e2e.py (21 headless checks).
Decisions: feedback = email to hello@rotation.fit only, no usage tracking (Tone, Oct 14). App should be fully fleshed out before the App Store push; Tone is not in a rush.
Open issues:
- Photo search needs the user's own Google API key (5-min setup). Normal users will never do this; adding pieces without it means taking own photos. Biggest onboarding wall. Needs a decision.
- Backup export uses a browser download (a[download]); likely does nothing inside the iOS wrapper. Needs Capacitor Filesystem + Share before TestFlight.
- images.weserv.nl proxy sees product image URLs; disclose in privacy.html.
- Export/import round trip tested for closet pieces; logged days and looks not yet covered by e2e.
Next action: Tone decides on photo search (see final message), then next feature batch. Mac: check free space / get adapter, or order M3.
