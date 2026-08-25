#!/bin/bash
# Rebuild the frontend and deploy it to static files.
# Run this whenever you change something in src-ui/.

set -e

REPO="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
DIST="$REPO/src-ui/dist/paperless-ui"
APP_STATIC="$REPO/src/documents/static/frontend"

echo "==> Building frontend..."
cd "$REPO/src-ui"
source "$HOME/.local/bin/env" 2>/dev/null || true
pnpm build

echo "==> Copying build to app static folder..."
for locale_dir in "$DIST"/*/; do
    locale=$(basename "$locale_dir")
    dest="$APP_STATIC/$locale"
    mkdir -p "$dest"
    cp -r "$locale_dir." "$dest/"
done

echo "==> Running collectstatic..."
cd "$REPO/src"
uv run python manage.py collectstatic --no-input --clear

echo ""
echo "Done. Reload the browser (Ctrl+Shift+R) to see changes."
