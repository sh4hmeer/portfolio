# shahmeershahid.com · HANDOFF

Single-page Astro site. Since the 2026-10-07 revamp it is a **plain, customer-facing page
for clinic owners, managers and physicians**: what Shahmeer changes inside a clinic, shown as
one clinic day in seven parts, with recreations of the real tools, then the numbers, how he
works, questions, and contact. The previous dark, scroll-pinned, WebGL portfolio is gone
(history: commits before `revamp-clear`; the old components were deleted, not hidden).

## Run / build / deploy
```
npm run dev        # localhost:4321 (predev mirrors prototype/ -> public/clinic/)
npm run build      # -> dist/
npm run preview    # serves dist
```
- **Live at https://shahmeershahid.com** (GitHub Pages, repo `sh4hmeer/portfolio`, branch `main`).
  Every push to `main` runs `.github/workflows/deploy.yml` (single `build-deploy` job: `npm ci`,
  `npm run build`, upload `dist`, deploy). `public/CNAME` keeps the custom domain. Node 24 local,
  22 on CI, Astro 5.
- The revamp was built on branch **`revamp-clear`**. Merge to `main` (or push the branch and
  open a PR) to deploy. Pushing needs the `sh4hmeer` gh login (`gh auth switch`).
- Screenshot harness used during the revamp lives in the session scratchpad, not the repo:
  Playwright (`python -m playwright`) against `astro preview` at three viewports. Pattern: start
  preview on a spare port, `goto`, scroll through, `screenshot(full_page=True)`, plus per-section
  element screenshots. Easy to recreate.

## Design rules (from the 2026-10 research, keep these)
Two research passes (business sites that stay enjoyable; copy and credibility for a one-person
clinic-tech service) converged on these. They are the reason the page looks the way it does.
1. **Light theme, 18 to 19 px body, AAA contrast, one accent colour.** Older and less technical
   readers; NN/g seniors + WCAG. Dark is reserved for the "screens" (board recreations).
2. **No pinned or scroll-jacked sections, no carousels, no hover-only content, no accordions.**
   Entrance fades only (450 ms), everything honours `prefers-reduced-motion` (visuals go static).
