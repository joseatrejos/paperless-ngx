#!/bin/bash
# Script para iniciar el entorno de desarrollo de paperless-ngx en WSL
# Ejecutar desde WSL Ubuntu: bash ~/paperless-ngx/scripts/start-dev-wsl.sh

PROJECT_PATH="$HOME/paperless-ngx"

export PATH="$HOME/.local/bin:$PATH"

echo "Liberando puerto 8000 si está en uso..."
sudo fuser -k 8000/tcp 2>/dev/null || true

echo "Iniciando Redis..."
sudo service redis-server start 2>/dev/null || sudo redis-server --daemonize yes

echo "Iniciando paperless-ngx en modo desarrollo..."
echo "Presiona Ctrl+C para detener."
echo ""
echo "  -> Webserver: http://localhost:8000"
echo ""

cd "$PROJECT_PATH/src"

# Iniciar todos los servicios
uv run manage.py runserver &
RUNSERVER_PID=$!

uv run manage.py document_consumer &
CONSUMER_PID=$!

uv run celery --app paperless worker -l DEBUG &
CELERY_PID=$!

# Trap para limpiar al salir
trap "echo 'Deteniendo servicios...'; kill $RUNSERVER_PID $CONSUMER_PID $CELERY_PID 2>/dev/null; exit" INT TERM

echo "Servicios iniciados (PIDs: $RUNSERVER_PID, $CONSUMER_PID, $CELERY_PID)"
wait
