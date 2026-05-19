import logging

import httpx
from django.conf import settings

logger = logging.getLogger("paperless.documenso.client")


class DocumensoAPIError(Exception):
    """Excepción lanzada cuando la API de documenso-django devuelve un error."""

    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"Documenso API error {status_code}: {detail}")


class DocumensoClient:
    """
    Cliente HTTP para el servidor documenso-django.

    Usa la clave global DOCUMENSO_API_KEY para autenticar todas las peticiones.
    La URL base se lee de DOCUMENSO_API_URL (ej. http://localhost:8000).

    Endpoints:
        POST {base_url}/api/documenso/users
        POST {base_url}/api/documenso/workspaces
        POST {base_url}/api/documenso/workspaces/members
    """

    def __init__(self):
        self.base_url = (getattr(settings, "DOCUMENSO_API_URL", "") or "").rstrip("/")
        self._api_key = getattr(settings, "DOCUMENSO_API_KEY", "") or ""

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

    def _post(self, path: str, payload: dict) -> dict:
        """Realiza un POST a la API y devuelve el JSON de respuesta."""
        url = f"{self.base_url}{path}"
        try:
            with httpx.Client(timeout=30) as client:
                response = client.post(url, json=payload, headers=self._headers())
        except httpx.RequestError as exc:
            raise DocumensoAPIError(0, str(exc)) from exc

        if response.status_code not in (200, 201):
            try:
                detail = response.json().get("detail", response.text)
            except Exception:
                detail = response.text
            raise DocumensoAPIError(response.status_code, detail)

        return response.json()

    def create_user(self, email: str, name: str, password: str) -> dict:
        """Crea un usuario en Documenso vía documenso-django."""
        data = self._post(
            "/api/documenso/users",
            {"email": email, "name": name, "password": password},
        )
        logger.info("Usuario creado en Documenso: %s", email)
        return data

    def lookup_user_by_email(self, email: str) -> dict | None:
        """Busca un usuario en Documenso por email. Devuelve None si no existe."""
        try:
            return self._post("/api/documenso/users/lookup", {"email": email})
        except DocumensoAPIError as exc:
            if exc.status_code == 404:
                return None
            raise

    def provision_workspace(self, org_name: str) -> dict:
        """Crea (o recupera) el workspace compartido para el grupo."""
        data = self._post("/api/documenso/workspaces", {"org_name": org_name})
        logger.info("Workspace provisionado en Documenso: %s", org_name)
        return data

    def add_user_to_workspace(self, user_id: int, org_name: str) -> dict:
        """Añade un usuario al workspace compartido."""
        data = self._post(
            "/api/documenso/workspaces/members",
            {"user_id": user_id, "org_name": org_name},
        )
        logger.info(
            "Usuario %s añadido al workspace '%s' en Documenso", user_id, org_name
        )
        return data

