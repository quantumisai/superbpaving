# Design Review — Superb Paving & Masonry site

**Date:** 2026-05-19
**Scope:** All 5 pages (index, services, portfolio, about, contact)
**Local URL:** http://localhost:8765/

---

## Headline scores

| Score             | Before | After |
|-------------------|--------|-------|
| **Design Score**  | C+     | A−    |
| **AI Slop Score** | A      | A     |

AI slop was already low (real photos, real type, no purple gradients, no icons-in-circles, no centered-everything). The Design Score jumped two grades because the bugs we fixed weren't taste calls — they were broken content.

---

## First Impression (initial render, desktop)

The site communicates **competence and craft**. Photography does the heavy lifting. The serif italic accents feel deliberate, not decorative. The 3 things my eye goes to are: the dark mansion driveway, the italic "built to last," and the green-dot phone CTA. That's the right hierarchy for a paving company.

One word: **earned**.

---

## Findings (high impact first)

### F-001 — CRITICAL — Reveal animation hid half the page

**Status:** Fixed
**Severity:** High
**Files:** styles.css

`.reveal{opacity:0}` was the default. The IntersectionObserver only added `.in` to elements in the initial viewport. Everything below the fold — services grid, portfolio grid, area list, craft section — stayed at opacity 0 forever. 24/24 reveal elements were invisible to anything that didn't scroll: SEO crawlers, screenshot tools, screen readers, slow JS networks.

**Fix:** Removed the hidden default. Content always visible. `prefers-reduced-motion` still respected. Animation removed entirely — not worth the trade for a static deliverable.

### F-002 — HIGH — Nav phone CTA invisible on mobile

**Status:** Fixed
**Severity:** High
**Files:** styles.css

`@media (max-width:880px){.nav-cta span:not(.dot){display:none}}` collapsed the phone number to just a green dot. Mobile users had no idea what to tap. For a paving company where calling is THE primary conversion, this was a self-inflicted wound.

**Fix:** Phone number now visible on all viewports. Nav CTA bumped to 44px min height.

### F-003 — HIGH — Hero CTAs hidden behind ticker on mobile

**Status:** Fixed
**Severity:** High
**Files:** styles.css

The bottom ticker bar wrapped to 4 lines on 390px viewports, overlapping the primary hero CTAs ("Get a free estimate" and "See our work"). Users could see the hero text but the action buttons were obscured.

**Fix:** Ticker hidden on mobile (≤680px). Hero CTAs now full-width centered buttons. Values band immediately below covers the same trust signals.

### F-004 — MEDIUM — Touch targets below 44px

**Status:** Fixed
**Severity:** Medium
**Files:** styles.css

Mobile audit found 7 interactive elements under 44×44px (WCAG / Apple HIG threshold):
- Nav phone CTA: 34×28
- Nav toggle: 37×38
- Footer links: 350×28

**Fix:** Nav targets bumped to 44px min-height. Footer links now use padding + flex centering to achieve 44px min tap area.

### F-005 — MEDIUM — Hero h1 too dominant on mobile

**Status:** Fixed
**Severity:** Medium
**Files:** styles.css

`font-size:clamp(48px,7vw,104px)` rendered the hero h1 at ~52px on a 390px viewport, pushing the body copy and CTAs below the fold even before the ticker overlay.

**Fix:** Min size dropped to 38px in the clamp, with an explicit 42px override at ≤680px.

---

## What's strong (no changes needed)

- **Typography system.** Fraunces serif italic accents are doing real work, not decoration. Two-family system (Fraunces + Inter), no system-ui fallback as primary. Real type discipline.
- **Color palette.** Bone + ink + bronze + paper. Coherent, warm, restrained. No purple gradients. No "I gave up" greys.
- **Real photography throughout.** Their actual work, not stock. Bigger trust signal than anything else on the page.
- **One job per section.** Each band has a clear purpose. No card-mosaic dashboards. No "we do everything" feature grids.
- **AI Slop blacklist** — clean across all 10 anti-patterns. Most notably: no 3-column icon-in-circle feature grids, no centered-everything, no decorative blobs/dividers, no bubbly uniform radius.

---

## Console errors

Zero across all 5 pages.

---

## Quick wins worth considering later (not in this pass)

1. Add `<link rel="preload">` for the hero image on index.html for LCP improvement
2. Add `loading="lazy"` to portfolio gallery images below the fold
3. Add a `favicon.ico` fallback for browsers that ignore SVG icons (`favicon.svg` and `apple-touch-icon.png` are both linked on every page)
4. Add an `og:image` with text overlay for social sharing
5. The portfolio "References available on request" callout could link to a `mailto:` directly

---

## Verdict

Ship it.

Five pages, all green on console, all responsive down to 390px, real photography, real copy, and a design system tight enough that the client can extend it themselves without a rebuild. The hero "Paving and masonry, built to last." is doing the job a high-end paving site needs to do: signal craft before content.

**Correction (added later):** the 390px pass missed horizontal overflow on `index.html` and `about.html`, and ticker wrapping between 680px and ~1100px. Both are measured and recorded in `TODOS.md`.
