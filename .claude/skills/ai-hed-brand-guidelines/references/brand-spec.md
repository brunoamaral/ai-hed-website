# AI-HED Brand Specifications

## Project Information

**Full name**: Artificial Intelligence in Higher Education Teaching and Learning
**Short name**: AI-HED
**Project code**: 2024-1-NL01-KA220-HED-000248874
**Programme**: Erasmus+ KA2 (Cooperation among organisations and institutions)
**Duration**: 24 months (1 September 2024 – 31 August 2026)

### Consortium Partners
- Amsterdam University of Applied Sciences (AUAS) — applicant organisation
- University of Applied Sciences BFI Vienna (UAS-BFI)
- School of Communication and Media Studies, Polytechnic University of Lisbon (IPL / ESCS)
- University of Zagreb, Faculty of Organization and Informatics (UNIZG)

### Communication Contacts (ESCS team)
- Ana Luísa Raposo — araposo@escs.ipl.pt
- Bruno Amaral Tiago — btiago@escs.ipl.pt
- Tatiana Nunes — tnunes@escs.ipl.pt

## Colour Palette

### Primary Colour

**Solid Green**
- Hex: `#628c68`
- RGB: 98, 140, 104
- Usage: primary brand colour, solid backgrounds, borders, accents

### Gradient Colour Map

The icon uses a multi-stop gradient flowing from top-left (lighter) to bottom-right (darker). Each node of the icon has its own gradient pair. The overall range spans:

| Position | Hex | RGB | Usage |
|----------|-----|-----|-------|
| Lightest | `#63a376` | 99, 163, 118 | Top-left gradient start |
| Light-mid | `#5a956c` | 90, 149, 108 | Upper nodes |
| Mid | `#4e835e` | 78, 131, 94 | Central nodes |
| Mid | `#4a7c5a` | 74, 124, 90 | Central nodes |
| Mid-dark | `#467655` | 70, 118, 85 | Lower-central nodes |
| Dark-mid | `#3e6a4b` | 62, 106, 75 | Lower nodes |
| Dark | `#34593f` | 52, 89, 63 | Bottom-right area |
| Darkest | `#2c4d36` | 44, 77, 54 | Bottom-right gradient end |

**Simplified gradient for CSS/presentations** (two-stop approximation):
```css
background: linear-gradient(135deg, #63a376 0%, #2c4d36 100%);
```

### Supporting Colours

**White**
- Hex: `#ffffff`
- Usage: text on green backgrounds, light backgrounds

**Black**
- Hex: `#000000`
- Usage: logo text, headings on light backgrounds, body text

## Typography

### Font Selection Rationale
1. Available in online Office apps and Microsoft tools
2. Facilitates readability, with preference for dyslexia-friendly fonts
3. Clear distinction between headings, subtitles, paragraphs, and other content

### Headings — Franklin Gothic Medium

Franklin Gothic Medium scales well between the 6 heading levels, maintaining clear distinction between an H6 and body text. It also stands out from more common typefaces.

| Level | Size (px) | Size (pt) |
|-------|-----------|-----------|
| H1 | 48px | 36pt |
| H2 | 40px | 30pt |
| H3 | 32px | 24pt |
| H4 | 28px | 21pt |
| H5 | 24px | 18pt |
| H6 | 20px | 15pt |

### Body Text — Helvetica

Helvetica provides tighter letter spacing and more elegant text wrapping than Franklin Gothic Medium. Research shows it is a preferred choice by people with dyslexia (Rello & Baeza-Yates, 2013, DOI: 10.1145/2513383.2513447).

**Default body**: Helvetica, 16px / 12pt, normal weight
**Slides body**: Helvetica, 18pt (increased for projection readability)
**Bold**: for key points
**Italic**: for quotes, foreign words, or specific intonation

**Fallback stack**: Helvetica, Verdana, Arial, sans-serif

### Logo Typography

**"AI-HED" text**: Franklin Gothic, thin/light weight, large size
**Tagline**: Helvetica Light — "Artificial Intelligence in Higher Education Teaching and Learning"

## Icon

### Concept
The icon represents the human brain and the connection of neurons during learning. Keywords that informed the design: Innovation, Difference, Speed, Automatic, Machine, Person, Robots, Thinking, Teach, Learn.

### Usage Rules
- Never use the icon in isolation without the project name
- The icon can appear with the full logo or the short-hand version
- Maintain aspect ratio at all times
- Minimum clear space around the icon: equal to the icon width × 0.25

## Logo Variants

### By Content
1. **Full logo**: Icon + "AI-HED" + tagline
2. **Short-hand logo**: Icon + "AI-HED" (no tagline)

### By Colour Treatment
1. **Solid green**: icon and text in `#628c68` on white/light background
2. **Gradient green**: icon in green gradient, text in black, on white/light background
3. **Inverted (white)**: icon and text in white on dark/green background
4. **Inverted short-hand**: short-hand version in white on dark/green background

### Selection Guide
- Default/primary: gradient green full logo on white background
- Presentations title slide: inverted (white) on green/dark background
- Small spaces or favicons: icon only (with project name nearby)
- Formal documents: solid green full logo

## Colour Combinations

### Recommended
- White background + green headings + black body text ✓
- Green background + white text ✓
- Gradient green accents on white background ✓
- Dark green (`#2c4d36`) background + white text for impact slides ✓

### Avoid
- Green text on green background (insufficient contrast)
- Very light green text on white (readability issues)
- Gradient applied to body text (reserve for icon/decorative elements)
- Overuse of the gradient — keep it for the icon and key decorative moments

## Asset Files

### SVG Logos (in `assets/`)
- `ai-hed-logo-full-green-gradient.svg` — full logo with icon, "AI-HED", and tagline in gradient
- `ai-hed-logo-icon-green-gradient.svg` — icon only in gradient

## EU Co-funding Acknowledgement

All public-facing materials must include the Erasmus+ co-funding acknowledgement. Use the standard disclaimer: "Co-funded by the European Union under the Erasmus+ Programme."

The Erasmus+ logo must appear alongside the AI-HED logo on official deliverables as required by the programme's visibility guidelines.
