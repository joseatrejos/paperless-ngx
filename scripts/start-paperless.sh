#!/bin/bash
# start-paperless.sh — [opcional: sincroniza desde Windows], compila frontend, despliega estáticos y arranca todos los servicios.
# Uso: bash start-paperless.sh [ruta-repo-wsl] [ruta-repo-windows-opcional]
# Si no se pasa ruta-repo-wsl, usa la carpeta padre de este script.
# Si se pasa ruta-repo-windows, sincroniza src/ y src-ui/src/ desde ahí antes de compilar (útil solo si editas en Windows y compilas en WSL).

set -e

REPO="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
WIN_REPO="${2:-}"
DIST="$REPO/src-ui/dist/paperless-ui"
APP_STATIC="$REPO/src/documents/static/frontend"

source "$HOME/.local/bin/env" 2>/dev/null || true

# ── 1. Sincronizar código de Windows → WSL (opcional) ────────────────────────
if [ -n "$WIN_REPO" ]; then
    echo "==> Sincronizando archivos desde Windows ($WIN_REPO)..."
    rsync -a --checksum \
        --exclude='__pycache__' --exclude='*.pyc' \
        --exclude='node_modules' --exclude='.git' \
        --exclude='dist' --exclude='static' \
        "$WIN_REPO/src/"     "$REPO/src/" 2>/dev/null | head -5 || \
        cp -r "$WIN_REPO/src/." "$REPO/src/"

    rsync -a --checksum \
        --exclude='node_modules' --exclude='dist' \
        "$WIN_REPO/src-ui/src/"  "$REPO/src-ui/src/" 2>/dev/null | head -5 || \
        cp -r "$WIN_REPO/src-ui/src/." "$REPO/src-ui/src/"
fi

# ── 2. Compilar frontend ─────────────────────────────────────────────────────
echo "==> Compilando frontend (pnpm build)..."
cd "$REPO/src-ui"
pnpm build

# ── 3. Copiar build → carpeta estática de la app ────────────────────────────
echo "==> Copiando build a app static..."
for locale_dir in "$DIST"/*/; do
    locale=$(basename "$locale_dir")
    dest="$APP_STATIC/$locale"
    mkdir -p "$dest"
    cp -r "$locale_dir." "$dest/"
done

# ── 4. Collectstatic ─────────────────────────────────────────────────────────
echo "==> Ejecutando collectstatic..."
cd "$REPO/src"
uv run python manage.py collectstatic --no-input --clear 2>&1 | tail -3

# ── 5. Detener procesos anteriores ───────────────────────────────────────────
echo "==> Deteniendo procesos anteriores..."
sudo fuser -k 8000/tcp 2>/dev/null || true
sudo pkill -f 'celery' 2>/dev/null || true
sudo pkill -f 'document_consumer' 2>/dev/null || true
sleep 1

# ── 6. Iniciar servicios ─────────────────────────────────────────────────────
echo "==> Iniciando Redis..."
sudo service redis-server start

echo "==> Iniciando Daphne (web)..."
nohup uv run daphne -b 0.0.0.0 -p 8000 paperless.asgi:application > /tmp/paperless-web.log 2>&1 &
echo "  PID web: $!"

nohup uv run celery --app paperless worker -l INFO > /tmp/paperless-celery.log 2>&1 &
echo "  PID celery: $!"

nohup uv run manage.py document_consumer > /tmp/paperless-consumer.log 2>&1 &
echo "  PID consumer: $!"

echo ""
echo "Esperando que inicie..."
sleep 4
echo ""

if ss -tlnp 2>/dev/null | grep -q 8000; then
    echo "Paperless-ngx corriendo en http://localhost:8000"
    echo "(Usa Ctrl+Shift+R en el navegador si ves la versión anterior)"
else
    echo "ERROR: el servidor no levantó. Revisa el log:"
    tail -20 /tmp/paperless-web.log
fi

echo "Logs: /tmp/paperless-web.log | /tmp/paperless-celery.log | /tmp/paperless-consumer.log"
