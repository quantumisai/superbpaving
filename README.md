# Superb Paving & Masonry

Website for **Superb Paving & Masonry** — paving and masonry contractor serving Stafford, VA and Northern Virginia.

**Live phone:** (703) 499-2258
**Office:** 800 Corporate Drive, Suite 301, Stafford, VA 22554
**Email:** superbpavingandmasonry@gmail.com

## What's in this repo

Static HTML website. No build step. Deployable as-is from the repo root.

```
.
├── index.html         Home
├── services.html      Services catalog (driveways, patios, walkways, masonry, walls, concrete, asphalt)
├── portfolio.html     Project gallery with category filter
├── about.html         Company values, approach, who we serve
├── contact.html       Phone, email, office, service area, map
├── styles.css         Shared stylesheet
├── favicon.svg        Brand favicon
├── sitemap.xml        Search engine sitemap (with image sitemap)
├── robots.txt         Crawler config
├── llms.txt           AI search optimization (ChatGPT, Perplexity, AI Overviews)
├── img/               Photography
└── docs/
    ├── DESIGN-REPORT.md   Design review findings + fixes
    └── SEO-REPORT.md      SEO audit + remaining client-side work
```

## Deploy

The repo root is the publish directory. Any static host works.

### Netlify (recommended)
1. Sign in at https://app.netlify.com
2. "Add new site" → "Import an existing project" → connect this GitHub repo
3. Build command: *(leave blank)*
4. Publish directory: `/` *(root)*
5. Deploy — done in ~30 seconds. Netlify gives you a free HTTPS subdomain. Point the real domain via Domain Settings.

### Cloudflare Pages
1. https://dash.cloudflare.com → Pages → Create a project → Connect to Git
2. Build settings: framework preset = *None*, build command = *blank*, output directory = `/`
3. Deploy.

### Vercel
1. https://vercel.com → New Project → Import this repo
2. Framework Preset: Other. Root Directory: `./`. Build/Output blank.
3. Deploy.

### FTP / SFTP / shared host
Upload the contents of the repo root to your web root (e.g. `public_html/`). Done.

## Local preview

```bash
python3 -m http.server 8765
# → http://localhost:8765/
```

## Editing content

Everything is plain HTML and CSS. Open the file, change the text or the photo path, save, refresh. No CMS, no database, no build tool.

To swap a photo, replace the file in `img/` (keep the same filename) or update the `<img src="...">` reference in the HTML.

## Design system

CSS custom properties at the top of `styles.css` drive the entire palette and type system. Change one variable, the whole site shifts.

- **Type:** Fraunces (serif, with italic display cuts) + Inter (UI/body)
- **Palette:** ink `#0E0F0C`, bone `#F2EDE4`, paper `#EAE3D5`, bronze `#9A7849`, highlight `#E8C99B`
- **Grid:** 12-column, 1360px max width, breakpoints at 880px (tablet) and 680px (mobile)

## Next steps after going live

Two things only the business owner can do (see `docs/SEO-REPORT.md` for full detail):

1. **Claim Google Business Profile** at https://business.google.com — this is what gets you in the local map pack.
2. **Build citations** (Yelp, Angi, BBB, Houzz, Nextdoor, Apple Maps) with NAP that matches the site exactly.
3. **Collect reviews** — every completed job should get a GBP review request.

---

© 2026 Superb Paving & Masonry. Stafford, Virginia.
