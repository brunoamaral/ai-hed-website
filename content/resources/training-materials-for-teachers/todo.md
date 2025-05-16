# Implementation TODO Checklist

Use this as a step-by-step guide while implementing the multi‑chapter navigation, search, and TOC features on your Hugo site.

---

## A. Scaffold Content Files

* [ ] Create directory `content/resources/training-materials-for-teachers/` if not existing
* [ ] Add `_index.md` (overview) with front matter:

  ```yaml
  title: "Training Materials for Teachers"
  layout: "page"
  slug: "overview"
  summary: "Learn how to adopt AI in teaching through seven detailed guideline chapters."
  ```
* [ ] Copy single-page content into separate files:

  * `01-objectives.md` (slug: `01-objectives`, summary)
  * `02-impact-of-ai.md` (slug: `02-impact-of-ai`, summary)
  * `03-pedagogical-approaches.md` (slug: `03-pedagogical-approaches`, summary)
  * `04-principles-of-course-design.md` (slug: `04-principles-of-course-design`, summary)
  * `05-designing-courses.md` (slug: `05-designing-courses`, summary)
  * `06-legal-compliance-and-ethical-responsibility.md` (slug: `06-legal-compliance-and-ethical-responsibility`, summary)
  * `07-recommended-ai-tools.md` (slug: `07-recommended-ai-tools`, summary)
* [ ] Populate each file’s front matter with `title`, `slug`, `summary`, and preserve other metadata
* [ ] Run `hugo server` and confirm pages render under `/resources/training-materials-for-teachers/<slug>/`

---

## B. Overview Page Template

* [ ] Create/override `layouts/_default/list.html` (or specific to this section)
* [ ] Insert Bootstrap 4 row with search input and PDF CTA:

  ```html
  <div class="form-row align-items-center mb-4">…</div>
  ```
* [ ] Loop through `.Pages` to render each chapter item:

  ```html
  {{ range .Pages }}…{{ end }}
  ```
* [ ] Style items with Bootstrap classes, verify spacing and typography
* [ ] Preview overview page to ensure static rendering is correct

---

## C. Build-Time Lunr Index Generation

* [ ] Create partial `layouts/partials/lunr-index.json` that:

  * Loops through `where.Section "training-materials-for-teachers"`
  * Emits valid JSON array with fields: `title`, `summary`, `slug`, `content`
* [ ] Add `outputs` configuration in front matter or `config.toml` to write this partial to `static/js/lunr-index.json`
* [ ] Run `hugo build` and confirm `static/js/lunr-index.json` exists and is valid

---

## D. Client-Side Lunr.js Integration

* [ ] Add Lunr.js library (via CDN or local) to the overview template
* [ ] Write JavaScript to:

  * Fetch `/js/lunr-index.json`
  * Build Lunr index on `title`, `summary`, and `content`, keep `slug`
  * Hook to `#chapter-search` input event to run `index.search(query)`
  * Filter DOM `.chapter-item` elements by matching `slug`
  * Display a “No chapters found” Bootstrap alert if `index.search` yields no results
* [ ] Implement error handling:

  * `catch` on fetch/parse, display an alert “Search is currently unavailable. Please try again later.”
* [ ] Test search functionality with sample keywords

---

## E. Chapter Page Layout & Navigation

* [ ] Override `layouts/_default/single.html` for this section
* [ ] Implement two-column grid:

  * **Left (`col-md-8`)**: top nav (`Prev`, `Overview`, `Next`), `{{ .Content }}`, bottom nav
  * **Right (`col-md-4 d-none d-md-block`)**: `<div class="toc" style="position: sticky; top:1rem;">{{ .TableOfContents }}</div>`
* [ ] Use Hugo’s `.Prev` and `.Next` to generate navigation; handle edge cases (first/last)
* [ ] Preview multiple chapter pages to confirm consistency

---

## F. Responsive TOC Toggle for Mobile

* [ ] Add floating toggle button in chapter template:

  ```html
  <button id="toc-toggle" class="toc-toggle btn"><i class="fas fa-list"></i></button>
  ```
* [ ] Write JS to toggle a `toc-visible` class on the `.toc` container
* [ ] Update CSS:

  * Hide `.toc` by default on `<md` screens (`d-none d-md-block`)
  * When `toc-visible` is present, display the `.toc` overlay
  * Style overlay appearance (width, background, z-index)
* [ ] Test TOC toggle on mobile breakpoints

---

## G. Error Handling, Polishing & Testing

* [ ] Review search script error paths and alert displays
* [ ] Test:

  * Hugo build errors
  * Fetch errors for missing/malformed JSON
  * Search result edge cases
  * Navigation link correctness (Prev/Next)
  * Layout on desktop and mobile
  * Cross-browser compatibility
* [ ] Fix any styling or JS bugs
* [ ] Document setup and testing steps in a short README.md

---

**End of TODO**
