## Hugo Multi-Chapter Content Navigation & Search — Developer Specification

This document provides a detailed, end-to-end specification for implementing chapter-based content splitting, full-text search, and navigational enhancements on the Hugo static site located at `content/resources/training-materials-for-teachers/`. It is intended for a developer to immediately begin implementation.

---

### 1. Directory Structure & Filenames

Create seven chapter files under:

```
content/resources/training-materials-for-teachers/
├── _index.md                # Overview page (landing)
├── 01-objectives.md
├── 02-impact-of-ai.md
├── 03-pedagogical-approaches.md
├── 04-principles-of-course-design.md
├── 05-designing-courses.md
├── 06-legal-compliance-and-ethical-responsibility.md
└── 07-recommended-ai-tools.md
```

* Each chapter file’s front matter must include:

  * `title`: Human-readable title
  * `slug`: Two-digit prefix + dash + slug (e.g. `01-objectives`)
  * `summary`: One- or two-sentence summary for overview
  * Other existing metadata (authors, date, etc.) preserved

---

### 2. Overview (Landing) Page

**File:** `_index.md` in the same folder.

#### 2.1 Front Matter

```yaml
---
title: "Training Materials for Teachers"
layout: "page"
slug: "overview"
summary: "Learn how to adopt AI in teaching through seven detailed guidelines chapters."
---
```

#### 2.2 Layout & Components (Bootstrap 4)

1. **Search & PDF CTA Row** (above chapter list)

   ```html
   <div class="form-row align-items-center mb-4">
     <div class="col">
       <div class="input-group">
         <input id="chapter-search" type="text"
                class="form-control"
                placeholder="Search chapters…">
       </div>
     </div>
     <div class="col-auto">
       <a href="/downloads/AI-HED_WP3_Guidelines_course_development_final_Feb14_2025.pdf"
          class="btn btn-lg btn-success font-weight-bold text-title">
         <i class="fas fa-file-pdf"></i>&nbsp; Download this page as a PDF
       </a>
     </div>
   </div>
   ```

2. **Chapter List**

   ```html
   {{ range .Pages }}
   <div class="chapter-item mb-4">
     <h3><a href="{{ .Permalink }}">{{ .Title }}</a></h3>
     <p>{{ .Params.summary }}</p>
   </div>
   {{ end }}
   ```

3. **Optional Intro Section**

   * Placeholder above search row for hero text (to be filled later).

---

### 3. Full-Text Search via Lunr.js

#### 3.1 Index Generation (Build Time)

* **When:** During `hugo build`.
* **Output Path:** `static/js/lunr-index.json`.
* **JSON Structure:** Array of objects; each entry:

  ```json
  {
    "title": "Objectives",
    "summary": "Outlines the goals of these guidelines...",
    "slug": "01-objectives",
    "content": "Plain-text content of the chapter..."
  }
  ```
* **Content Extraction:** Use Hugo’s `.Plain` (plain-text from `.Content`).
* **Implementation:** Create a partial or data template that loops through chapters and writes JSON to the specified path.

#### 3.2 Client-Side Search (Runtime)

* **Fetch Index:** `fetch('/js/lunr-index.json')`.
* **Build Index:** Use Lunr to index `title`, `summary`, and `content` fields; store `slug` as metadata for link generation.
* **Search Input Handler:** On `input` event of `#chapter-search`, query Lunr and return matching document refs.
* **Results Rendering:** Replace or filter the `.chapter-item` list to show only matches; use `a.href = '/resources/training-materials-for-teachers/' + doc.slug + '/'`.
* **No Results UI:** Display a message: “No chapters found. Try different keywords.”

---

### 4. Chapter Page Layout & Navigation

Apply a two-column responsive layout (Bootstrap 4 grid):

