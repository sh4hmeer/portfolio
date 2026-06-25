# Tri-City Clinic Walkthrough — HANDOFF (current state)

Authoritative status doc, **rewritten 2026-06-16** and verified against the actual files (not memory). It describes the **current** state — earlier chronological round-notes were removed because several had gone stale (e.g. an old left-side status board and an `Adam_sit` seated sprite that were both later replaced). A short history is at the very bottom.

**Working dir:** `c:\Users\Shahmeer\Desktop\Projects\fde-portfolio\prototype`
**Active file:** `clinic2d.html` (open it directly in a browser — pure static, no server/build needed).

---

## 0. The big picture — where this fits

This is **one segment of a forthcoming personal portfolio site** branding Shahmeer as a *forward-deployed engineer* (creative, informal, "loves helping people with software, leverages AI, makes impact in healthcare"). Repo root: `Desktop/Projects/fde-portfolio`.

- **Portfolio decisions locked (from project memory, not yet built):** stack = **Astro + GitHub Pages on the `sh4hmeer` account**; voice/minimalism north-star = ehmorris.com, but **proof plays in-page, not linked out**; the site will also showcase the real Tri-City Eye Care work (the live OSCAR dashboards, receipt/data-entry automations, Omnia→OSCAR, AI-agents-with-personas) and an informal "about". **The Astro site is NOT scaffolded yet** — only this prototype exists.
- **This walkthrough is the centerpiece** ("watch the OSCAR patient flow, then watch it become data"). When the site is built, `clinic2d.html` (or a componentized version of it) becomes an embedded section the visitor scrolls to. So: keep it self-contained, keep the asset paths relative, and assume it will eventually live inside a larger Astro page rather than be the whole page.

> **NEXT STEP (the actual task after this):** scaffold the Astro + GH-Pages(`sh4hmeer`) site and make this clinic walkthrough one section of it. Nothing in the portfolio shell exists yet beyond this prototype folder.

---

## 1. What the walkthrough does (current behavior)

