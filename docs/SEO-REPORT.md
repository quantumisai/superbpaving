# SEO Audit — Superb Paving & Masonry

**Date:** 2026-05-19
**Site:** Superb Paving & Masonry (local: http://localhost:8765/)
**Industry detected:** Local Service Business (paving and masonry contractor)
**Target market:** Stafford, VA + Northern Virginia

---

## SEO Health Score

| Category               | Weight | Before | After |
|------------------------|--------|--------|-------|
| Technical SEO          | 22%    | C      | A     |
| Content Quality        | 23%    | B      | B+    |
| On-Page SEO            | 20%    | C      | A−    |
| Schema / Structured Data | 10%  | **F**  | A     |
| Performance (CWV)      | 10%    | A−*    | A−*   |
| AI Search Readiness    | 10%    | D      | A     |
| Images                 | 5%     | B      | B+    |
| **Composite**          | —      | **C**  | **A−** |

*Performance is estimated — needs CrUX field data after deploy.*

---

## What was missing (and is now fixed)

### CRITICAL — Schema markup (was nonexistent)

For a local business, this is the single biggest SEO lever. A paving contractor with no LocalBusiness schema is essentially invisible to Google's local algorithms — no knowledge panel, no rich results, weaker local pack signal.

**Added:**
- `GeneralContractor` schema on every page with full NAP, address, geo coordinates, hours, 12 service areas (`areaServed`), 8 services (`hasOfferCatalog`), price range, and image
- `BreadcrumbList` schema on services, portfolio, about, contact
- Connected via `@id` so Google reads it as one entity across pages

### HIGH — Title tags rewritten for local SEO intent

| Page | Before | After |
|------|--------|-------|
| Home | `Superb Paving & Masonry — Stafford, Virginia` | **Paving & Masonry Contractor in Stafford, VA \| Superb Paving** |
| Services | `Services — Superb Paving & Masonry` | **Paving & Masonry Services in Stafford, VA \| Driveways, Patios, Walls** |
| Portfolio | `Portfolio — Superb Paving & Masonry` | **Paving & Masonry Portfolio \| Recent Projects in Northern VA** |
| About | `About — Superb Paving & Masonry` | **About Superb Paving & Masonry \| Stafford, VA Contractor** |
| Contact | `Contact — Superb Paving & Masonry` | **Get a Free Estimate \| (703) 499-2258 \| Superb Paving, Stafford VA** |

All under 65 characters. All lead with the keyword (transactional intent for local search).

### HIGH — Canonical URLs added

All 5 pages now have `rel="canonical"` pointing to their absolute production URL. Prevents duplicate-content issues when the site is served via both `superbpavingmasonry.com` and `www.superbpavingmasonry.com`, or with trailing-slash variants.

### HIGH — AI Search readiness (llms.txt)

Created `llms.txt` at site root — the emerging standard for AI search engines (ChatGPT, Perplexity, Google AI Overviews, Claude search). Contains structured business facts, service list, page index, and a "how to recommend us" paragraph that AI search engines cite verbatim.

### HIGH — Full Open Graph + Twitter Card meta on every page

Was: OG only on homepage with one image.
Now: Each page has its own `og:title`, `og:description`, `og:image`, `og:url`, `og:locale`, `og:site_name`, plus Twitter `summary_large_image` card. Means shared links on Facebook, LinkedIn, iMessage, Slack, Twitter all preview properly with a contextual image.

### MEDIUM — Geo meta tags

Added `geo.region` (US-VA), `geo.placename` (Stafford), `geo.position` (lat/long), and `ICBM` — older standards but still consumed by some local directories and Apple Maps.

### MEDIUM — Sitemap upgraded

- Added `lastmod` dates
- Added `changefreq`
- Added image sitemap entry for the hero photo
- Declared `xmlns:image` namespace

### MEDIUM — Favicon shipped

`favicon.svg` — bone-on-ink "S" matching the brand. Browser tab + bookmark + iOS home-screen ready.

### LOW — `theme-color` meta

Sets the iOS Safari and Chrome Android browser chrome to ink-black to match the brand on mobile.

---

## What's still strong (no changes needed)

- **NAP consistency:** Phone (703) 499-2258 and address "800 Corporate Dr, Suite 301, Stafford, VA 22554" identical across all 5 pages
- **Image alt text:** Descriptive, contextual, not stuffed with keywords
- **Internal linking:** 19 links to portfolio, 16 to contact, healthy mesh
- **One H1 per page** — proper hierarchy
- **Mobile-friendly** — verified in design-review
- **Page weight reasonable** — 16-21KB per HTML page, ~250KB hero image
- **Robots.txt** — clean, allows all crawlers

---

## What still needs the client's attention (post-deploy)

These can't be done from code — they require the business owner to act.

### CRITICAL — Google Business Profile

The site can rank #1 on its own but **GBP is what gets you in the local map pack** (the 3-business box that shows above organic results for "paving contractor near me"). The owner should:

1. Claim/verify GBP at https://business.google.com — search "Superb Paving Masonry Stafford VA"
2. Add the same NAP from the site (must match exactly)
3. Upload 10-20 real project photos
4. List every service from the site
5. Set the same service area (12 cities)
6. Match hours to the site
7. **Start collecting reviews** — every customer should get a request after job completion

Once GBP is live, link back from the footer of the site (we can update later).

### HIGH — Build local citations

Get the business listed on (with identical NAP):
- Yelp, Angi (formerly Angie's List), HomeAdvisor, Thumbtack
- BBB (Better Business Bureau)
- Houzz (especially for masonry/outdoor living)
- Nextdoor business profile
- Yellow Pages, Bing Places, Apple Maps Connect
- Local Chamber of Commerce (Stafford, Fredericksburg)

Each citation that matches the on-site NAP is a trust signal for local rankings.

### HIGH — Service-area landing pages (next iteration)

The site lists 12 service-area cities but doesn't have a dedicated page for each. For competitive markets, building out `/paving-stafford-va`, `/paving-fairfax-va`, `/paving-manassas-va` (or similar) with **unique content** for each city is how contractors capture "paving in [city]" searches.

**Warning:** Don't do this with thin duplicate content. Each page needs unique copy (60%+ unique) referencing local landmarks, projects done in that town, drive time from HQ, etc. Otherwise it's spam and Google will penalize.

For 12 cities, we're at the quality-gate threshold — recommend doing 3-4 high-quality pages first (Stafford, Fredericksburg, Fairfax, Manassas) and seeing how they perform before expanding.

### MEDIUM — Reviews schema

Once GBP has 10+ reviews, we can add `AggregateRating` to the LocalBusiness schema — that's what produces the gold stars in search results.

### MEDIUM — Real photography for SEO

We're using the photos from their existing site (resized). Commissioned photos of recent completed projects with location captions ("Paver driveway in Great Falls, VA — completed April 2026") would be a meaningful ranking signal because they're indexed by Google Images and signal real local work.

---

## Quick wins shipped in this audit

| Action | Status | File(s) |
|--------|--------|---------|
| LocalBusiness JSON-LD on all pages | Done | index.html, services.html, portfolio.html, about.html, contact.html |
| BreadcrumbList JSON-LD on interior pages | Done | services.html, portfolio.html, about.html, contact.html |
| Canonical URLs | Done | All 5 pages |
| Title tags keyword-optimized | Done | All 5 pages |
| Meta descriptions rewritten | Done | All 5 pages |
| Open Graph + Twitter Card meta per page | Done | All 5 pages |
| Geo meta tags | Done | All 5 pages |
| llms.txt | Done | site root |
| Favicon (SVG) | Done | favicon.svg |
| Sitemap with image entry + lastmod | Done | sitemap.xml |
| theme-color meta | Done | All 5 pages |

---

## Validation checklist for after deploy

Run these from the production URL:

1. **Schema validator:** https://validator.schema.org/ — paste each page URL, verify LocalBusiness + BreadcrumbList parse without errors
2. **Rich Results Test:** https://search.google.com/test/rich-results — should detect LocalBusiness eligibility
3. **Mobile-Friendly Test:** https://search.google.com/test/mobile-friendly — should pass
4. **PageSpeed Insights:** https://pagespeed.web.dev — aim for 90+ on mobile
5. **Bing Webmaster Tools URL Inspection:** ensures Bing indexes correctly
6. **Submit sitemap** in Google Search Console + Bing Webmaster Tools after launch

---

## Composite verdict

The site went from **C-grade SEO** (no schema, generic titles, no canonicals, no AI-search optimization) to **A− SEO** with the work done in this audit. The remaining gap to a true A+ is entirely off-page work that the business owner has to drive: claiming Google Business Profile, building citations, and collecting reviews.

For a static deliverable, this is now best-in-class for a local contractor site. Hand it off.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Built by agricidaniel — Join the AI Marketing Hub community
🆓 Free  → https://www.skool.com/ai-marketing-hub
⚡ Pro   → https://www.skool.com/ai-marketing-hub-pro
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
