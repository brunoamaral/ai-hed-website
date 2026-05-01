# Implementation Plan — "From the Classroom" Section

Based on spec v2. Tasks are sequenced so each phase compiles cleanly before the next begins.

---

## Phase 0 — Scaffolding & data

### 0.1 — i18n: migrate existing keys and add new ones

The current `i18n/en.json` uses JSON format (`[{"id": "...", "translation": "..."}]`). The spec prescribes `i18n/en.yaml`. Hugo supports both formats in the same project; add `i18n/en.yaml` as a second file rather than converting the existing one.

- Create `i18n/en.yaml` with all `ftc_*` keys from the spec.
- Verify `i18n/pt.json` does not need parallel keys yet (out of scope per spec; add empty stubs with same ids so builds don't warn).

### 0.2 — Data directory

Create `data/from_the_classroom/` and add three JSON files with the full schema defined in the spec. For the initial commit:

- `raw` block populated from the interview JSON already produced.
- `edited` block present but empty (`"intro": "", "why_we_used_ai": "", ...`, `"pull_quotes": []`).

Files:
- `data/from_the_classroom/digital-transformation-foi.json`
- `data/from_the_classroom/digital-marketing-foi.json`
- `data/from_the_classroom/consumer-branding-hva.json`

Schema checklist per file:
- [ ] `metadata.slug` matches filename and intended URL segment
- [ ] `metadata.informants` is an array (two entries for Digital Transformation, one for the others)
- [ ] `metadata.portrait` paths point to `assets/images/from-the-classroom/educators/` — files absent initially, fallback renders instead
- [ ] `metadata.hook` is a non-empty string (required per spec)
- [ ] `metadata.institution_logo` uses existing paths under `static/images/partners/` (`FOI_horiz_EN_color-ai.svg`, `logo_amsterdam-uas.svg`)
- [ ] `raw.*` keys cover all eight top-level blocks from the interview template
- [ ] `edited.*` keys all present, all empty string or empty array

### 0.3 — Content stubs

Create `content/from-the-classroom/` with four files:

- `_index.md` — section index, front matter sets `title`, `type: from-the-classroom`, `layout: list`, no body content needed.
- `digital-transformation-foi.md` — front matter: `title`, `slug`, `draft: false`, `type: from-the-classroom`. Body empty; all content comes from the data file.
- `digital-marketing-foi.md` — same pattern.
- `consumer-branding-hva.md` — same pattern.

Front matter convention: each stub references its data file via a `dataFile` param so the single layout can look it up via `index site.Data.from_the_classroom .Params.dataFile`.

### 0.4 — Assets placeholders

- Create `assets/images/from-the-classroom/educators/` directory with a `.gitkeep`. Actual portraits land here later.
- Create `assets/scss/sections/_from-the-classroom.scss` as an empty file (imports added in Phase 2).

### 0.5 — Navigation

In `hugo.toml`, add after the existing "Adopting AI in Teaching" menu entry:

```toml
[[menu.main]]
  name = "From the Classroom"
  url = "/from-the-classroom/"
  parent = "AI in Higher Education"
  weight = 4
```

Check current menu weights to confirm no collision. The spec places this between "Adopting AI in Teaching" (weight 3) and whatever follows.

---

## Phase 1 — Partials (bottom-up, no layout yet)

Build all partials before wiring layouts so each can be reviewed independently.

### 1.1 — `informant-portrait-fallback.html`

Inputs: `informant` object (name, role), `size` (int, px), `institutionLogo` (path string).

Renders a square tile at `size × size`:
- Background: AI-HED accent colour (define as a CSS custom property `--ftc-accent`; set the hex value in `_from-the-classroom.scss`).
- Initials in white, heavy weight, centred; derived from `informant.name` by splitting on space and taking first char of each word (max 2 chars).
- Bottom-right: `<img>` of `institutionLogo` at 20px height, `aria-hidden="true"`.
- Same `border-radius` and `box-shadow` CSS classes as portrait `<img>`.
- Outer `<div>` carries `role="img"` and `aria-label="Portrait of {{ informant.name }}"`.

### 1.2 — `informant-portraits.html`

Inputs: `informants` array, `size` (int), `overlap` (bool), `institutionLogo`.

Logic:
- Loops over `informants`.
- For each: if `informant.portrait` non-empty, attempts Hugo image resource; renders `<img>` resized to `size × size` webp, `loading="{{ if $.eager }}eager{{ else }}lazy{{ end }}"`, `alt="Portrait of {{ informant.name }}"`.
- If portrait path empty or resource not found: calls `informant-portrait-fallback.html`.
- Duo + `overlap=true`: wraps portraits in a flex container, applies `-8px` negative margin-left on second portrait, matching the 8-12px overlap spec.

### 1.3 — `profile-hero.html`

Inputs: full data object (`.`), page context.

Renders:
- Portraits via `informant-portraits.html` with `size=160` (solo) or `size=140` (duo), `overlap=true` for duo, `eager=true`.
- `<h1>` = `metadata.course_title`.
- Byline `<p>`: uses `ftc_byline_solo` / `ftc_byline_duo` i18n keys depending on `len(metadata.informants)`.
- Institution badge: `<img>` of `metadata.institution_logo` at 36px height + `metadata.institution_short` text.
- Course-meta line: level · ECTS · semester · students (sourced from `raw.course_overview`).

### 1.4 — `profile-pullquote.html`

Inputs: `quote` object (`text`, `speaker`).

Renders:
- `<blockquote class="ftc-pullquote">` wrapping `<p>` for text and `<cite>` for speaker.
- Opening quote glyph `"` in `--ftc-accent` colour, `aria-hidden="true"`, display weight (class `ftc-pullquote__glyph`).

### 1.5 — `profile-section.html`

Inputs: `heading` (i18n key string), `content` (HTML-safe string or slice for the challenges list).

Renders:
- `<h2>` using `i18n heading`.
- If `content` is a string: `<p>` block.
- If `content` is a slice (challenges fallback): `<dl>` of challenge/management pairs.

### 1.6 — `profile-factsheet.html`

Inputs: full data object.

Renders a `<aside>` with `aria-label="{{ i18n "ftc_factsheet_title" }}"`:
- `<h2 class="ftc-factsheet__title">` (h2 semantically inside aside, not in the article flow — this is intentional per the spec's heading hierarchy note).
- Nine `<section>` blocks each with `<h3>`:
  1. Course basics — table or dl of title, institution, programme, level, ECTS, semester, students, prerequisites.
  2. Learning outcomes — `<ol>`.
  3. AI tools used — chip row.
  4. Assessment — boolean badge + details.
  5. Evaluation — text + KPI/formal booleans.
  6. Risk management — boolean badge + description if present.
  7. Challenges — full list with management notes as `<dl>`.
  8. Scalability — boolean badge + requirements if present.

Note: spec says factsheet heading hierarchy uses `<h3>` for groupings inside the factsheet. Ensure the factsheet `<h2>` is scoped to the aside so it does not disrupt the main article's h2 flow (use `aria-labelledby` on the aside, render the heading as `<h2>` visually but inside the landmark so AT announces it correctly).

### 1.7 — `educator-summary-card.html`

Inputs: data object for one course.

Renders a card `<article>`:
- Portrait(s) via `informant-portraits.html` at 120px.
- `<h2>` = course title.
- Byline + institution badge.
- Hook line.
- Lede excerpt: first ~50 words of `edited.intro`; if empty, use `raw.ai_usage_summary`; both truncated to 50 words via `truncatewords`.
- CTA link ("Read [first-name]'s story" or duo variant), using `ftc_read_story_solo` / `ftc_read_story_duo` i18n keys.
- Full card surface is a link (`<a>` wrapping the card with the CTA visible inside for accessibility).
- `data-umami-event="ftc_landing_card_click"` + `data-umami-event-slug="{{ .metadata.slug }}"` on the card link.

### 1.8 — `comparison-strip.html`

Inputs: slice of all data objects, sorted by `metadata.date` ascending.

Desktop (>= 992px): real `<table>`:
- `<caption>{{ i18n "ftc_landing_comparison_caption" }}</caption>`
- `<thead>` with eight `<th scope="col">` using i18n keys for each column.
- `<tbody>`: one `<tr>` per course; first cell `<th scope="row">` linked to the profile; remaining cells are `<td>`.
- Data sourced strictly from `raw.*`.
- `data-umami-event="ftc_comparison_row_click"` on each row link.

Mobile (< 992px): each row becomes a `<dl>` card with label/value pairs. Hidden via CSS class toggled at 992px breakpoint.

Accessibility: both the table and the DL cards are in the DOM; the non-active variant gets `aria-hidden="true"` and `class="d-none d-lg-table"` / `d-lg-none` pattern (Bootstrap responsive utilities already present in the theme).

### 1.9 — `from-the-classroom-teaser.html`

Inputs: site context (reads `site.Data.from_the_classroom` itself).

Logic:
- Collect all values from `site.Data.from_the_classroom`, sort by `metadata.date` desc, take first 3.
- If count = 0: render nothing (empty string, no wrapper).
- Otherwise: render the teaser section.

Structure:
- `<section class="section ftc-teaser py-5">` with `data-umami-event="ftc_homepage_teaser_view"` on the section (fires on viewport entry via Intersection Observer — inline `<script>` block, ~8 lines, no new dependency).
- `<h2>{{ i18n "ftc_section_title" }}</h2>` + 1-line intro.
- Row of up to 3 small educator cards (Bootstrap col-12 col-md-6 col-lg-4):
  - Portrait(s) via `informant-portraits.html` at 80px, `overlap=true` for duo, `eager=false`.
  - Name(s), course title, institution short, hook line.
  - `data-umami-event="ftc_homepage_card_click"` + `data-umami-event-slug` on each card link.
- "Read all stories" CTA button → `/from-the-classroom/`, `data-umami-event="ftc_homepage_cta"`.
- Portrait containers have fixed square dimensions set in CSS so portrait load doesn't cause layout shift.

---

## Phase 2 — Layouts

### 2.1 — `layouts/from-the-classroom/single.html`

Extends `baseof.html`. Reads data file via front matter `dataFile` param:

```
{{ $data := index site.Data.from_the_classroom .Params.dataFile }}
```

Main column (~col-md-8):
1. `{{ partial "from-the-classroom/profile-hero.html" $data }}`
2. Lede: `edited.intro` or fallback to `raw.ai_usage_summary`.
3. Pull quote 1 (if `edited.pull_quotes` has index 0).
4. Section "Why we used AI" via `profile-section.html`.
5. Section "How it worked" via `profile-section.html`, followed by tool chips row from `raw.implementation_details.tools_used`.
6. Pull quote 2 (if `edited.pull_quotes` has index 1).
7. Section "What changed for students".
8. Section "What we struggled with" — challenges fallback renders as `<dl>` pairs.
9. Section "What we learned".
10. Footer: institution credit, interview date, prev/next nav.

Prev/next nav:
- Collect all profiles from `site.Data.from_the_classroom`, sort by `metadata.date` ascending.
- Find current index; prev = `[index-1]` mod 3, next = `[index+1]` mod 3.
- Each nav item: portrait thumb at 48px + name(s) + course title.
- `data-umami-event="ftc_profile_prevnext_click"` with `from_slug`, `to_slug`, `direction` attributes.

Sidebar (~col-md-4):
- `{{ partial "from-the-classroom/profile-factsheet.html" $data }}`
- Sticky: `position: sticky; top: calc(var(--header-height, 80px) + 24px)` in SCSS.
- On mobile (< 992px): factsheet moves below article body. Achieve via CSS `order` on flexbox/grid row rather than duplicating the DOM.
- Intersection Observer fires `ftc_profile_factsheet_engagement` when factsheet enters viewport; `slug` property from `$data.metadata.slug`. Inline `<script>`, no new dependency.

### 2.2 — `layouts/from-the-classroom/list.html`

Extends `baseof.html`. Reads all data from `site.Data.from_the_classroom`:

```
{{ $profiles := slice }}
{{ range $key, $val := site.Data.from_the_classroom }}
  {{ $profiles = $profiles | append $val }}
{{ end }}
{{ $profiles = sort $profiles "metadata.date" }}
```

Order:
1. Section header: h1 "From the Classroom" + subhead (i18n keys).
2. `{{ partial "from-the-classroom/comparison-strip.html" $profiles }}`
3. Educator cards: loop `$profiles`, render `{{ partial "from-the-classroom/educator-summary-card.html" . }}`.
4. Closing block: paragraph + link to AI-HED project page.

### 2.3 — Homepage integration

In `content/_index.html`, add the teaser partial call between the `{{< latest-posts ... "Project Updates" ... >}}` shortcode and the `{{< team-cta >}}` block:

```
{{ partial "homepage/from-the-classroom-teaser.html" . }}
```

The partial self-guards against an empty data directory (Phase 1.9 logic).

---

## Phase 3 — Styles

### 3.1 — `assets/scss/sections/_from-the-classroom.scss`

All new CSS for the section. Budget: < 6KB gzipped.

Key rules:
- `--ftc-accent`: hex value for the AI-HED accent colour (check `.claude/skills/ai-hed-brand-guidelines/` for the authoritative value; fall back to the green used in existing CTAs if the skill file is not available).
- `.ftc-portrait` — square, same `border-radius` and `box-shadow` as existing project-update card images.
- `.ftc-portrait-fallback` — background `var(--ftc-accent)`, initials centered, corner logo.
- `.ftc-portrait-duo` — flex container, second child gets `margin-left: -10px`.
- `.ftc-pullquote` — oversized `"` glyph in `var(--ftc-accent)`, display-weight body.
- `.ftc-card` — same hover lift (`transform: translateY(-2px)` + shadow) as existing Project Update cards.
- `.ftc-factsheet` — sticky sidebar rules; `overflow-y: auto; max-height: calc(100vh - var(--header-height, 80px) - 48px)` to prevent overflow on short screens.
- Comparison table: responsive rules, row hover state linking visually to the CTA.
- At < 992px: factsheet moves below article (`order: 2`), main column `order: 1`.
- Portrait placeholder reserves square space: `width: Xpx; height: Xpx; flex-shrink: 0` on all portrait containers so there is no layout shift when images load.

### 3.2 — Wire SCSS into build

The theme's `baseof.html` uses Hugo Pipes to concatenate SCSS. Check how `now-ui-kit.scss` imports partials; add:

```scss
@import "sections/from-the-classroom";
```

to the project-level SCSS entry point (or create one at `assets/scss/main.scss` that imports both the theme's kit and the new partial, then reference `main.scss` in `baseof.html`).

Verify the theme already has a project-level override point; if not, override `baseof.html` in `layouts/baseof.html` (already exists) to inject the new stylesheet as a second compiled resource.

---

## Phase 4 — Analytics

All event firing is inline JavaScript using the existing Umami `window.umami.track()` API. No new script tags needed; Umami is already loaded.

### 4.1 — Teaser viewport event

In `from-the-classroom-teaser.html`:

```html
<script>
(function(){
  var el = document.getElementById('ftc-teaser');
  if(!el || !window.IntersectionObserver) return;
  var fired = false;
  new IntersectionObserver(function(entries){
    if(!fired && entries[0].isIntersecting){
      fired = true;
      if(window.umami) window.umami.track('ftc_homepage_teaser_view');
    }
  }, {threshold: 0.5}).observe(el);
})();
</script>
```

Add `id="ftc-teaser"` to the section element.

### 4.2 — Factsheet viewport event

Same pattern in `profile-factsheet.html`, firing `ftc_profile_factsheet_engagement` with `{ slug: '...' }`.

### 4.3 — Click events

Card and row clicks use `data-umami-event` attributes (declarative). Umami auto-picks these up. No JS needed.

For prev/next direction, add `data-umami-event-from_slug`, `data-umami-event-to_slug`, `data-umami-event-direction` attributes on the nav links in the single layout.

---

## Phase 5 — Accessibility pass

After initial build, verify:

- [ ] Comparison table: `<caption>`, `<thead>`, all `<th scope="col">` present, first `<td>` of each row is `<th scope="row">`.
- [ ] Mobile DL variant has same data as table (no missing columns).
- [ ] Pull quotes: `<blockquote>` + `<cite>`.
- [ ] Profile page h1 appears once (course title in `profile-hero.html`).
- [ ] Factsheet sidebar is in DOM order after article body; sticky via CSS only.
- [ ] Portrait fallback: `role="img"`, `aria-label="Portrait of [name]"`.
- [ ] Decorative glyphs: `aria-hidden="true"`.
- [ ] All institution logo `<img>` tags have descriptive `alt` or `aria-hidden="true"` if decorative.
- [ ] Full-card-surface links include a visually-present CTA text child element (not icon-only).
- [ ] Run `hugo --minify` and confirm zero template errors.
- [ ] Lighthouse a11y >= 95 on a profile page.
- [ ] Lighthouse performance >= 90 on a profile page.

---

## Phase 6 — Content data entry

*After* the frontend ships with raw fallbacks rendering cleanly, Bruno fills in `edited.*` fields per profile. This is editorial work, not a development task. Each profile transitions independently:

- Fill `edited.intro` → hero lede transitions from interview prose to first-person narrative.
- Fill remaining `edited.*` fields one by one.
- Add pull quotes to `edited.pull_quotes[]`.
- `hugo --minify` + push → live.

No code changes required for this phase.

---

## Open questions to resolve before Phase 1

1. **SCSS entry point**: Does the project currently have a project-level `assets/scss/main.scss` that overrides the theme's SCSS, or does `layouts/baseof.html` reference the theme's SCSS directly? Check before writing Phase 3.2 to avoid a double-compile issue.

2. **`raw.*` key names from interview JSON**: The spec shows top-level keys (`course_overview`, `ai_usage_summary`, etc.) but the actual interview JSON may use different nested structure. Confirm the exact key paths in the three interview JSONs before writing the factsheet partial to avoid empty renders.

3. **`metadata.date` vs editorial order**: Spec recommends date-ascending; flag if any two profiles share the same date (would make sort non-deterministic). Consider adding a `metadata.order` int field as a tiebreaker.

4. **AI-HED accent colour hex**: Needed in Phase 3. The brand guidelines skill file at `.claude/skills/ai-hed-brand-guidelines/SKILL.md` should be the canonical source. Confirm before writing SCSS.

5. **`assets/` vs `static/` for portraits**: Spec says `assets/images/from-the-classroom/educators/`. This requires Hugo image processing; portraits must be under `assets/`. Confirm this is the right call vs. `static/images/from-the-classroom/educators/` (static would skip processing but lose webp conversion).

---

## Acceptance checklist (mirrors spec)

- [ ] Three JSON files in `data/from_the_classroom/` with schema (`raw` populated, `edited` empty)
- [ ] Three content stubs + `_index.md` in `content/from-the-classroom/`
- [ ] Profile page renders for each of the three slugs at `/from-the-classroom/<slug>/`
- [ ] Profile main column falls back to `raw.*` cleanly when `edited.<key>` is missing or empty string
- [ ] Profile factsheet sidebar renders all listed sections from `raw.*`
- [ ] Duo case renders two portraits, two-name byline, and "Larisa and Ana's story" CTA
- [ ] Portrait fallback renders cleanly when image files are absent
- [ ] Landing page renders comparison strip as a real `<table>` with proper semantics
- [ ] Comparison strip flips to stacked DL card layout below 992px without losing data
- [ ] Three educator cards on landing link to profiles; full-card click and visible CTA both work
- [ ] Homepage teaser renders between "Project Updates" and team block
- [ ] Teaser renders nothing when `data/from_the_classroom/` is empty
- [ ] All UI strings live in `i18n/en.yaml`; no hardcoded copy in templates
- [ ] Nav menu shows "From the Classroom" under "AI in Higher Education"
- [ ] Lighthouse a11y >= 95 on profile page
- [ ] Lighthouse performance >= 90 on profile page
- [ ] `hugo --minify` passes with no errors and no broken inter-section links
