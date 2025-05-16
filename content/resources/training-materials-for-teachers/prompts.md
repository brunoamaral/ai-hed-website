Here’s a multi-pass breakdown to get you from zero to a fully‐wired Hugo chapter/navigation/search feature. We’ll start with a high-level blueprint, then iteratively decompose into well-sized work chunks, and finally craft a sequence of code-generation prompts for each chunk.

⸻

1. High-Level Blueprint
	1.	Scaffold chapter files
	•	Create _index.md and 01-… through 07-… under the target folder.
	•	Populate front-matter (title, slug, summary, etc.) and copy content.
	2.	Overview page template
	•	Build a Hugo list template that renders search bar, PDF CTA, and chapter summaries.
	3.	Build-time Lunr index generation
	•	Write a Hugo data template (e.g. a partial) to emit JSON from each chapter’s .Title, .Params.summary, .Params.slug, .Plain.
	4.	Client-side Lunr search wiring
	•	Add Lunr.js script to overview template, fetch the static JSON, build index, wire the search input to filter the rendered list.
	5.	Chapter page layout & navigation
	•	Create (or update) a Hugo single-page layout with the two-column grid: content + sticky TOC + prev/next/overview nav.
	6.	Responsive TOC toggle
	•	Add JS + CSS to hide sidebar on small screens and display a floating “Show TOC” button that toggles an overlay.
	7.	Polish, error handling & testing
	•	Graceful fallbacks for fetch/index errors, test across breakpoints, browsers, and content edge cases.

⸻

2. First-Level Chunks

Chunk	Goal
A	Scaffold content files & front-matter
B	Overview page template (static list + CTA)
C	Build JSON index via Hugo
D	Integrate Lunr.js & simple client-side search
E	Chapter layout with static prev/next nav & sticky TOC sidebar
F	Responsive TOC overlay toggle
G	Error handling, testing, and refinements


⸻

3. Refined Sub-Steps

We’ll take each chunk and split into implementable steps of roughly 1–2 hours each:

A. Scaffold content files
	1.	Create empty _index.md with minimal front matter.
	2.	Copy 01-objectives.md … 07-recommended-ai-tools.md into place.
	3.	Populate each front matter with slug and summary.
	4.	Verify Hugo recognizes pages (hugo server).

B. Overview page template
	1.	Create layouts/_default/list.tpl (or override folder list).
	2.	Insert static HTML for search bar + PDF CTA.
	3.	Loop over .Pages to render title + summary blocks.
	4.	Style using Bootstrap 4 classes and verify markup.

C. Build JSON index
	1.	Create layouts/partials/lunr-index.json as an output template.
	2.	Loop through chapters; output valid JSON array.
	3.	Configure Hugo’s outputs front matter to generate lunr-index.json in static/js.
	4.	Run build; inspect JSON for correctness.

D. Client-side Lunr.js
	1.	Add Lunr.js to overview template (via CDN or local).
	2.	Write JS to fetch('/js/lunr-index.json') and build lunr index.
	3.	Hook #chapter-search input: on change, search index and gather results.
	4.	Filter/hide .chapter-item elements based on search results.

E. Chapter layout & nav
	1.	Create layouts/_default/single.tpl override.
	2.	Build two-column Bootstrap row: col-8 content, col-4 sidebar .toc.
	3.	Insert Hugo nav links (.Prev, .Next, overview).
	4.	Add {{ .TableOfContents }} in sidebar; apply position: sticky.

F. Responsive TOC toggle
	1.	Add floating <button> in template.
	2.	Write simple JS to toggle a CSS class on the .toc container.
	3.	Hide .toc on <md screens (d-none d-md-block).
	4.	Style overlay version for mobile.

G. Error handling & testing
	1.	In search JS, catch fetch/parse errors; display warning.
	2.	Manual QA: feature-test build and search.
	3.	Cross-browser, responsive breakpoints, nav edge cases.
	4.	Fix issues and document steps.

⸻

4. Code-Generation LLM Prompt Series

Below each prompt is self-contained, references prior outputs, and ends with “wire it up” instructions.

⸻

Prompt 1: Scaffold chapter files

You are Hugo site generator.
Create a new directory `content/resources/training-materials-for-teachers/` and inside it:
1) an `_index.md` file with front matter:
---
title: "Training Materials for Teachers"
layout: "page"
slug: "overview"
summary: "Learn how to adopt AI in teaching through seven detailed guideline chapters."
---
2) seven files named `01-objectives.md` through `07-recommended-ai-tools.md`.
Each file should have front matter containing `title`, `slug`, and `summary` placeholders, and the rest of the original single-page content under the respective header content converted into that file.
Ensure Hugo recognizes each page via `hugo server`.
Wire the new pages into the site structure.