```html
<div class="row">
  <div class="col-md-8">
    <!-- Top Navigation -->
    <nav class="chapter-nav mb-3">
      {{ with .Prev }}<a href="{{ .Permalink }}">‹ Previous Chapter</a>{{ end }}
      <a href="/resources/training-materials-for-teachers/">Back to Overview</a>
      {{ with .Next }}<a href="{{ .Permalink }}">Next Chapter ›</a>{{ end }}
    </nav>

    <!-- Content -->
    {{ .Content }}

    <!-- Bottom Navigation (same as top) -->
    <nav class="chapter-nav mt-4">
      {{ with .Prev }}<a href="{{ .Permalink }}">‹ Previous Chapter</a>{{ end }}
      <a href="/resources/training-materials-for-teachers/">Back to Overview</a>
      {{ with .Next }}<a href="{{ .Permalink }}">Next Chapter ›</a>{{ end }}
    </nav>
  </div>

  <div class="col-md-4 d-none d-md-block">
    <!-- Sticky Sidebar TOC -->
    <div class="toc" style="position: sticky; top: 1rem;">
      {{ .TableOfContents }}
    </div>
  </div>
</div>
```

#### 4.1 Responsive TOC Toggle

* **Hide sidebar** on screens `< md` (`.d-none d-md-block`).
* **Floating Toggle Button** (top-right corner):

  ```html
  <button id="toc-toggle" class="toc-toggle btn">
    <i class="fas fa-list"></i>
  </button>
  ```
* **Toggle Behavior:** Clicking shows/hides the TOC as an overlay or slide-in from right. Implement with minimal JavaScript and CSS (e.g., a hidden panel that toggles `display`).

---

### 5. Data Handling & Error Strategies

* **Index Fetch Errors:** If `/js/lunr-index.json` fails to load (404 or network error), capture in `catch()` and display:

  ```html
  <div class="alert alert-warning">
    Search is currently unavailable. Please try again later.
  </div>
  ```
* **Malformed JSON:** Validate JSON parse; on error, fallback to showing all chapters and log error to console.
* **Search Performance:** If index size is large, consider lazy-loading or web-worker indexing in future iterations.

---

### 6. Architecture Choices

* **Static Index at Build Time:** Ensures fast runtime performance and no server dependencies.
* **Client-Side Lunr.js:** Lightweight, runs fully in browser; ideal for small-medium indices.
* **Bootstrap 4 & FontAwesome:** Leverage existing CSS framework and icons.
* **Hugo Templates & Partials:** Use Hugo’s template system to generate both HTML and JSON data.

---

### 7. Testing & Validation Plan

1. **Build Verification**

   * Run `hugo build`; confirm `static/js/lunr-index.json` exists and is valid JSON.
   * Spot-check that each chapter entry includes correct `title`, `summary`, `slug`, `content`.

2. **Overview Page**

   * Manually test search input: typing keywords filters chapters as expected.
   * Test PDF CTA link and styling.
   * Test no-results state.

3. **Lunr Index Integrity**

   * Write unit tests (e.g., Jest) for index schema and search queries.
   * Validate that searching for a unique term in a chapter returns that chapter only.

4. **Chapter Navigation**

   * Verify Prev/Next/Overview links for all chapters, including edge cases (first chapter has no Previous, last has no Next).
   * Confirm URLs match slugs.

5. **TOC Sidebar**

   * Desktop: ensure TOC is visible, sticky, and scrolls with content.
   * Mobile (< md): sidebar hidden; toggle button shows and hides TOC overlay.

6. **Responsive Testing**

   * Use browser devtools to test key breakpoints (xs, sm, md, lg).
   * Confirm layout gracefully degrades to single column on mobile.

7. **Accessibility & SEO**

   * Ensure semantic HTML (e.g., `<nav>`, `<h3>`, `<button>`).
   * Confirm that each chapter page has correct `<title>` tags and meta `description` from front matter.

8. **Cross-Browser**

   * Test in latest Chrome, Firefox, Safari, Edge.

---

**End of Specification**