A **split-screen** experience, ~50/50:
- **Left = a walkable top-down pixel clinic** (the real Tri-City Eye Care floor plan, LimeZu "Modern Interiors Free" art). One "hero" patient auto-walks his whole visit (you *can* drive with WASD/arrows; it returns to auto after ~3.5 s idle). The clinic is populated with seated patients, seated techs, white-coated doctors, wall decor, and a few staff pacing the halls.
- **Right = faithful copies of the real Tri-City dashboards** (HVF / Vision / OCT / Doctors-Lounge), in their real dark theme and status colours. As the patient hits each clinical stage, the matching board is shown and a **fake cursor performs the staff action** (drag the patient's card into a room, click "Done") in sync with him.

**The run, start to finish:**
1. **Intro overlay** — zoomed portrait of the patient + "DOE, Jordan · here to see Dr. Husayn" + today's orders `optos · HVF · VA · OCT · gl w/u` as chips that light up one at a time, each explaining the term and where he'll go. Auto-starts (or "▶ Start the visit").
2. Dashboard starts **dimmed** so you watch him **walk in and check in**; on check-in it un-dims and his card **reveals** into the HVF "greens" queue (so you know who to track).
3. **HVF:** the HVF tech (Amelia) walks all the way out to his seat, **pauses in front** while he says "Yes, I'm ready for HVF", then **leads him in** (clearly ahead of him). Cursor drags his card into an HVF box. The board room-timer **spins up rapidly** (clinical minutes) to ~9 min, then freezes when he leaves.
4. **Vision:** board swaps; Vision tech (Alex) escorts him in the same way; cursor → Vision 1; timer ~5 min.
5. **OCT:** board swaps; he walks himself (no escort); cursor → an OCT room; timer ~4 min.
6. **Doctor:** board swaps to the Doctors-Lounge; his doctor (Husayn) WAIT→BILLED counts tick; doctor portion ~12 min.
7. **Billing & exit:** "That's all for me, thank you." then "What a smooth flow." as he walks out.
8. **Finale** (full-split overlay): door-to-door time (~**40 min** clinical) → "becomes a data row" table → ML "predict-the-day" reveal (training curve, loss, accuracy, "peak congestion ~2:40pm"). "↻ Walk it again" / "↻ Restart" replay the whole thing (intro included).

- A **speech bubble** above the patient narrates the whole visit (brief, fades). A **focus-dim** greys whichever half *isn't* the action so a first-timer knows where to look.
- Total run ≈ **2 min real-time**; the clinical clock reads ~40 min because it accelerates while he's in rooms.

---

## 2. How to run & verify

- **Run:** double-click `clinic2d.html` (file://). It's static; no server. (When embedded in Astro later, asset paths are relative — `assets/limezu/…`, `dash.css`, `dash.js`, `map2d.js`, etc.)
- **Headless screenshots / checks (what I used all session):** Playwright + Chromium with swiftshader. Pattern:
  ```python
  # cd into prototype first — the Bash tool's cwd resets to Desktop/Projects each call
  b=p.chromium.launch(headless=True,args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
  pg.goto(<file uri>); pg.click('#introStart')   # skip the intro wait
  pg.screenshot(clip={'x':..,'y':..,'width':..,'height':..})
  ```
  `_shot.py` is a minimal helper (`python _shot.py clinic2d.html 4000`).
- **Gotchas:**
  - **Bash cwd resets** to `Desktop\Projects` each call → always `cd .../prototype &&` first.
  - **Windows console** can't print em-dash/✓ → set `PYTHONIOENCODING=utf-8`; read JS with `encoding='utf-8'`.
  - The **image-view API** rejects very large/many PNGs → keep crops under ~1200 px, few at a time, or analyse pixels in Python.
  - Pasting the data files into chat **mojibakes** em-dashes/curly-quotes into `â` — clean when writing back.

---

## 3. File inventory (verified)

**Game + data (loaded by `clinic2d.html`, in this order):**
- `clinic2d.html` (~834 lines) — the whole game engine, layout, intro, finale, speech bubbles, escorts, walkers, timer. Loads `dash.css` (link) and the scripts below, then an inline `<script>` IIFE.
- `assets_data.js` — **only `window.CLINIC_ASSETS.index` (the `IDX` cell-type constants) is still used** (`IDX.void/room/wall/deskH/monitor/mach_top/…`). Its procedural tile *images* are no longer drawn (LimeZu replaced them). **Don't delete.**
- `map2d.js` — `window.CLINIC_MAP = {w:88,h:78,rows:[…88-char strings…]}`. Walls/floor/desk/machine grid. **Source of truth for structure.**
- `flow2d.js` — `window.CLINIC_FLOW = {start:[x,y], stops:[…]}`. The hero's route (11 stops, each with a hand-drawn `path`).
- `marks2d.js` — `window.CLINIC_MARKS = {marks:[…]}`. Placement annotations (rooms/waiting/seats/staff/decor/equipment).
- `dash.css` (~119 lines) + `dash.js` (~242 lines) — the four dashboards + the `window.Dash` director API.

**Editor:**
- `mapedit.html` (~443 lines) — visual editor (Walls / Flow / Marks). Authors `map2d.js`/`flow2d.js`/`marks2d.js`; autosaves to `localStorage`; exports via ⬇ buttons.

**Assets — `assets/limezu/`** (LimeZu Modern Interiors **Free** v2.2, non-commercial = fine for a personal portfolio):
- `Room_Builder_free_16x16.png` (floors+walls), `Interiors_free_16x16.png` (furniture — *unused*, multi-tile).
- Walk sheets (384×224, 24 frames = 4 dir × 6, **16×32** each): `Adam_16x16.png` (the player), `Amelia_16x16.png`, `Bob_16x16.png`, `Alex_16x16.png`.
- `Adam_coat.png`, `Amelia_coat.png`, `Bob_coat.png`, `Alex_coat.png` — **generated** white-coat (doctor) variants (see §9).
- `Adam_sit_16x16.png`, `Adam_idle_16x16.png` — present but **NOT used** anymore.
- `assets/` also has `tiles.png`/`char.png`/`tiles_index.json` — legacy procedural atlas, unused.

**Build/util scripts (Python+Pillow):**
- `make_coats.py` — **active:** recolours each walk sheet's shirt band (frame rows 22–28, skin/outline excluded, shading preserved) → `<Name>_coat.png`. Re-run if base art changes.
- `build_map.py` — **legacy:** baked `blueprint_walls.txt` → `map2d.js`. ⚠️ **Never re-run** — it regenerates from the raw blueprint and clobbers all hand/editor edits. `map2d.js` is the source of truth now.
- `make_assets.py` — **legacy:** generated the old procedural atlas (`assets_data.js`, `assets/tiles.png`, `assets/char.png`). Still produces `assets_data.js` whose `IDX` we use; don't need to re-run.
- `render_overview.py` — renders a full-map PNG overview for eyeballing topology. `_shot.py` — screenshot helper.
- `blueprint_walls.txt` / `blueprint_ascii.txt` — the digitised 88×78 floor-plan source (the blueprint *image* `layout2.jpg` is not on disk).

**Superseded prototypes in this folder (keep for reference, NOT active):** `clinic.html` (Three.js perspective version — rejected), `index.html` (card-bouncing v1 — rejected).

---

## 4. Architecture — how the two halves connect

- `clinic2d.html` is the **engine** (canvas game + the page chrome). It exposes nothing globally except by *calling* `window.Dash.*`.
- `dash.js` builds the four boards into the `#dash` panel and exposes **`window.Dash`** (the "director"). The engine drives it; the dashboard never reads game state directly.
- The contract (all calls guarded with `if(window.Dash)`):
  - `Dash.stage(idx, key, leg)` — called from `applyStep(idx)` when the hero **arrives** at flow stop `idx`. The director's big `switch(idx)` swaps boards + animates the cursor.
  - `Dash.clock(timer.secs)` — pushed **every frame**; drives the hero's room-timer on the board.
  - `Dash.focusGame()/focusDash()/focusNone()` — toggle the grey dim on the inactive half.
  - `Dash.roomLeave()` — engine calls it at leg-start when leaving a room → freezes that room-timer.
  - `Dash.reset()` — on restart.
- **Layout:** body = `.split` → (`.stage` [canvas + `#dimGame`] | `.dash` [boards + cursor/drag + `#dimDash`]) and `.finale` (z48) + `#intro` (z50) overlaying the whole split. Canvas auto-sizes from its bounding rect (`resize()` on load + window resize), so the camera adapts to the half-width.

---

## 5. The choreography, stop by stop (the part most likely to need edits)

The flow has a **fixed 11-stop order** (verified in `flow2d.js`), statuses:
`0 here(check-in) · 1 here(wait) · 2 hvf · 3 here(post-hvf) · 4 vision · 5 octwait · 6 oct · 7 drwait · 8 doctor · 9 billed · 10 billed(exit)`

**`dash.js` `stage(idx)` switch (verified):**
- `0` check-in → un-dim dash, hero card into HVF greens queue, `.reveal` animation.
- `1` → nothing (seated beat).
- `2` hvf → `roomEnter()`; cursor **drags** hero into first empty HVF box.
- `3` post-hvf → cursor clicks **HVF done** (`roomLeave`); board → **Vision**, hero into queue.
- `4` vision → `roomEnter()`; cursor drags hero into **Vision 1**.
- `5` octwait → click **Done** (`roomLeave`); board → **OCT**, hero into yellow queue.
- `6` oct → `roomEnter()`; cursor drags hero into first empty OCT room.
- `7` drwait → click **Done** (`roomLeave`); board → **Lounge**, Husayn's `wait++`.
- `8` doctor → pulse.
- `9` billed → Husayn `wait--`, `billed++`.

> ⚠️ **If you reorder/relabel `flow2d.js` stops, update this `switch(idx)`** and the bubble/timer maps below — they're keyed to these exact indices.

**Engine-side per-leg behaviour (in `clinic2d.html` `walkAuto`):**
- **`DWELL`** (real seconds the patient sits at each arrival): `{here:2.5, hvf:6, vision:6, oct:6, octwait:2.5, drwait:2.5, doctor:6, billed:2}`, leg0 = 2.5.
- **Escorts** spawn only for legs whose target is `hvf`/`vision` (`escortSheet` 1=Amelia / 3=Alex). On leg-start: `spawnEscort`, `escortHold=true` (patient frozen at his seat). `updateEscorts`: `out` (speed 225) → within 26 px of patient flips to **`pause`** (~1.9 s, faces him, fires his "ready" bubble) → **`lead`** with an `escortReleaseT` (0.85 s) head-start so the escort stays ahead. Guarded so a failed spawn can't freeze the patient.
- **Speech bubbles** (`drawBubble` on canvas, fades after `TTL 3.2s + 0.55s`): `BUBBLES` = {0:"Ok, let me just check in.",1:"Nice, now I'll find a seat.",2:"Yes, I'm ready for HVF.",3:"Alright, back to waiting.",4:"Hi, yes I'm ready for vision.",5:"Got it, I'll find a seat.",6:"Time for OCT.",7:"That was fast, just need to see the doc now.",10:"What a smooth flow."}. Set at **leg-start** for non-escort legs; at the **escort pause** for legs 2 & 4. Leg **9** is a 2-line queue (`sayLines(["Thanks, doc.","Time to get billed."])`). `ARRIVE_BUBBLES = {9:"That's all for me, thank you."}` fires on arrival at billing. (No em dashes in bubbles, by request. The dashboard *card* reason "gl w/u — optos …" still has one — that's a card, not a bubble.)
- **Clinical timer** (`timer.secs`, runs from first `here`, freezes at first `billed`): advances at **`ROOMRATE` {hvf:90, vision:50, oct:40, doctor:120}** clinical-s per real-s while `pendingDwell>0` in that room, else **base 8** → ~40 min door-to-door. The hero's dashboard room-timer mirrors it via `Dash.clock` (rendered **without `data-ts`** so the per-second `tick()` won't revert it) and **freezes** on `Dash.roomLeave()`.
- **Focus dim:** engine calls `Dash.focusGame()` at each leg-start (watch the character); director calls `Dash.focusDash()` on each board action (watch the board).
- **Finale** fires on the **last** leg (`leg===LEGS.length-1`) → `runFinale()` (calls `Dash.focusNone()` so the dim doesn't bleed onto it).

---

## 6. Data formats

**`map2d.js`** — each row is 88 chars: `#`=wall, `.`=floor, ` `=void(exterior), `D`=desk (solid), `M`=machine (solid; **adjacent to a `D`→ computer/blue monitor, standalone → grey eye-machine**). 88×78. Patient enter/exit opened on the right edge at row 58 (`start`/exit `[87,58]`).

**`flow2d.js`** — `{start:[x,y], stops:[{status,label,where,color,t:[x,y],path:[[x,y],…]}]}`.
- `status` ∈ `here, hvf, vision, octwait, oct, drwait, doctor, billed, via` (`via` = routing-only waypoint, no stop). Repeated statuses are fine (the engine is index-driven).
- Every current stop has an explicit hand-drawn **`path`** (tile list) used verbatim; if a stop has no `path`, the engine BFS-routes between anchors. `label`/`where`/`color` are legacy fields from the old status board (kept; harmless).

**`marks2d.js`** — `{marks:[{type,label,dir,t:[x,y], who?, kind?}]}`. Current counts: 17 `room`, 4 `waiting`, 1 `equipment`, 38 `seat`, 15 `staff`, 7 `decor` (**no `patient` marks — patients are auto-generated into seats**).
- `type` ∈ `room, waiting, seat, patient, staff, equipment, decor`. `dir` ∈ `'',up,down,left,right`.
- **`seat`** rows: a pair labelled `"<key> start"` / `"<key> end"` expands into a straight line of chairs (h or v by relative position); seats without start/end are single. Seat label containing `exam` → always occupied; label `who`-less seats are auto-filled ~52% (skipping flow-stop tiles so the hero's seats stay open).
- **`staff`** / **`patient`** carry **`who`** = a `PEOPLE` catalog id (else a deterministic default). `who` starting `sit_*` ⇒ drawn seated.
- **`decor`** carry optional **`kind`** (a `DECOR_KINDS` value) or auto; decor can also be `start/end` rows (a line of one kind). `room`/`waiting`/`equipment` marks are design labels (room name labels are drawn from a hardcoded `labels` array in the engine, not from marks).

---

## 7. People & rendering (game side)

- **Everyone is one of the 4 walk sheets** (Adam/Amelia/Bob/Alex) + an optional subtle `LOOK_FILTER` tint (`none/warm/cool/muted/rose/sage/sand/sky` — kept gentle so skin stays natural; applied via cached `ctx.filter`, never `getImageData`, to avoid `file://` taint). **`PEOPLE`** (16 ids, shared with the editor): `sit_olive/warm/cool/grey/rose/sage/sand/sky` (these map to the 4 chars **seated**) + `adam/amelia/bob/alex` + 4 tinted standing. `CHAR_IDS` is the auto-fill pool.
- **Seated = the standing walk sprite + a chair drawn over the legs** (`drawSeatFront`). There is **no** seated sprite sheet (the old `Adam_sit` approach was removed — it only had 2 front poses, couldn't face 4 ways or be different people). Facing comes from the seat's `dir`; `faceMachine()` overrides it toward a nearby `M`/monitor for exam/vision/oct seats. **The hero himself also sits** (`player.seated`, facing from `SEAT_DIR`) so he aligns with the row.
- **Doctors** (NPC mark label matching `/^doc/`) render from `coatImgs[sheet]` (the recoloured white-coat sheet) instead of the normal sheet.
- **Decor** primitives (canvas-drawn): `DECOR_KINDS = plant, bookshelf, eyechart, poster, clock, frame, cooler, sign, board`.
- **Walkers:** `WALK_ROUTES` → `WALKERS` pace straight hall segments, animated, y-sorted with everyone (`updateWalkers`). **Escorts** are a separate animated set (`ESCORTS`/`updateEscorts`).
- `ADV_DIR = {0:18,1:6,2:12,3:0}` (down/up/left/right → walk-sheet column block; sheet column order is right,up,left,down). `DIRNUM` maps `'up'/'down'/…`→0-3. `TILE=16`, `SCALE=2`, `TS=32`. `need=9` images.

---

## 8. The editor (`mapedit.html`)

Three modes (**Walls / Flow / Marks**) + shared: blueprint-underlay picker+opacity, zoom, show flow/marks/gridlines, live **Flow check**, and **Save** (⬇ map / ⬇ flow / ⬇ marks · Revert all · Clear autosave).
- **Walls:** brushes `1` wall · `2` floor · `3` desk · `4` machine · `5` void; left-drag paint, right-drag erase; live flow-break detection.
- **Flow:** per-stop status/colour/label/where, reorder, delete; drag dots to move stops/START; **✏ draw custom path** toggle (drag across floor; non-adjacent jumps BFS-bridged; pink path vs cyan BFS; `✏ path(N)` chip + `⌫path`; contiguity validated).
- **Marks:** per-mark type/label/facing/delete; drag diamonds; for `patient`/`staff` a **person** dropdown (`who`); for `decor` an **item** dropdown (`kind`); seat & decor **start/end rows previewed** as dot-lines.
- ⚠️ **Edits live in `localStorage`** (`clinic_mapedit_rows`/`clinic_flowedit`/`clinic_marksedit`) **until exported.** You must ⬇ and drop the files into `prototype/`. If old in-browser marks shadow a new file, **Clear autosave / Revert**.

---

## 9. Doctor white-coat pipeline (`make_coats.py`)

Doctors needed white attire; a drawn overlay looked like a pasted blob (rejected). Instead, **build-time recolour:** `make_coats.py` whitens only the shirt band (frame rows `22..28`, skin & dark outlines excluded, shading preserved by luminance) of each `<Name>_16x16.png` → `<Name>_coat.png`. The game loads these as `coatImgs[0..3]` and draws doctors from them. Re-run `python make_coats.py` if the base character art changes.

---

## 10. Gotchas & rules (don't relearn the hard way)

1. **Editor → localStorage → must ⬇ export** to reach disk; I can only see files on disk.
2. **Never re-run `build_map.py`** — wipes hand/editor edits. `map2d.js` is canonical.
3. **Mojibake** when pasting data files into chat — clean `â…` back to `—`/curly quotes.
4. **LimeZu Free has no medical equipment** — computers/eye-machines/decor are drawn canvas primitives. Real sprites need the paid pack.
5. **License:** LimeZu Free is **non-commercial** — fine for a personal portfolio; revisit if the site ever monetises.
6. The dashboards are **stylised faithful copies**, not live — colours/labels mirror the real `/`, `/oct`, `/hvf`, `/vision` boards (real repo: `Desktop/Projects/appointment-dashboard`). They don't talk to OSCAR.

---

## 11. Known limitations / possible polish (within the game)

- Dashboard patient **card reason** still contains an em dash ("gl w/u — optos · HVF · VA · OCT") — bubbles were de-dashed, cards weren't (by request). Easy to change in `dash.js` `HERO.reason`.
- Seated patients are the **standing sprite + chair overlay** (reads fine at game zoom, slightly upright). True bent-leg 4-dir seated poses would need the **paid** Modern Interiors pack.
- `DECOR_KINDS` items are canvas primitives; decor sits at the mark tile (nudged toward the wall), not perfectly flush. Walker routes are hand-picked straight segments.
- The director `stage(idx)` and the bubble/timer maps are **hard-keyed to the 11-stop flow order** — change the flow, update them together.
- Filler dashboard patients/timers are cosmetic (real-time `tick()`); only the **hero's** room timer tracks the clinical clock.

---

## 12. History (condensed, for context only)

Built in order: rebuilt the 88×78 map from the blueprint (BFS through real corridors) → externalised map/flow/marks + built the `mapedit.html` editor → integrated LimeZu art (floors/walls/animated player) → fixed character facing (sheet order `right,up,left,down`) → rendered NPCs from marks as a shared **people catalog** → custom path drawing → big "populated clinic" pass (seat-row expansion, ~52% auto-occupancy, decor system, hall walkers) → character/decor fine-tune (4-dir seated-via-chair, machine-facing, white-coat doctors via `make_coats.py`) → **the live-dashboard split-screen** (this doc's main subject: `dash.css`/`dash.js`, the director, escorts, focus-dim, intro screen, narration bubbles, ~40-min spin-up clock, dashboard reveal, seated-alignment). Every round was screenshot-verified with **zero console errors**; the full run reaches the finale in ~2 min real-time at ~40:00 clinical.
