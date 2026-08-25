#!/bin/bash
# Script de configuración del entorno de desarrollo de paperless-ngx en WSL
# Ejecutar desde WSL Ubuntu: bash /ruta/al/repo/paperless-ngx/scripts/setup-dev-wsl.sh [ruta-del-repo]
# Si no se pasa ruta, usa la carpeta padre de este script.

set -e

PROJECT_PATH="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"

echo "=========================================="
echo "  Configurando paperless-ngx para desarrollo en WSL"
echo "  Repo: $PROJECT_PATH"
echo "=========================================="

# 1. Instalar dependencias del sistema
echo ""
echo "[1/7] Instalando dependencias del sistema..."
sudo apt-get update -qq
sudo apt-get install -y \
    python3 python3-pip python3-dev \
    imagemagick fonts-liberation gnupg \
    libpq-dev default-libmysqlclient-dev \
    pkg-config libmagic-dev poppler-utils \
    unpaper ghostscript icc-profiles-free \
    qpdf liblept5 libxml2 pngquant zlib1g \
    tesseract-ocr tesseract-ocr-spa \
    build-essential python3-setuptools python3-wheel \
    redis-server

# 2. Instalar uv si no está instalado
echo ""
echo "[2/7] Verificando uv..."
if ! command -v uv &>/dev/null; then
    if [ -f "$HOME/.local/bin/uv" ]; then
        export PATH="$HOME/.local/bin:$PATH"
    else
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.local/bin:$PATH"
    fi
fi
echo "uv $(uv --version)"

# 3. Instalar Node.js + pnpm (necesario para compilar src-ui)
echo ""
echo "[3/7] Verificando Node.js y pnpm..."
if ! command -v node &>/dev/null || [ "$(node -v | sed 's/^v//' | cut -d. -f1)" -lt 20 ]; then
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi
echo "node $(node -v)"

sudo corepack enable
PNPM_VERSION=$(grep -m1 '"packageManager"' "$PROJECT_PATH/src-ui/package.json" | sed -E 's/.*pnpm@([0-9.]+).*/\1/')
corepack prepare "pnpm@${PNPM_VERSION:-10.17.1}" --activate
echo "pnpm $(pnpm --version)"

# 4. Crear directorios necesarios
echo ""
echo "[4/7] Creando directorios consume y media..."
mkdir -p "$PROJECT_PATH/consume" "$PROJECT_PATH/media"

# 5. Configurar paperless.conf
echo ""
echo "[5/7] Configurando paperless.conf..."
CONF_FILE="$PROJECT_PATH/paperless.conf"
if [ ! -f "$CONF_FILE" ]; then
    cp "$PROJECT_PATH/paperless.conf.example" "$CONF_FILE"
fi

# Activar modo debug si no está activo
if ! grep -q "^PAPERLESS_DEBUG=true" "$CONF_FILE"; then
    sed -i 's/^#\?PAPERLESS_DEBUG=.*/PAPERLESS_DEBUG=true/' "$CONF_FILE" 2>/dev/null || \
        echo "PAPERLESS_DEBUG=true" >> "$CONF_FILE"
fi

# Configurar la URL del host de Redis (default ya está bien)
echo "paperless.conf configurado."

# 6. Instalar dependencias Python y frontend
echo ""
echo "[6/7] Instalando dependencias Python (uv) y frontend (pnpm)..."
cd "$PROJECT_PATH"
uv sync --group dev
cd "$PROJECT_PATH/src-ui"
pnpm install

# 7. Aplicar migraciones
echo ""
echo "[7/7] Aplicando migraciones de base de datos..."
cd "$PROJECT_PATH/src"
uv run manage.py migrate

echo ""
echo "=========================================="
echo "  ¡Configuración completada!"
echo "=========================================="
echo ""
echo "Para crear el superusuario (la primera vez):"
echo "  cd $PROJECT_PATH/src"
echo "  uv run manage.py createsuperuser"
echo ""
echo "Para iniciar Redis (necesario antes del servidor):"
echo "  sudo service redis-server start"
echo ""
echo "Para iniciar el backend de desarrollo:"
echo "  cd $PROJECT_PATH/src"
echo "  uv run manage.py runserver &"
echo "  uv run manage.py document_consumer &"
echo "  uv run celery --app paperless worker -l DEBUG"
echo ""
echo "El servidor estará disponible en: http://localhost:8000"
