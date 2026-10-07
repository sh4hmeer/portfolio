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
- **Plain, first-person, unhurried.** Describe what the work does for the clinic; no slogans, no
  staccato "X. Y." headlines, no hype words. Headings are full sentences a manager would say.
- **Light on how anything works.** Outcomes, not mechanisms. Nothing on the page should read as
  instructions for rebuilding it. Specific internals (polling, file watching, matching rules,
  model stats, email schedules, hardware) stay off the page.
- **Everyone shown is made up** and the footer says so. Never real EMR screenshots.
- **Light theme, 18 to 19 px body text, AAA contrast, one accent colour.** Dark is only for the
  "screens" (the board recreations).
- **No pinned or scroll-jacked sections, no carousels, no hover-only content, no accordions,
  nothing the visitor has to press to make a demo run.** Every visual moves slowly and
  continuously on its own, pauses off-screen and on a hidden tab, and goes static under
  `prefers-reduced-motion`.
- **Structure is visible:** numbered "On this page" index under the hero, a big numeral and a
  time of day on each part, a "Next: ..." link closing each part, and a hand-drawn squiggle arrow
  between parts that leans toward where the next part's text starts.
- **Visuals size themselves by their own container** (`@container` queries on `.stop-visual` /
  `.hero-screen`, nested one on `.rc-lane`), not the viewport, because the same visual sits in
  columns of very different widths. Verified at 22 widths from 320 to 2560 px with the overflow
  audit (see below).
- **No em or en dashes anywhere** (standing rule). `grep -c "—\|–" dist/index.html` must be 0.
- Canadian spelling and vocabulary: EMR (not EHR), health card, front desk, exam room, scan.

## Page order (`src/pages/index.astro`)
`Hero` (#top) → `OnThisPage` → `#day` wrapper with seven `DayStop`s:
`#checkin` Kiosk · `#boards` TriageBoard (flip) · `#devices` DeviceRace · `#doctor` DoctorFlow (flip) ·
`#staff` FloorClock · `#map` FloorMap (flip) · `#nightly` NightlyReport
→ `Changed` (#changed) → `HowIWork` (#how) → `BeforeThis` (#before) → `Questions` (#questions,
"Good to know") → `Contact` (#contact; two mailto buttons + a form that composes a mailto, no
backend, nothing stored).
Top bar (`Base.astro`): brand, five links (hidden under 1000 px), "Get in touch" button, 2 px
page-progress line, scroll spy.

## Files
- `src/layouts/Base.astro` – head, fonts (Space Grotesk headings, IBM Plex Sans body, Plex Mono
  labels; all in package.json), top bar, footer, reveal + scroll-spy script.
- `src/styles/global.css` – tokens, layout, buttons, `.screen` frame, `.stop` grid (grid-areas text /
  visual / next / squig; `.flip` swaps columns AND column widths), `.stop-mark` numeral, `.fact`,
  `.next`, `.squig` arrow (draws in via `.rv.in`).
- `src/styles/visuals.css` – all visual styles, global on purpose (some DOM is built by JS).
- `src/components/DayStop.astro` – the part wrapper (numeral + time, h2, `text` and `visual` slots,
  Next link, squiggle).
- Visuals (self-contained, inline script, slow continuous loops):
  `LoungeBoard` (hero), `Kiosk`, `TriageBoard`, `DeviceRace`, `DoctorFlow`, `FloorClock`,
  `FloorMap` (SVG map with moving dots), `NightlyReport` (SVG bars + cycling highlight).
- `Changed`, `HowIWork`, `BeforeThis`, `Questions`, `Contact` – copy lives in each component.

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
