# TODOS

Items found during the Chicago relocation ship (v0.0.1.0) that were deliberately
left out of that change. Each one is real and reproducible; none of them block
the relocation.

## Performance

### Cut the image payload on the home page

**What:** index.html eager-loads roughly 1.42 MB of JPEGs across 14 `<img>` tags plus the hero background, for 1.47 MB total page weight.

**Why:** On a mobile connection this is the difference between a fast first impression and a visitor leaving. Only the hero and the first service card are above the fold; the other ~11 images compete for bandwidth with the image that determines the Largest Contentful Paint score Google measures.

**Context:** Measured file sizes: `img/home.jpg` 248 KB (1028x1200), `serv_0006` 217 KB, `serv_0009` 204 KB, `serv_0004` 196 KB, `serv_0007` 196 KB, `serv_0002` 166 KB, `serv_0008` 164 KB. `grep -rn 'loading=' *.html` returns exactly one hit, and it is the map iframe — no `<img>` on any page carries `loading`, `decoding`, `width`, or `height`. Two independent fixes: add `loading="lazy" decoding="async"` to every below-the-fold image (leave the hero eager), and re-encode the JPEGs as WebP, which typically lands 60-75% smaller and needs no build step via `<picture>`. Note that missing width/height is *not* causing layout shift here — every image container already reserves its box with `aspect-ratio` in styles.css.

**Effort:** M
**Priority:** P1
**Depends on:** None

### Make the hero image visible to the preload scanner

**What:** The 248 KB hero image is declared as a CSS background inside an inline `style` attribute, so the browser's preload scanner never sees it.

**Why:** It is the Largest Contentful Paint element. Its download cannot start until the render-blocking Google Fonts stylesheet and styles.css have both arrived and styles are computed, which serialises the biggest asset on the page behind two round trips.

**Context:** `index.html:119` is `<div class="hero-img" style="background-image:url('img/home.jpg')"></div>`, styled by `.hero-img` at styles.css:160. There is no `rel=preload` anywhere in the file. Either add `<link rel="preload" as="image" href="img/home.jpg" fetchpriority="high">` to `<head>`, or convert `.hero-img` to a real absolutely-positioned `<img>` with `fetchpriority="high"`.

**Effort:** S
**Priority:** P1
**Depends on:** None

### Shrink apple-touch-icon.png

**What:** The icon added in v0.0.1.0 is 11,049 bytes of 8-bit RGBA for a flat two-colour design.

**Why:** Low urgency and honest about it — the icon is fetched on add-to-home-screen, not during page load, so this costs no LCP and no page weight. It is oversized, not harmful.

**Context:** The image contains only 571 distinct RGBA values, all antialiasing gradations, plus 517 bytes of generator metadata (eXIf, iTXt, gAMA, cHRM). Re-emitting as an 8-bit palette PNG with PLTE+tRNS was measured at 4,535 bytes, a 59% reduction with no visible change. It was generated from `favicon.svg` via `qlmanage` + `sips`.

**Effort:** S
**Priority:** P4
**Depends on:** None

## Responsive

### Fix horizontal overflow on mobile

**What:** index.html and about.html scroll sideways on phones.

**Why:** A page that slides horizontally under your thumb reads as broken, and this is the viewport most local-search traffic arrives on.

**Context:** Pre-existing, not introduced by the relocation — verified byte-for-byte against the previous commit. It did improve as a side effect of the shorter Chicago strings: index.html measured scrollWidth 456px at a 390px viewport before, 416px after. Still overflowing by 66px. The culprits are the hero service-tag row on index and the "For businesses / Commercial" reveal block on about; both need `flex-wrap`, `min-width:0`, or a mobile breakpoint.

**Effort:** S
**Priority:** P2
**Depends on:** None

### Stop the hero ticker wrapping to four lines

**What:** The trust strip under the hero collapses from one line to four between 680px and roughly 1100px, growing upward over the hero.

**Why:** It is above the fold on tablets and small laptops, so the first impression is a block of stacked text over the hero image.

**Context:** Pre-existing and slightly improved by this release — the new `Cook · DuPage · Lake · Will Counties` string measures 331px against 411px for the string it replaced, so it wraps later, but the underlying behaviour is unchanged. Measured ticker-inner height: 19px at 1280px, 69px at 1100px. Either hide the third span below 1150px or give the ticker `overflow-x:auto` with `nowrap` in that band.

**Effort:** S
**Priority:** P3
**Depends on:** None

