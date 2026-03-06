# AI-HED Website

Hugo-based website for the AI-HED project (Artificial Intelligence in Higher Education Teaching and Learning).

---

## Prerequisites

- [Hugo extended](https://gohugo.io/installation/) v0.100+
- Python 3.10+ (only needed to regenerate heatmap data)

---

## Development

```bash
hugo server --disableFastRender
```

The site is served at `http://localhost:1313`.

## Build

```bash
hugo --minify
```

Output is written to `public/`.

---

## AI Tools Heatmap

The interactive heatmap at `/resources/ai-tools-heatmap/` maps 44 AI-based tools against the 21 DigComp 2.2 competencies and Bloom's Taxonomy levels. The source data lives outside this repository in the `HeatMap v3` project folder.

### Data files

| File | Description |
|------|-------------|
| `HeatMap v3/data.csv` | Source matrix — 44 tools × 21 competency codes, values are Bloom levels 0–6 |
| `HeatMap v3/Data/competencies.py` | Competency metadata (full names, group labels, descriptions) |
| `content/resources/ai-tools-heatmap/heatmap-data.json` | Generated JSON consumed by the browser — **do not edit by hand** |

### Regenerating the heatmap data

Run this whenever `data.csv` or `competencies.py` is updated:

```bash
cd "/path/to/HeatMap v3"
python generate_json.py
```

The script writes `heatmap-data.json` directly into the Hugo page bundle at:

```
content/resources/ai-tools-heatmap/heatmap-data.json
```

Then rebuild the site:

```bash
cd /path/to/ai-hed-website
hugo --minify
```

### How the heatmap works

- **Layout template**: `layouts/page-heatmap.html` — contains all CSS, HTML, and JavaScript inline. No extra build steps or npm dependencies.
- **Data loading**: the page fetches `heatmap-data.json` at runtime via `fetch()`.
- **Colors**: 5 competency groups × 7 Bloom-level shades (defined in `HeatMap v3/heatmap.py` and mirrored in the layout).
- **Patterns**: CSS gradient overlays reproduce the hatching patterns from the original PDF output (vertical lines, diagonals, dots, crosshatch, etc.).
- **Filters**: group dropdown, Bloom level dropdown, and tool name search — all composable.

---

## Makefile targets

| Target | Description |
|--------|-------------|
| `make publish` | Push `main` branch to origin |
| `make sync-main` | Pull latest `main` from origin |
| `make sync-testing` | Merge `testing` into `main` |
