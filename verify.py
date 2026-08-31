#!/usr/bin/env python3
"""Static-site invariant check. No dependencies, no framework: python3 verify.py

Guards the things that silently rot on a contractor marketing site — NAP
consistency across pages (a real local-SEO ranking factor), JSON-LD validity,
service-area agreement between the schema and the visible copy, geo metadata,
and SERP length limits. Run it after any content edit.
"""
import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = ["index", "about", "services", "portfolio", "contact"]

# --- Canonical business facts. Change here when the business changes. ---
NAME = "Superb Paving & Masonry"
URL = "https://www.superbpavingmasonry.com/"
PHONE_DISPLAY = "(773) 842-1700"
PHONE_TEL = "7738421700"
PHONE_SCHEMA = "+1-773-842-1700"
EMAIL = "superbpavingillinois@gmail.com"
STREET = "180 North Stetson Avenue, Suite 202"
CITY, REGION, POSTAL = "Chicago", "IL", "60601"
LAT, LON = 41.8858, -87.6216
SERVICE_AREA = ["Chicago", "Evanston", "Oak Park", "Skokie", "Des Plaines",
                "Arlington Heights", "Schaumburg", "Oak Lawn", "Elmhurst",
                "Naperville", "Highland Park", "Joliet"]

# Terms from the location the business left in August 2026, plus the tautology
# the Chicago rewrite introduced. Any hit means a stale edit crept back in.
# Matched case-insensitively. "Arlington" is deliberately absent: it collides
# with the current "Arlington Heights".
STALE = ["Stafford", "Virginia", "Northern VA", "Fredericksburg", "Quantico",
         "Woodbridge", "Manassas", "Fairfax", "Springfield", "Burke",
         "Alexandria", "Dumfries", "Dale City", "Loudoun", "Prince William",
         "US-VA", "22554", "Corporate Dr", "499-2258", "7034992258",
         "superbpavingandmasonry", "Chicago and Chicagoland",
         "Chicago & Chicagoland", "Chicago or Chicagoland",
         "Chicago · Chicagoland"]

TITLE_MAX, DESC_MAX, DESC_MIN = 62, 158, 70
fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
        return fh.read()


def meta(html, name):
    m = re.search(r'<meta\s+name="%s"\s+content="(.*?)"' % re.escape(name), html, re.S)
    return m.group(1) if m else None


def title_of(html):
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    return m.group(1) if m else None


VOID = {"br", "img", "link", "meta", "input", "hr", "source", "area",
        "base", "col", "embed", "param", "track", "wbr"}