## Content

### Decide the portfolio project captions

**What:** Eleven of the twelve portfolio tiles use a `Segment · Project type` caption (`Residential · Driveway`), while one uses `Residential · Chicago, IL`.

**Why:** The filter bar on that page is built from project types, so the odd caption breaks the taxonomy. Separately, the page currently offers almost no local proof, which is what a homeowner is actually scanning for.

**Context:** The odd caption is a direct swap of the original `Residential · Stafford, VA`, so the inconsistency predates this release. Two open questions only the owner can answer: should that tile read `Residential · Driveway` to match the others, and are there real suburb names that can be attached to the other tiles? Do not invent project locations — a fabricated job location is worse than none.

**Effort:** S
**Priority:** P2
**Depends on:** Owner input

### Localise the durability claims on the services page

**What:** None of the eight service blocks on services.html makes a Chicago-specific claim.

**Why:** The copy currently reads identically to a contractor in Phoenix — driveways "stand up to daily use, season after season", asphalt "doesn't sink, crack, or pool". A Chicago contractor's actual differentiator is the thing that is missing.

**Context:** The genuine local hooks are the 42-inch frost depth and building the base below it, freeze-thaw heave, salt scaling on concrete, and sealcoating before the first freeze. These are claims about how the crew actually builds, so they need the owner's confirmation before going on the site — do not assert them unilaterally. Note also that "Belgian block borders" in the driveways list is mid-Atlantic trade register; a Chicago crew would more likely write "granite setts" or "stone borders", but it may be a real product line, so confirm before changing.

**Effort:** M
**Priority:** P2
**Depends on:** Owner input

### Confirm the office address is the right one to publish

**What:** 180 N Stetson Ave, Suite 202 is Two Prudential Plaza, a Class-A office tower in the Loop.

**Why:** A paving and masonry contractor headquartered in a downtown office tower with no yard reads as a virtual office to a local customer, and Google Business Profile verification and citation building both work better from a real service address.

**Context:** Flagging rather than changing, because this is owner-supplied business data. It also sits awkwardly beside the adjacent line on the contact page, "Office visits by appointment only — we're usually on a job site." If the Loop suite stays, it should not be presented as a walk-in office.

**Effort:** S
**Priority:** P2
**Depends on:** Owner input

## Design

### Level the contact card CTA rows

**What:** The three contact cards have their CTA rows at 268 / 230 / 290px from the card top — a 60px stagger.

**Why:** The three cards are the primary conversion element on the contact page, and their calls to action no longer sit on a shared baseline.

**Context:** Measured at 1440x900; all three cards are 360px tall. The stagger widened when the email card dropped from three lines to two after the address shortened. Fix is `display:flex; flex-direction:column` on the cards with `margin-top:auto` on the CTA row.

**Effort:** S
**Priority:** P3
**Depends on:** None

### Reconsider the italic accent on the about page heading

**What:** `about.html` reads `Chicago <em>& the suburbs.</em>`, so the largest italic glyph on the line is an ampersand.

**Why:** Every other accent on the site emphasises the distinctive proper noun — `Serving <em>Chicagoland.</em>`, `Based in <em>Chicago, Illinois.</em>`.

**Context:** Taste call, deliberately left alone during the relocation. Options are moving the accent onto the place name or matching the home page with `<em>Chicagoland.</em>`.

**Effort:** S
**Priority:** P4
**Depends on:** None

## SEO

### Add Open Graph title and description tags

**What:** No page has `og:title` or `og:description`. Only `og:site_name`, `og:locale`, `og:url`, and `og:image` are present.

**Why:** Facebook, LinkedIn, Slack, and iMessage all read `og:*`. Shared links currently render with an image and no description text, wasting the tuned copy that already exists in the `twitter:` tags.

**Context:** Pre-existing. Each page already has a correct `<title>` and meta description that `verify.py` keeps within SERP limits and mirrored into `twitter:title` / `twitter:description` — the same strings just need mirroring into `og:` tags too. Worth extending `verify.py` to assert it once the tags exist.

**Effort:** S
**Priority:** P2
**Depends on:** None

## Completed

### Relocate the site from Stafford, VA to Chicago, IL

**What:** Full NAP, service area, metadata, structured data, and copy relocation across all five pages plus llms.txt, README.md, sitemap.xml, and docs/SEO-REPORT.md.

**Completed:** v0.0.1.0 (2026-08-31)
