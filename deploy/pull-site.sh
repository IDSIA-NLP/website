#!/usr/bin/env bash
# Runs on the IDSIA web server via cron. If the main branch on GitHub has
# changed (or once a day), it builds the site and copies it to the web folder.
#
# The site is built here from "main" only, so only approved changes go live.
# Needs: git, python3, rsync, curl, and outgoing HTTPS to github.com.
# Hugo is downloaded automatically on first run (single file, no admin rights).
set -euo pipefail

REPO_URL="https://github.com/IDSIA-NLP/website.git"
WEBROOT="/path/to/web/root"            # TODO: folder Apache serves
WORKDIR="$HOME/nlp-website"            # working files (not served)
HUGO_VERSION="0.145.0"

SRC="$WORKDIR/src"
HUGO="$WORKDIR/hugo-$HUGO_VERSION"
STAMP="$WORKDIR/last-build"
mkdir -p "$WORKDIR"

# Hugo, pinned to the same version GitHub uses
if [ ! -x "$HUGO" ]; then
  curl -sSL "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_${HUGO_VERSION}_linux-amd64.tar.gz" \
    | tar -xz -C "$WORKDIR" hugo
  mv "$WORKDIR/hugo" "$HUGO"
fi

# Get the latest approved version
if [ ! -d "$SRC/.git" ]; then
  git clone -q --depth 1 --branch main "$REPO_URL" "$SRC"
else
  git -C "$SRC" fetch -q --depth 1 origin main
  git -C "$SRC" reset -q --hard FETCH_HEAD
fi
REV="$(git -C "$SRC" rev-parse HEAD)"

# Rebuild if main changed, or if the last build is older than a day
# (so projects move from "current" to "past" when their end year passes).
if [ -f "$STAMP" ] && [ "$(cat "$STAMP")" = "$REV" ] && [ -z "$(find "$STAMP" -mmin +1440)" ]; then
  exit 0
fi

cd "$SRC"
python3 scripts/bib2json.py >/dev/null
rm -rf "$WORKDIR/public"
"$HUGO" --gc --minify --quiet -d "$WORKDIR/public"

# --delete removes files that are no longer part of the site.
# Add --exclude lines for anything on the server that must be kept.
rsync -a --delete "$WORKDIR/public/" "$WEBROOT/"
echo "$REV" > "$STAMP"
echo "$(date -Is) built ${REV:0:7}"
