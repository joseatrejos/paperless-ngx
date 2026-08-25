import logging
import os
import time

from django.db import connections
from django.db.utils import InterfaceError
from django.db.utils import OperationalError

logger = logging.getLogger("paperless.db_checks")


def wait_for_database_connection(
    alias: str = "default",
    retry_interval: float | None = None,
    max_retries: int | None = None,
) -> None:
    retry_interval = retry_interval or float(
        os.getenv("PAPERLESS_DB_CONNECT_RETRY_DELAY", 2),
    )
    max_retries = max_retries or int(os.getenv("PAPERLESS_DB_CONNECT_RETRIES", 15))

    connection = connections[alias]
    attempt = 0
    while True:
        attempt += 1
        try:
            connection.ensure_connection()
            logger.info(
                f"[db_checks] Conexión a la base de datos '{alias}' establecida "
                f"(intento {attempt}). Continuando con el arranque del servidor.",
            )
            return
        except (OperationalError, InterfaceError) as e:
            logger.warning(
                f"[db_checks][arranque] Intento {attempt} de conexión a '{alias}' "
                f"falló ({e}). Reintentando en {retry_interval:.0f}s...",
            )
            if attempt >= max_retries:
                logger.critical(
                    f"[db_checks] No se pudo conectar a '{alias}' tras {attempt} "
                    "intentos. El servidor no arrancará.",
                )
                raise SystemExit(1)
            time.sleep(retry_interval)
        finally:
            connection.close()
