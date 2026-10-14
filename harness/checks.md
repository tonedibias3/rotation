# Checks (step | requirement | verdict | evidence)
Verdicts: pass / fail / unresolved. Update after every run.

| step | requirement | verdict | evidence |
|---|---|---|---|
| 1 | check.js runs and passes on current main | pass | 7/7 on Oct 14 |
| 1 | no @rotationcloset anywhere | pass | check.js |
| 1 | app JS parses | pass | check.js |
| 1 | beta URL not on public pages | pass | check.js |
| 2 | empty closet -> starter list -> Get started checklist on Closet + Log; Hide persists | pass | scripts/e2e.py 21/21 |
| 2 | checklist updates live when a piece is picked | pass | scripts/e2e.py |
| 3 | Share this fit on Log opens share sheet; nothing picked shows a hint, no sheet | pass | scripts/e2e.py |
| 4 | export then import on a fresh device restores every piece; survives reload | pass | scripts/e2e.py (closet only; days not covered yet) |
| 4 | feedback mailto goes to hello@rotation.fit, carries counts not item names | pass | scripts/e2e.py |
| 4 | backup nudge: shows at 8+ pieces, clears after export, returns after 14 days, snoozes | pass | scripts/e2e.py |
| 2 | first outfit logged in under 60s by a real new user | unresolved | needs watching a real person |
| 5 | listing kit covers name, subtitle, keywords, privacy label, review notes, screenshots | unresolved | |
| 6 | Xcode build succeeds on device | unresolved | needs Mac |
