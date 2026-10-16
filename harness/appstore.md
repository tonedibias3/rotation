# App Store listing kit (plan step 5, drafted Oct 16)

Status: DRAFT. Nothing here is submitted. Items marked DECIDE need Tone. Items marked VERIFY need App Store Connect or a device. Facts come from the code (app/index.html, ios/, privacy.html), not from memory.

## Identity
- Bundle ID: com.tonedibias3.rotation (ios/App/App.xcodeproj). Version 1.0. Min iOS 15.0. Devices: iPhone and iPad (TARGETED_DEVICE_FAMILY 1,2), so iPad screenshots are required.
- App name (30 max): `Rotation: Closet & Outfit Log` (29). The plain name "Rotation" is generic and very likely taken in the store. VERIFY availability when the app record is created; keep this as the fallback-proof form.
- Subtitle (30 max): `Log what you wear. Share it.` (28)
- Category: primary Lifestyle. Secondary: Productivity. (Not Shopping: nothing is sold or bought in the app.)
- Support URL: https://rotation.fit . Marketing URL: https://rotation.fit . Privacy policy URL: https://rotation.fit/privacy.html . Support email: hello@rotation.fit
- Copyright line: DECIDE the legal name (personal name or an LLC) before submission.
- Price: DECIDE. Public materials show no price anywhere until announced. The Oct 13 landing page says "free during beta" and "pricing will be announced before App Store launch".

## Promotional text (170 max, editable any time)
`Add your pieces, log what you wear each day, and see what you actually wear. No account. Your data stays on your device.` (120)

## Keywords (100 max, comma separated, no spaces after commas)
`wardrobe,ootd,sneakers,fragrance,cologne,organizer,planner,calendar,cost per wear,shoes,style,fits` (98)
Words already in the name or subtitle (closet, outfit, log, wear, share) are not repeated on purpose.

## Description (4000 max)
Rotation is a closet and outfit log for people who care what they wear.

Add your clothes, shoes and fragrances with your own photos. Log what you wear each day. See which pieces you actually wear and which ones just sit there.

WHAT YOU CAN DO
Build your closet. Sort pieces into tops, bottoms, shoes, outerwear, accessories and scents. Add brand, type, colors, price and where you bought it.
Log your fit. Pick the pieces, add a photo, and tag the day work, casual or going out.
Shoe of the day and scent of the day. Set either one and rate it.
See it on a calendar. Month or week view, with your photos on each day.
Track cost per wear. Add a price and Rotation does the math as you log.
Save your looks. Keep your best fits and heart the pieces you love.
Share it. Turn a fit, a shoe, a scent, a single piece or your monthly recap into a clean image for Instagram or X. Prices and where you bought something are never shown.

PRIVATE BY DESIGN
No account. No ads. No tracking. Your closet, photos and history stay on your device. Save a backup file to iCloud or Files and load it on another device any time.

The weather chip is optional. If you turn it on, Rotation uses your approximate location to show the forecast for your outfit.

Questions or ideas: hello@rotation.fit

Do not add before it is true: iCloud sync (plan step 6b is not built), widgets, reminders (plan step 6), any price, any "No. 1" or comparison claim.

## What's New (version 1.0)
`First release.`

## Age rating (questionnaire answers)
All "None": no violence, no mature or suggestive themes, no gambling, no unrestricted web access, no user-generated content shared with other users (sharing goes out through the system share sheet only). Expected result: 4+. VERIFY in the questionnaire.

## Privacy nutrition label (App Store Connect > App Privacy)
Principle: Apple counts data as collected when it leaves the device and you or a partner can keep it longer than needed to serve the request. Answers below follow the code.
- Account: none. Tracking: No. Third-party analytics, ads, SDKs: none (check.js enforces no unexpected hosts).
- Photos and camera: stay on device. Not collected.
- Closet, outfits, notes, ratings, backups: stay on device. Not collected.
- Coarse location (weather chip, optional): the app rounds it to about 0.01 degrees (roughly a mile), stores it on the device, and sends it to Open-Meteo (forecast) and BigDataCloud (town name). DECIDE and VERIFY: the conservative answer is to declare "Coarse Location", purpose App Functionality, not linked to the user, not used for tracking. Under-declaring is the risk; over-declaring costs nothing. Confidence that declaring is required is only moderate, so confirm with Apple's current definition when filling the form.
- Contact info: the feedback button opens the user's own email app. Nothing is sent by Rotation. Not collected.
- Resulting label if coarse location is declared: "Data Used to Track You: none"; "Data Not Linked to You: Coarse Location".

## Privacy-string fix needed before submission (DECIDE, edit not made)
ios/App/App/Info.plist NSLocationWhenInUseUsageDescription currently says: "Rotation uses your location once to show the weather for your outfit. It is never stored or shared." That contradicts privacy.html and the code (stored on device, sent to two weather services). A reviewer or user comparing the two would see it. Suggested replacement: "Rotation uses your approximate location to show the weather for your outfit. It is rounded and sent to a weather service for the forecast. Rotation never keeps it on a server."

## Review notes (paste into App Review Information)
No sign-in is required and there is no demo account. To see content quickly: on the empty Closet tap "Start your closet", then add the starter list. Then open the Log tab, pick a few pieces and tap Share this fit. The weather chip is optional; location is requested only if you turn it on. All data stays on the device. Contact: hello@rotation.fit.
Guideline 4.2 (minimum functionality): reviewers dislike plain web wrappers. Plan step 6 (haptics, a home-screen widget, local reminder opt-in) is what answers this. Do not submit before step 6 is built and tested on a device.

## Export compliance
ITSAppUsesNonExemptEncryption = false is already set in Info.plist. The app uses only standard HTTPS.

## Screenshots
- Required sets: iPhone 6.9 inch (1320 x 2868) and iPad 13 inch (2064 x 2752) because the app supports iPad. 3 to 10 images each.
- Existing images (shots/ at 720 px wide, install/shots/ at 600 px wide) are far too small. They are fine for the landing page only.
- Plan: capture on the Simulator or a TestFlight build with Tone's real export file loaded (real photos and wear history). A headless render at the right size is possible but App Review prefers real device UI, so use it only if the Mac is delayed.
- Suggested order (benefit first, one idea per screen, short caption on top, no price): 1 Closet ("Your closet, all in one place"), 2 Log a fit ("Log what you wore"), 3 Calendar ("See every day"), 4 Piece detail with cost per wear ("Know what each piece costs per wear"), 5 Share card ("Share it clean"), 6 Looks and favorites ("Save your best fits").
- Keep the watermark and handles consistent: ROTATION.fit, @rotation.fit, @rotationfit.

## Before submitting (checklist)
- [ ] Apple Developer account ($99/yr) and the Mac
- [ ] App record created, name accepted or fallback chosen
- [ ] Info.plist location string fixed (see above)
- [ ] PrivacyInfo.xcprivacy added to the App target (not in repo yet)
- [ ] Plan step 6 built, TestFlight build installed by Tone
- [ ] Real-device pass: safe areas, Dynamic Type, VoiceOver, backup export in the iOS app
- [ ] Screenshots captured at the required sizes
- [ ] Privacy label answered, privacy page matches (both copies: this repo and rotation-site)
- [ ] node scripts/check.js and python3 scripts/e2e.py pass
