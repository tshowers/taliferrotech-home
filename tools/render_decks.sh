#!/bin/bash
# Render both investor decks from src/decks.py with headless Chrome.
#   teaser -> public/files/16ahead-investor-overview.pdf (public, linked from /deck)
#   full   -> deck-private/ (PNG per slide + investor-deck.pdf), never under public/
# Then, with --upload, copies the full deck to gs://taliferro-investor-room/docs/deck/.
set -euo pipefail
cd "$(dirname "$0")/.."
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT=deck-private
rm -rf "$OUT"; mkdir -p "$OUT/slides" public/files
python3 src/decks.py "$OUT" > "$OUT/titles.json"
shot() { "$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=1600,900 --screenshot="$2" "file://$PWD/$1" 2>/dev/null; }
pdf() { "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --print-to-pdf="$2" "file://$PWD/$1" 2>/dev/null; }
for f in "$OUT"/full-[0-9][0-9].html; do
  n=$(basename "$f" .html | sed 's/full-//')
  shot "$f" "$OUT/slides/$n.png"
  sips -s format jpeg -s formatOptions 88 "$OUT/slides/$n.png" --out "$OUT/slides/$n.jpg" >/dev/null && rm "$OUT/slides/$n.png"
done
pdf "$OUT/full-print.html" "$OUT/investor-deck.pdf"
pdf "$OUT/teaser-print.html" public/files/16ahead-investor-overview.pdf
echo "rendered $(ls "$OUT/slides" | wc -l | tr -d ' ') room slides, investor-deck.pdf and the teaser PDF"
if [ "${1:-}" = "--upload" ]; then
  gcloud storage rm -r gs://taliferro-investor-room/docs/deck/ --project taliferro-de66f 2>/dev/null || true
  gcloud storage cp "$OUT/slides/"*.jpg gs://taliferro-investor-room/docs/deck/slides/ --project taliferro-de66f
  gcloud storage cp "$OUT/investor-deck.pdf" gs://taliferro-investor-room/docs/deck/ --project taliferro-de66f
  echo "uploaded to gs://taliferro-investor-room/docs/deck/"
fi
