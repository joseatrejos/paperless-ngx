# Guía de despliegue de Paperless-ngx

## 1) Antes de Docker (preparación)

Copia el archivo de ejemplo y edítalo:

```bash
cp docker/compose/docker-compose.example.env docker/compose/docker-compose.env
```

Cambia estas variables:

```env
# Obligatorias
PAPERLESS_SECRET_KEY=       # genera con: python3 -c "import secrets; print(secrets.token_urlsafe(64))"
PAPERLESS_WEB_PORT=9000     # puerto del host — verifica que esté libre en el servidor
```

```env
# Recomendadas revisar
COMPOSE_PROJECT_NAME=paperless-deploy  # nombre único por stack en el servidor
PAPERLESS_POSTGRES_DB=paperless
PAPERLESS_POSTGRES_USER=paperless
PAPERLESS_POSTGRES_PORT=5432
PAPERLESS_POSTGRES_PASSWORD= # contraseña de la base de datos
```

Si vas a enviar correos (notificaciones, consumo por mail), agrega esto en `paperless.conf`:

```env
PAPERLESS_EMAIL_HOST=smtp.gmail.com
PAPERLESS_EMAIL_PORT=587
PAPERLESS_EMAIL_USE_TLS=true
PAPERLESS_EMAIL_HOST_USER=tu-correo@gmail.com
PAPERLESS_EMAIL_HOST_PASSWORD=tu-app-password
```

---

## 2) Durante Docker (arranque)

Desde la raíz del repositorio:

```bash
docker compose -f docker/compose/docker-compose.deploy.yml --env-file docker/compose/docker-compose.env up -d
```

Verifica estado de servicios:

```bash
docker compose -f docker/compose/docker-compose.deploy.yml --env-file docker/compose/docker-compose.env ps
```

Ver logs del webserver si algo no inicia:

```bash
docker compose -f docker/compose/docker-compose.deploy.yml --env-file docker/compose/docker-compose.env logs -f webserver
```

---

## 3) Después de Docker (post-arranque)

### Crear usuario administrador

```bash
docker compose -f docker/compose/docker-compose.deploy.yml --env-file docker/compose/docker-compose.env exec webserver python3 manage.py createsuperuser
```

### Entrar a la app

- Local: `http://localhost:9000`
- Servidor: `http://IP_DEL_SERVIDOR:PUERTO`
- Con dominio: `https://tu-dominio.com`

### Comandos útiles de operación

```bash
# Reiniciar aplicando cambios de variables
docker compose -f docker/compose/docker-compose.deploy.yml --env-file docker/compose/docker-compose.env up -d --force-recreate

# Apagar sin borrar datos
docker compose -f docker/compose/docker-compose.deploy.yml --env-file docker/compose/docker-compose.env down

# Apagar y borrar datos (cuidado)
docker compose -f docker/compose/docker-compose.deploy.yml --env-file docker/compose/docker-compose.env down -v

# Rebuild de imagen local
docker build -t paperless-ngx:local .
docker compose -f docker/compose/docker-compose.deploy.yml --env-file docker/compose/docker-compose.env up -d --force-recreate webserver
```

---

## 4) Migraciones (después de cada rebuild con cambios en modelos)

Siempre que se agreguen nuevos modelos o se modifiquen campos existentes, genera y aplica las migraciones:

```bash
# Generar migraciones pendientes
docker compose -f docker/compose/docker-compose.deploy.yml --env-file docker/compose/docker-compose.env exec webserver python3 manage.py makemigrations

# Aplicar migraciones
docker compose -f docker/compose/docker-compose.deploy.yml --env-file docker/compose/docker-compose.env exec webserver python3 manage.py migrate
```
---

## 5) Al final: ejecutar `seed_all` (una vez)

Ejecuta este comando solo una vez en una instalación nueva:

```bash
docker compose -f docker/compose/docker-compose.deploy.yml --env-file docker/compose/docker-compose.env exec webserver python3 manage.py seed_all
```
