# shahmeershahid.com · HANDOFF

Single-page Astro site. A plain, customer-facing page for clinic owners, managers and
physicians: what Shahmeer changes inside a clinic, told as one clinic day in seven parts with
recreations of the real screens, then what changed, how he works, a few reassurances, and how
to get in touch. The earlier dark, scroll-pinned, WebGL portfolio is gone (git history before
branch `revamp-clear` has it).

## Run / build / deploy
```
npm run dev        # localhost:4321
npm run build      # -> dist/
npm run preview    # serves dist
```
- **Live at https://shahmeershahid.com** (GitHub Pages, repo `sh4hmeer/portfolio`, branch `main`).
  Every push to `main` runs `.github/workflows/deploy.yml` (single `build-deploy` job).
  `public/CNAME` keeps the custom domain. Node 24 local, 22 on CI, Astro 5.
- Pushing needs the `sh4hmeer` gh login (`gh auth switch`).
- `prototype/` (the pixel clinic game) stays in the repo for other projects that copied from it,
  but the site no longer embeds it and the build no longer mirrors it (`npm run sync-clinic` still
  exists if it is ever wanted again).

## How the page is meant to read (keep these)
- **Plain, first-person, and confident.** Describe what the work does; no slogans, no hype words,
  and NO hedging ("usually", "a little", "probably", "ask and I will give you a straight answer").
  Credibility first: every claim is stated flatly, with a number where one helps. Some rounding up
  is fine; the page is meant to be easy for someone who knows nothing about the software.
- **Broad, not clinic-only.** The intro speaks to any business with a messy workflow; the clinic
  day is the proof. The contact form asks only name, industry, and what slows the day down.
- **Light on how anything works.** Outcomes, not mechanisms. Nothing on the page should read as
  instructions for rebuilding it. Specific internals (polling, file watching, matching rules,
  model stats, email schedules, hardware) stay off the page.
- **Everyone shown is made up** (no disclaimer on the page). Never real EMR screenshots.
- **Light theme, 18 to 19 px body text, AAA contrast, one accent colour.** Dark is only for the
  "screens" (the board recreations).
- **No pinned or scroll-jacked sections, no carousels, no hover-only content, no accordions,
  nothing the visitor has to press to make a demo run.** Every visual moves slowly and
  continuously on its own, pauses off-screen and on a hidden tab, and goes static under
  `prefers-reduced-motion`.
- **Structure is visible:** a big numeral and a LOCATION (not a time of day; the tools loop all
  day) on each part, and a hand-drawn squiggle arrow between parts that lands on the next part's
  numeral (`nextFlip` prop on `DayStop` says which side that is).
- **Numbers read as measured, not made up:** per-person figure first (so a small clinic sees itself
  in it), then the clinic's own uneven total (380 patients a day, 3 h 40 min, 11 machines, 1 h 50
  min, 27 s, 2 h 50 min). Never round, even numbers like 400 / 4 hours / 200x / 2 hours. No table of
  contents, no captions under the screens, no explanatory grey notes.
- **Visuals size themselves by their own container** (`@container` queries on `.stop-visual` /
  `.hero-screen`, nested one on `.rc-lane`), not the viewport, because the same visual sits in
  columns of very different widths. Verified at 22 widths from 320 to 2560 px with the overflow
  audit (see below).
- **No em or en dashes anywhere** (standing rule). `grep -c "—\|–" dist/index.html` must be 0.
- Canadian spelling and vocabulary: EMR (not EHR), health card, front desk, exam room, scan.

## Page order (`src/pages/index.astro`)
`Hero` (#top; broad intro, then the "See my work in healthcare" lead-in) → `#day` wrapper with seven
`DayStop`s, each = numeral + time of day, ONE bold claim with a number, ONE grey line, one screen:
`#checkin` Kiosk · `#boards` LoungeBoard (wide, full-width under the text) · `#devices` DeviceRace ·
`#doctor` DoctorFlow (flip) · `#staff` FloorClock · `#map` FloorMap (flip) · `#nightly` NightlyReport
→ `Numbers` (#numbers, "Your numbers": the visitor types people-per-day and the per-person savings
measured at the clinic, 35 s check-in / 115 s per result / 27 s doctor, add up to hours a week; this
replaced the before/after rows and metric cards, which repeated the parts) → `HowIWork` (#how, broad
enough for any business, no "Right now" card: it revealed too much and could put off a clinic on a
different EMR) → `Questions` (#questions, "Good to know", 4 direct answers) → `Contact` (#contact;
two mailto buttons + a 3-field form, name / industry / what slows your day down, that composes a
mailto; links read "Email", never the address; no backend, nothing stored).
Top bar (`Base.astro`): brand, five links (hidden under 1000 px), "Get in touch" button, 2 px
page-progress line, scroll spy.

## Files
- `src/layouts/Base.astro` – head, fonts (Space Grotesk headings, IBM Plex Sans body, Plex Mono
  labels; all in package.json), top bar, footer, reveal + scroll-spy script.
- `src/styles/global.css` – tokens, layout, buttons, `.screen` frame, `.stop` grid (grid-areas text /
  visual / next / squig; `.flip` swaps columns AND column widths), `.stop-mark` numeral, `.fact`,
  `.next`, `.squig` arrow (draws in via `.rv.in`).
- `src/styles/visuals.css` – all visual styles, global on purpose (some DOM is built by JS).
- `src/components/DayStop.astro` – the part wrapper (numeral + time, `claim` / `detail` / `visual`
  slots, squiggle; props `flip`, `wide`, `last`).
- Visuals (self-contained, inline script, slow continuous loops):
  `Kiosk`, `LoungeBoard`, `DeviceRace`, `DoctorFlow`, `FloorClock`,
  `FloorMap` (SVG map with moving dots), `NightlyReport` (SVG bars + cycling highlight).
- `Numbers`, `HowIWork`, `Questions`, `Contact` – copy lives in each component.
- Privacy wording: "built to PHIPA and HIPAA standards" (PHIPA is Ontario's health privacy law).

## Checking a change
Build, then serve `dist` and run Playwright against it (the scripts used live in the session
scratchpad; they are short and easy to recreate):
1. Overflow audit: for widths 320 … 2560, scroll the whole page, then for every `.screen`, `.rc`,
   `.rp`, `.df-mon`, `.card`, `.fact`, `.toc-in`, `.cf-form` check `scrollWidth > clientWidth`,
   `scrollHeight > clientHeight`, and any descendant rect past the container rect. Also
   `document.documentElement.scrollWidth` vs `innerWidth`. Expect zero findings.
2. Element screenshots of each section at 1280 and 390 px, a full-page shot at 1440 / 1366 / 390,
   and a pass with `reduced_motion="reduce"`.
3. `grep -c "—\|–" dist/index.html` = 0; no console errors.

## Gotchas
- Bash cwd resets to `Desktop/Projects` each call; `cd .../fde-portfolio &&` first.
- Astro scopes `<style>`; JS-created nodes need global styles (hence visuals.css).
- `.stop.flip` must swap column widths, not just order, or the visual is squeezed into 5fr.
- Element screenshots right after `scrollIntoView` show the sticky top bar over the numeral; real
  anchor navigation is fine because every section has `scroll-margin-top`.
- Heredocs with non-ASCII characters can fail in the Windows Git Bash tool; write files with the
  editor tools or Python.
