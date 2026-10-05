# taliferro.tech

Static site for Taliferro Tech, LLC, hosted on Firebase Hosting (`taliferro-tech` site).

- `src/build.py` holds the products, header, footer and universal menu, and writes the pages into `public/`. Edit it, then run `python3 src/build.py`.
- `src/product_pages.py` holds the copy for each `/products/<slug>` page (features, steps, FAQ). Keep it factual and free of prices.
- `public/css/site.css` and `public/js/site.js` are hand-written; edit them directly.
- Deploy: `firebase deploy --only hosting:taliferro-tech`

Preview locally with `firebase emulators:start --only hosting` (it serves on 5002 when macOS AirPlay holds 5000).
