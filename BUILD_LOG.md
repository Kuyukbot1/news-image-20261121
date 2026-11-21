# Build log — news-image-20261121

- 2026-11-21 ~02:15–02:30 UTC: researched 21 Nov news (Reuters, AP, AFP,
  BBC, Al Jazeera, Le Monde, NDTV, ANI, PIB and others); recorded 42
  verified stories in `../RESEARCH_21NOV.md`.
- 2026-11-21 ~02:30 UTC: wrote `draw.py` fresh (layout + helpers + flat
  illustrations + simplified world map), then added the story data and
  feature cards in a second step.
- 2026-11-21 ~02:40 UTC: first render failed — two illustration kinds used
  fixed coordinates that broke in the 40px small-card bands. Rewrote all
  illustrations to height-proportional coordinates; fixed an inverted
  chart-axis rectangle.
- 2026-11-21 ~02:45 UTC: first successful render (155,352 bytes). Visual
  check found deck/headline text clipped to two lines in the small cards
  (3rd line dropped). Shortened all small-card headlines and decks to fit
  two lines; offset the Washington/New York map pins with leader lines;
  tightened the vertical budget so the footer clears the bottom edge.
- 2026-11-21 ~02:50 UTC: second render (155,819 bytes) — visual check
  passed: masthead date readable, all 13 headlines and decks complete,
  map pins match card numbers, also-on list complete (14–42), footer fits.
- 2026-11-21 ~02:53 UTC: wrote `main.ts` fresh (stdlib-only copy to
  `$MAKEFUN_OUTPUT_DIR`); ran it twice into two temp dirs and compared
  sha256 — byte-identical.

Final: entry.png 1024x1024, 155,819 bytes.
