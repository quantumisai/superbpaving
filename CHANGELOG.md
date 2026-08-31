# Changelog

All notable changes to the Superb Paving & Masonry site are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.0.1.0] - 2026-08-31

The business moved from Stafford, Virginia to Chicago, Illinois. Every place a
customer or a search engine could find the old location has been updated.

### Changed

- New phone number `(773) 842-1700`, email `superbpavingillinois@gmail.com`, and
  office at 180 North Stetson Avenue, Suite 202, Chicago, IL 60601 — updated in
  the header, footer, contact cards, and click-to-call links on every page.
- Service area is now Chicagoland: Chicago (HQ), Evanston, Oak Park, Skokie,
  Des Plaines, Arlington Heights, Schaumburg, Oak Lawn, Elmhurst, Naperville,
  Highland Park, and Joliet — spanning Cook, DuPage, Lake, and Will counties.
- Page titles and search descriptions now target Chicago instead of Stafford, so
  the site can rank for local searches in the market it actually serves.
- Structured business data (JSON-LD), geo meta tags, and the map embed all point
  at the Chicago office, which is what Google Business Profile and Apple Maps read.
- Durability claims now describe the weather that actually damages pavement here —
  freeze-thaw cycles, road salt, and summer heat — instead of mid-Atlantic seasons.
- `llms.txt` updated so AI search tools (ChatGPT, Perplexity, AI Overviews)
  recommend the business for the right city.
- `docs/SEO-REPORT.md` no longer instructs the owner to claim a Google Business
  Profile for the old location or build pages for the old service area.

### Added

- `verify.py` — a dependency-free check that fails if the phone, email, address,
  service area, or structured data drift apart between pages, if a title or
  description breaks its search-result length limit, or if an image or stylesheet
  reference points at a file that isn't there. Run `python3 verify.py` after any
  content edit.
- `apple-touch-icon.png` — the iOS home-screen icon every page had been linking
  to without it existing, so the link 404'd on all five pages.

### Fixed

- The contact page email and the footer email were rendering as one unbroken
  30-character string, which split mid-word on the contact card and stretched the
  footer's Contact column wide enough to squash the office address.
- The "HQ" badge on the contact page service-area list now matches the size,
  colour, and spacing of the same badge on the home and about pages.