⸻

Prompt 2: Overview template with static list + CTA

You are coding a Hugo template.
Create or override `layouts/_default/list.html` to render the overview page for `training-materials-for-teachers`:
1. Add a Bootstrap 4 form-row above the listing:
   - A search input `id="chapter-search"` with class `form-control` placeholder "Search chapters…"
   - A PDF download button styled `btn btn-lg btn-success font-weight-bold text-title`, linking to /downloads/AI-HED_WP3_Guidelines_course_development_final_Feb14_2025.pdf, with `<i class="fas fa-file-pdf"></i>` icon.
2. Loop over `.Pages` to output each chapter’s `<h3><a href="{{ .Permalink }}">{{ .Title }}</a></h3><p>{{ .Params.summary }}</p>`.
Ensure correct Bootstrap spacing. Preview in browser.


⸻

Prompt 3: Generate Lunr JSON at build time

You are coding Hugo build-time data generation.
Implement a partial `layouts/partials/lunr-index.json` that loops over pages in `section "resources/training-materials-for-teachers"`:
Output valid JSON array where each entry has:
  "title": .Title,
  "summary": .Params.summary,
  "slug": .Params.slug,
  "content": .Plain
Configure the site’s `outputs` in front matter so Hugo emits this partial to `static/js/lunr-index.json` during `hugo build`. Validate the JSON file.


⸻

Prompt 4: Wire Lunr.js search

You’re writing client JS for the overview page.
1. Include Lunr.js via CDN in the overview template.
2. In a script block:
   - Fetch `/js/lunr-index.json`.
   - Build a Lunr index indexing `title`, `summary`, and `content`, storing `slug`.
   - On `#chapter-search` input event, perform `index.search(query)` and get matching slugs.
   - Show only `.chapter-item` elements whose slug matches results; hide others.
   - If no matches, display a Bootstrap alert: “No chapters found. Try different keywords.”
3. Ensure errors in fetch or JSON parsing are caught; show a warning alert if they occur.
Wire this script into the page and verify real-time filtering.


⸻

Prompt 5: Chapter page layout & nav

You are coding a Hugo single-page layout.
Override `layouts/_default/single.html` for `training-materials-for-teachers`:
1. Wrap output in `<div class="row">` with:
   - `<div class="col-md-8">`: top nav bar with `.Prev`, overview link, `.Next`; then `{{ .Content }}`; then bottom nav bar same as top.
   - `<div class="col-md-4 d-none d-md-block">`: a `<div class="toc" style="position: sticky; top:1rem;">{{ .TableOfContents }}</div>`.
2. Use Bootstrap classes for spacing and nav styling.
3. Verify navigation links on all chapters, including edge cases.
Wire this template into Hugo and preview chapter pages.


⸻

Prompt 6: Responsive TOC toggle

You are adding mobile support.
In the chapter template:
1. Add a floating `<button id="toc-toggle" class="toc-toggle btn">` with `<i class="fas fa-list"></i>`, positioned via CSS in the top-right corner.
2. Write JS to toggle a class (e.g., `toc-visible`) on the `.toc` container.
3. In CSS, for screens `< md`, hide `.toc` by default and when `toc-visible` is present, display it as an overlay (covering part of the screen).
4. Ensure toggle button shows/hides the TOC overlay on mobile.
Wire CSS and JS into the build and test on mobile breakpoints.


⸻

Prompt 7: Error handling & testing

You’re adding robustness and QA.
1. In the search script, wrap fetch/index logic in `try/catch`; on error, insert a Bootstrap `.alert.alert-warning` above the search bar: “Search is currently unavailable. Please try again later.”
2. Manually test:
   - Prefilled index search terms.
   - No-results and error states.
   - Prev/Next/Overview links on chapter pages.
   - Sidebar sticky behavior on desktop.
   - TOC toggle on mobile.
   - Cross-browser checks in Chrome, Firefox, Safari, Edge.
3. Fix any CSS/JS bugs and document known limitations.
Wire these fixes into the repo and prepare a short README of how to test.


⸻

With this series of prompts—and each one building on the artifacts of the previous—you’ll be able to hand off to a code-generation LLM (or engineer) and walk through the entire implementation start to finish.