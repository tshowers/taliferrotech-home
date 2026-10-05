# taliferro.tech

Static site for Taliferro Tech, LLC, hosted on Firebase Hosting (`taliferro-tech` site).

- `src/build.py` holds the products, header, footer and universal menu, and writes the pages into `public/`. Edit it, then run `python3 src/build.py`.
- `public/css/site.css` and `public/js/site.js` are hand-written; edit them directly.
- Deploy: `firebase deploy --only hosting:taliferro-tech`

Products with no confirmed URL (`None` in `PRODUCTS`) render as "Coming soon" cards without a link.