class SpanGroups(HTMLParser):
    """Collect the direct <span> text of every element, so a service-area
    container can be compared as a whole. Extra entries then show up as a
    mismatch instead of being filtered away."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.groups, self.depth, self.buf = [], [], 0, []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        if self.depth:
            self.depth += 1                 # nested <small>HQ</small> etc.
        elif tag == "span":
            self.depth, self.buf = 1, []
        else:
            self.stack.append([tag, []])

    def handle_startendtag(self, tag, attrs):
        return                              # self-closing: no children

    def handle_data(self, data):
        if self.depth == 1:                 # direct text of the span only
            self.buf.append(data)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.depth:
            self.depth -= 1
            if self.depth == 0 and self.stack:
                self.stack[-1][1].append("".join(self.buf).strip())
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                for frame in self.stack[i:]:
                    if frame[1]:
                        self.groups.append(frame[1])
                del self.stack[i:]
                return


def visible_area_list(html):
    """The span group that looks like the service-area block, or None."""
    parser = SpanGroups()
    parser.feed(html)
    for group in parser.groups:
        if group and group[0] == SERVICE_AREA[0] and len(group) >= len(SERVICE_AREA):
            return group
    return None


html = {p: read(p + ".html") for p in PAGES}

# Scan every text-bearing tracked file, not just the served pages: a stale
# instruction in docs/ sends the owner to claim the wrong business listing.
corpus = {p + ".html": html[p] for p in PAGES}
for pattern in ("*.txt", "*.md", "*.xml", "*.css", "docs/*.md"):
    for path in sorted(glob.glob(os.path.join(ROOT, pattern))):
        corpus[os.path.relpath(path, ROOT)] = read(os.path.relpath(path, ROOT))

# History files must be able to name the previous location — that is the record
# of the move, not stale targeting. Everything else is still scanned.
HISTORY = {"CHANGELOG.md", "TODOS.md"}

# 1. No stale geography anywhere, in any casing.
for name, body in corpus.items():
    if name in HISTORY:
        continue
    low = body.lower()
    for term in STALE:
        check(term.lower() not in low, "stale term %r in %s" % (term, name))

# 2. JSON-LD parses, and the business block is identical on every page.
blocks = {}
for p, body in html.items():
    raw = re.findall(r'<script type="application/ld\+json">(.*?)</script>', body, re.S)
    check(raw, "%s.html: no JSON-LD" % p)
    nodes = []
    for chunk in raw:
        try:
            doc = json.loads(chunk)
        except json.JSONDecodeError as exc:
            fails.append("%s.html: invalid JSON-LD (%s)" % (p, exc))
            continue
        for node in (doc if isinstance(doc, list) else [doc]):
            if isinstance(node, dict):
                nodes.extend(node.get("@graph", [node]))
    biz = [n for n in nodes if isinstance(n, dict) and n.get("@type") == "GeneralContractor"]
    check(len(biz) == 1, "%s.html: expected exactly 1 GeneralContractor block" % p)
    if len(biz) == 1:
        blocks[p] = biz[0]

if len(blocks) == len(PAGES):
    ref = json.dumps(blocks["index"], sort_keys=True)
    for p in PAGES[1:]:
        check(json.dumps(blocks[p], sort_keys=True) == ref,
              "%s.html: JSON-LD business block differs from index.html (NAP drift)" % p)

# 3. NAP, geo, and service area are correct in the schema.
for p, biz in blocks.items():
    addr = biz.get("address", {})
    check(biz.get("name") == NAME, "%s.html: schema name" % p)
    check(biz.get("url") == URL, "%s.html: schema url" % p)
    check(biz.get("telephone") == PHONE_SCHEMA, "%s.html: schema telephone" % p)
    check(biz.get("email") == EMAIL, "%s.html: schema email" % p)
    check(addr.get("streetAddress") == STREET, "%s.html: schema streetAddress" % p)
    check(addr.get("addressLocality") == CITY, "%s.html: schema addressLocality" % p)
    check(addr.get("addressRegion") == REGION, "%s.html: schema addressRegion" % p)
    check(addr.get("postalCode") == POSTAL, "%s.html: schema postalCode" % p)
    check(biz.get("geo", {}).get("latitude") == LAT, "%s.html: schema latitude" % p)
    check(biz.get("geo", {}).get("longitude") == LON, "%s.html: schema longitude" % p)
    area = biz.get("areaServed", [])
    check([c.get("name") for c in area] == SERVICE_AREA,
          "%s.html: areaServed does not match the canonical 12 cities in order" % p)
    check(all(c.get("containedInPlace", {}).get("name") == "Illinois" for c in area),
          "%s.html: areaServed contains a non-Illinois state" % p)

# 4. The ONLY phone and email on any page are the current ones. Asserting the
#    new value is present is not enough: a half-finished edit leaves both.
for p, body in html.items():
    check(set(re.findall(r'href="tel:([^"]+)"', body)) == {PHONE_TEL},
          "%s.html: unexpected tel: target (%s)" % (p, set(re.findall(r'href="tel:([^"]+)"', body))))
    check(set(re.findall(r'href="mailto:([^"]+)"', body)) == {EMAIL},
          "%s.html: unexpected mailto: target" % p)
    check(PHONE_DISPLAY in body, "%s.html: missing display phone" % p)

# 5. Geo meta tags duplicate the schema coordinates — assert they agree.
for p, body in html.items():
    check(meta(body, "geo.region") == "US-" + REGION, "%s.html: geo.region" % p)
    check(meta(body, "geo.placename") == CITY, "%s.html: geo.placename" % p)
    for tag, sep in (("geo.position", ";"), ("ICBM", ", ")):
        val = meta(body, tag)
        check(val == "%s%s%s" % (LAT, sep, LON), "%s.html: %s is %r" % (p, tag, val))

# 6. Visible service-area lists agree with the schema, in the same order.
for p in ("index", "about", "contact"):
    check(visible_area_list(html[p]) == SERVICE_AREA,
          "%s.html: visible service-area list does not match the schema (got %s)"
          % (p, visible_area_list(html[p])))

# 7. llms.txt is quoted verbatim by AI search; README is the human entry point.
#    Both carry hand-maintained copies of the NAP, so assert them positively.
check("- Service area: " + ", ".join(SERVICE_AREA) in corpus["llms.txt"],
      "llms.txt: service-area line does not match the canonical 12 cities")
for name in ("llms.txt", "README.md"):
    for fact in (PHONE_DISPLAY, EMAIL, STREET, "%s, %s %s" % (CITY, REGION, POSTAL)):
        check(fact in corpus[name], "%s: missing %r" % (name, fact))

# 8. SERP length limits, and the twitter tags mirror the real title/description.
titles = []
for p, body in html.items():
    title, desc = title_of(body), meta(body, "description")
    check(title is not None, "%s.html: no <title>" % p)
    check(desc is not None, "%s.html: no meta description" % p)
    titles.append(title)
    if title is not None:
        check(len(title) <= TITLE_MAX, "%s.html: title is %d chars (max %d)" % (p, len(title), TITLE_MAX))
        check(meta(body, "twitter:title") == title, "%s.html: twitter:title does not mirror <title>" % p)
    if desc is not None:
        check(DESC_MIN <= len(desc) <= DESC_MAX,
              "%s.html: meta description is %d chars (want %d-%d)" % (p, len(desc), DESC_MIN, DESC_MAX))
        check(meta(body, "twitter:description") == desc,
              "%s.html: twitter:description does not mirror the meta description" % p)
check(len(set(titles)) == len(titles), "duplicate <title> across pages")

# 9. sitemap.xml parses and every <loc> points at a page that exists.
try:
    root = ET.fromstring(corpus["sitemap.xml"])
    locs = [e.text.strip() for e in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
    check(locs, "sitemap.xml: no <loc> entries")
    for loc in locs:
        rel = loc[len(URL):] or "index.html"
        check(os.path.exists(os.path.join(ROOT, rel)), "sitemap.xml: <loc> has no file (%s)" % loc)
except ET.ParseError as exc:
    fails.append("sitemap.xml: invalid XML (%s)" % exc)

# 10. Every local asset exists, matching case exactly — macOS is case-insensitive
#     but static hosts are not, so os.path.exists alone would pass a 404.
for p, body in html.items():
    for ref in re.findall(r'(?:src|href)="((?!https?:|mailto:|tel:|#|//)[^"]+)"', body):
        rel = ref.split("?")[0].split("#")[0].lstrip("/")
        folder = os.path.join(ROOT, os.path.dirname(rel))
        check(os.path.isdir(folder) and os.path.basename(rel) in os.listdir(folder),
              "%s.html: missing local asset %s" % (p, ref))

if fails:
    print("FAIL (%d)" % len(fails))
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("OK: %d pages, no failures" % len(PAGES))