3. **The hero is one plain-English outcome sentence** ("The clinic that always knows where every
   patient is."). "Forward deployed engineer" never appears in the H1; it is explained once in
   "How I work".
4. **Proof is cut by the fold.** The lounge board sits directly under the hero text so the first
   screen always shows the page continues (NN/g "illusion of completeness").
5. **A visible, numbered "On this page" index** right under the hero, and **every part ends with
   a "Next: ..." link**. Less technical visitors never have to discover that there is more below.
6. **The spine is one clinic day** (7:55 am check-in ... 11:00 pm nightly report), each part = full-
   sentence heading, two short paragraphs, one green "fact" box with a precise number and how it
   was measured, one recreation of the real tool.
7. **Numbers only inside sentences with a method footnote**; never a stats wall. All numbers on the
   page are real and sourced from the project notes (see "Facts used" below).
8. **Scarcity as a calm logistical fact, never a pitch**: "one clinic at a time", "Next start: one
   clinic, 2027", "by introduction". Never "limited spots", "exclusive", countdowns.
9. **First person ("I")**, Canadian spelling and vocabulary (EMR not EHR, health card, daysheet,
   patient flow, front desk, exam room). Avoid: AI, ML, platform, integration, provider.
10. **Primary CTA "See it running" (20-minute video call); secondary "Ask about 2027".**
11. **NO EM OR EN DASHES anywhere** (standing rule). Verify: `grep -c "—\|–" dist/index.html` = 0.
12. **Everything shown is fictional** (patients, staff, report numbers) and the footer says so. The
    kiosk wording is the real kiosk's wording. Never put real OSCAR screenshots on the site (PHI).

## Page order (index.astro)
`Hero` (#top) → `OnThisPage` → `#day` wrapper with seven `DayStop`s:
`#checkin` Kiosk · `#boards` TriageBoard (flip) · `#devices` DeviceRace · `#doctor` DoctorFlow (flip) ·
`#staff` FloorClock · `#map` ClinicMap (flip) · `#nightly` NightlyReport
→ `Changed` (#changed: before/after rows + 4 numbers) → `HowIWork` (#how: 4 steps + status / fit /
not-a-fit cards) → `BeforeThis` (#before: 3 earlier employers) → `Questions` (#questions, 6 Q&As, all
visible) → `Contact` (#contact: two mailto CTAs + a fit-check form that composes a mailto; the site is
static so there is no backend and nothing is stored).
Top bar (`Base.astro`): brand, 5 links (hidden under 1000 px), "Ask about 2027" button, 2 px page-
progress line. Scroll spy marks the current section.

## Files
- `src/layouts/Base.astro` – head, fonts (Space Grotesk headings, IBM Plex Sans body, Plex Mono
  labels; all already in package.json), top bar, footer, reveal + scroll-spy script.
- `src/styles/global.css` – tokens (`--accent #1d7a4b`, `--ink`, board palette `--s-*`), layout,
  buttons, `.screen` dark frame, `.stop` grid (grid-areas: text / visual / next; `.flip` swaps columns
  AND column widths so the visual always gets the 7fr side), `.fact`, `.next`.
- `src/styles/visuals.css` – all visual-component styles, kept global on purpose (several visuals
  build DOM from JS, which Astro-scoped styles would miss). Prefixes documented at the top.
- `src/components/DayStop.astro` – the part wrapper (eyebrow "Part n of 7 · time", h2, slots `text` and
  `visual`, Next link).
- Visuals (each self-contained, inline script, pauses off-screen and on hidden tab, static under
  reduced motion):
  - `LoungeBoard.astro` (hero): 3 doctor cards with the 5 real status circles + waiting list; a
    patient advances a step every 4.5 s, timers tick.
  - `Kiosk.astro`: 4 screens (card / reading / confirm / seated), auto-steps, step buttons, Replay.
  - `TriageBoard.astro`: doctors' purple counts, 3 imaging rooms, ready-for-scan queue; a scan
    finishes every 6 s and the next in line takes the room. Phone: queue trimmed to 3 cards.
  - `DeviceRace.astro`: typed-by-hand lane (10x speed, one typo fixed) vs script lane (0.5 s). Auto-
    runs once at 45% visibility, "Run again" button; result strip appears at the end.
  - `DoctorFlow.astro`: two stacked monitors; cursor clicks the purple row, chart opens beside the
    board, FORUM + Optos windows open on monitor 2, "opened in 2.4 s" pill. Loops every 7.5 s.
  - `FloorClock.astro`: stations list + time clock + "sent on its own" emails; last-event line cycles.
  - `ClinicMap.astro`: poster + "Play the walkthrough" button that inserts the iframe
    (`/clinic/clinic2d.html`, mirrored from `prototype/` by `scripts/sync-clinic.mjs`). Under 760 px
    it opens the game in a new tab instead.
  - `NightlyReport.astro`: document-style card, SVG bar chart (bars draw in via `.rv.in`), findings,
    "try tomorrow", footer. Illustrative numbers.
- `Changed.astro`, `HowIWork.astro`, `BeforeThis.astro`, `Questions.astro`, `Contact.astro` – copy
  lives in each component's frontmatter arrays; edit there.
- `src/lib/url.js` – `withBase()` for the game path. `prototype/` stays canonical for the game.

## Facts used on the page (sources: project memory notes, 2026-10-07)
- Device results: biometer exports → OSCAR, running since May 2026; 8 fields, 55 keystrokes by hand;
  ~0.5 s by script vs ~2 min typed ("about 200x"). ~12 devices export to one share.
- Check-in: card kiosk live at the front desk 2026-09-23; decision 2026-09-11 → live in 12 days;
  one confirmation tap; chart address/phone updated from a newer card.
- Doctor flow: FORUM/Optos/eChart open in ~2 to 13 s, down from ~33 s (speed rework 2026-08-14).
- Time clock: live 2026-09-29; manager emails 9:00 / 17:00; bi-weekly PDF to the accountant;
  uAttend history imported.
- Model: 5,941 "who's next" decisions over 18 clinic days; vision ranker 51.4% top-1 vs 24.1% best
  baseline; age never used in ordering; suggestion-first, staff decide.
- Boards poll the OSCAR daysheet ~every 10 s; Done/room actions write back to OSCAR.
If any of these change, update the fact box in `index.astro` AND the matching card in `Changed.astro`.

## Things to confirm with Shahmeer (written as plausible defaults)
- "What does it cost?" answer (fixed engagement, scoped after the first week on the floor).
- "I read and answer every message myself." and the 20-minute call framing.
- "Next start: one clinic, 2027" and "by introduction".
- LinkedIn handle `shahmeer-shahid-` (carried over from the old site, still unverified).
- Optional: a real photo (him, or the kiosk / a board in the actual waiting room) under the hero;
  research ranked a real photo above any device frame. None exists in the repo, so none is used.

## Gotchas
- Bash cwd resets to `Desktop/Projects` each call; `cd .../fde-portfolio &&` first.
- Astro scopes `<style>` to build-time elements; JS-created nodes need global styles (hence visuals.css).
- The `.stop.flip` rule must swap column widths, not just order, or the visual is squeezed into 5fr
  (this clipped the imaging board's third column once).
- Element screenshots taken right after `scrollIntoView` show the sticky top bar over the eyebrow;
  real anchor navigation is fine because every section has `scroll-margin-top`.
- Heredocs with non-ASCII box characters failed in the Windows Git Bash tool; write files with the
  editor tools or Python instead.
