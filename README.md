# taliferro.tech

Static site for Taliferro Tech, LLC, hosted on Firebase Hosting (`taliferro-tech` site).

- `src/build.py` holds the products, header, footer and universal menu, and writes the pages into `public/`. Edit it, then run `python3 src/build.py`.
- `src/product_pages.py` holds the copy for each `/products/<slug>` page (features, steps, FAQ). Keep it factual and free of prices.
- `src/legal_pages.py` builds `/terms`, `/privacy` and `/privacy-rights`, the legal pages for every Taliferro product (moved from todd.taliferro.tech, which 301s its old paths here). The wording is in `src/legal_terms.html` and `src/legal_privacy.html`: legal text, restyle only.
- `public/css/site.css` and `public/js/site.js` are hand-written; edit them directly.
- Deploy: `firebase deploy --only hosting:taliferro-tech`

Preview locally with `firebase emulators:start --only hosting` (it serves on 5002 when macOS AirPlay holds 5000).

## 16ahead.com

The same folder also builds 16ahead.com (Firebase site `16ahead`, output `public-16ahead/`).

- `src/sixteen_ahead.py` writes the landing page (Claude Design's `design_handoff_16ahead_landing`), `/terms`, `/privacy`, `/privacy-rights` and the 404. Run `python3 src/sixteen_ahead.py`.
- The header uses the universal menu from `taliferro-ui`. The build copies its static script, styles and icons into `public-16ahead/tt/`, so rebuild after the menu changes.
- `public-16ahead/css/16ahead.css` and `js/16ahead.js` are hand-written.
- Deploy: `firebase deploy --only hosting:16ahead`. taliferro.tech's own deploy is unchanged.

## 16ahead.io

The technical page, "how it works" (Firebase site `16ahead-io`, output `public-16ahead-io/`).

- `src/sixteen_ahead_io.py` writes the page from Claude Design's `design_handoff_16ahead_io`, plus a 404. Run `python3 src/sixteen_ahead_io.py`. It imports shared values from `sixteen_ahead.py`.
- `public-16ahead-io/css/16ahead-io.css` and `js/16ahead-io.js` are hand-written. The script starts the looping video unless the visitor prefers reduced motion; in that case it shows the player controls instead.
- The video is the design's MP4, unchanged (`media/16ahead-io.mp4`, no audio). The poster is a frame at 16s.
- The product icons are the light SVGs from `taliferro-ui/brand/products/svg/light`.
- Deploy: `firebase deploy --only hosting:16ahead-io`.
