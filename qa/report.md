# Wispwalk QA report (live site), 2026-10-24
Target: https://artisalivalor1591-cell.github.io/wispwalk/. Device: Playwright Chromium, Pixel 7 emulation (412x915). Fake geo is 44.43601,-89.41313 unless noted. Seeded with `ttu_profile_theme`=<theme> and `ttu_profile_v1.fan`=true/false. Coverage: 6 themes × normal/fantasy (12 combos). Scripts: qa/*.py. Shots: qa/, qa/shots_m/, qa/shots_h/.

**Counts: P0 0 · P1 8 · P2 10 · nits 7**

## P1
1. **Compass stays "Locating…" until the device moves.** Repro: `?reset=1`, haunted, agree → lantern → On foot · ½ mi · Easy → Off we go. Expected: the needle and accuracy show within a few seconds. Actual: no needle and an empty #acc for 30 s+. It updates instantly after the first position change. Wisp proximity and detour (`__wispC`) both depend on it. Needs a real-device check (it may be headless-only). Shot: shots_h/haunted_norm_hunt.png
2. **Permission dialog question is invisible.** Repro: Draw my own area → Open the map → tap 4 corners → Done → lantern. Actual: "Is this your own property, or do you have the owner's permission…" is pale lavender on cream and almost unreadable. Shot: 08_permission_dialog.png
3. **Geo denied shows a raw browser error.** Repro: block location permission, then Off we go. Actual: "Problem: User denied Geolocation. Allow location access and try again." Expected: friendly copy that says how to re-enable location. Shot: 09_denied_b.png
4. **Begin-line wraps into the CTA.** "A cold breeze, a faint glow…" / "A secret is buried nearby…" wrap onto 2 lines and crowd or overlap "Follow it?" / "Dig it up?". Shots: 08_permission_dialog.png, 09_denied_b.png
5. **Story theme Begin step: selected text unreadable.** Dark red on dark slate. Shot: shots_m/story_norm_begin.png
6. **Spring Begin step: low contrast overall.** Shot: shots_m/spring_norm_begin.png
7. **Win screen: milestone toast covers "↺ Start fresh".** Repro: complete a hunt (move to the pin → claim). Shot: shots_h/golden_norm_win.png
8. **Feedback card is translucent.** Win-card text bleeds through, and the white text is low contrast in spring and summer. Shot: shots_h/spring_norm_win.png

## P2
1. **Default ½ mi hunt fails at the coverage center.** At Birnamwood center it says "No approved public spots within 0.5 mi of you. Try a bigger radius." Suggest auto-widening the radius or offering Wander.
2. **"By car" shows combo copy.** It reads "Park somewhere safe, then finish on foot." Shot: shots_m/*_mv_drive.png
3. **Prize names include the zone name**, e.g. "You found Hard Scrabble - SR 10 Midnight Ember". It also shows on the share card. Shot: shots_h/golden_norm_sharecard.png
4. **Star catch copy:** "You caught Star-caught Midnight Wish Shard." Every item also gets "Midnight".
5. **Detour copy mixes voices.** A first-person quip is followed by "Follow it to X?", e.g. "I'm a winter wisp, so naturally I'm a little flaky. Follow it to Super Duper Looper?" Shot: sheet_h_detour_offer.png
6. **Share card:** it says "An afternoon in the golden woods" at 2 AM, and "medium" is lowercase. Shot: shots_h/golden_norm_sharecard.png
7. **Art clashes.** Prizes ignore the theme: golden gets Pumpkin Head and Witch's Lantern, winter gets Bat Cloak, spring gets a maple leaf. "Trail Staff" uses 🦯 (white cane). Shot: sheet_h_win.png
8. **Internal header "Solo hunt · Tier 1 prototype"** is visible on the win screen.
9. **Compass text gets selected when dragging a wisp** (blue highlight). The compass needs `user-select:none`. Shot: shots_h/haunted_norm_star_caught.png
10. **Draw my own area opens the old settings panel.** Its labels are "Draw public area" (with a blurred glow box behind it) and "My property". The panel also has an orphan "Use" line. The map sits below the fold, and "Hide my treasure" is hidden, so the user has to find "Done" and then the lantern. Shots: 07_draw_map.png, 08_draw_polygon.png

## Nits
- "Your mock prize: Mock: $5 coffee voucher" repeats "Mock".
- The milestone "a first critter sighting" starts lowercase.
- The feedback placeholder "anything you'd like to tell us? (optional)" starts lowercase.
- "Walked so far: 0" has no unit.
- "I won't trespass!" has an exclamation mark.
- The intro is not fantasy-specific.
- The drawn-area pin can land only ~14 m from the edge (the copy says "a little in from the edges").

## Verified working
- The intro has no Skip in all 12 combos, and it does not come back after Start fresh or a reload (05_after_start_fresh.png).
- Start/begin lines: no overlap or off-screen text found by the automated check in any of the 12 combos (except the wrap in P1-4).
- Travel modes, distances and the Custom slider work (defaults: walk 1, drive 15, combo 3 mi).
- Wisp tap, follow, twirl, decoy and mirage work. Detour: offer → follow → reward → "Path Less Traveled" toast.
- Shooting star (`?star=1`, `TTU_STAR.fly()`): catch works and sets ttu_star_caught. The star is a short-lived moving target; it was spawned and caught in 4 of 12 timed runs. The misses look like harness timing, not a bug.
- Claim → win, share PNG download and the feedback card all work.
- Draw my own area: the polygon draws, the permission dialog appears, and the pin was inside the drawn polygon (point-in-polygon check: inside=true).
- Wander nearby starts a hunt with a needle (09_wander_b.png). Somewhere else with no place blocks with "First, choose a place."
- No JS errors in any run. The only console message is a requestFullscreen user-gesture warning.
- Redirect: https://artisalivalor1591-cell.github.io/trail-trade-up/ → final URL **https://artisalivalor1591-cell.github.io/wispwalk/**

## Not tested / limits
- Real compass heading and latency: headless has no magnetometer, and deviceorientation can't be judged meaningfully. Needs a phone.
- The native OS/browser location prompt: headless can't show it. Tested only granted vs. denied.
- Somewhere else full flow (#elQ geocode search, then tap a spot on the map and save) was not driven end to end.
- Thief trickster was not triggered.
- Audio/sound (`?snd=`) and iOS Safari were not tested.
