#!/bin/bash
# Setup scaffolding + download teacher-notes PDFs for the 12 remaining BibleProject courses.
set -u
ROOT="/Users/macbook/Documents/GitHub/abraao-estudo"
cd "$ROOT" || exit 1

# folder-slug  |  pdf-slug (bibleproject)
COURSES=(
  "heaven-and-earth|heaven-and-earth"
  "adam-to-noah|adam-to-noah"
  "jacob|jacob"
  "joseph|joseph"
  "exodus-overview|exodus-overview-carmen-imes"
  "ezekiel|ezekiel"
  "jonah|jonah"
  "messianic-torah|messianic-torah"
  "1-corinthians|1-corinthians-lucy-peppiatt"
  "ephesians|ephesians"
  "intro-hebrew-bible|introduction-to-the-hebrew-bible"
  "art-of-biblical-words|art-of-biblical-words"
)

for entry in "${COURSES[@]}"; do
  folder="${entry%%|*}"
  slug="${entry##*|}"
  dir="$ROOT/$folder"
  mkdir -p "$dir/image" "$dir/js" "$dir/pdf-images"
  # copy verse-modal.js from abraao (shared component)
  cp -f "$ROOT/abraao/js/verse-modal.js" "$dir/js/verse-modal.js"
  pdf="$dir/$folder-teacher-notes.pdf"
  if [ -s "$pdf" ]; then
    echo "SKIP (exists): $folder"
  else
    url="https://documents.bibleproject.com/classroom/teacher-notes/$slug-teacher-notes.pdf"
    code=$(curl -sL "$url" -o "$pdf" -w "%{http_code}")
    size=$(stat -f%z "$pdf" 2>/dev/null || echo 0)
    echo "$code  ${size} bytes  -> $folder"
  fi
done
echo "DONE"
