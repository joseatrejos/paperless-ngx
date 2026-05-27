import logging

import httpx
from django.conf import settings

logger = logging.getLogger("paperless.documenso.client")


class DocumensoAPIError(Exception):
    """Raised when the documenso-django API returns an error."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        method: str = "POST",
        url: str = "",
        location: str | None = None,
        response_body: str = "",
    ):
        self.status_code = status_code
        self.detail = detail
        self.method = method
        self.url = url
        self.location = location
        self.response_body = response_body
        # Keep constructor args fully serializable so Celery can pickle this exception.
        super().__init__(
            status_code,
            detail,
            method,
            url,
            location,
            response_body,
        )

    def __str__(self) -> str:
        base = f"Documenso API error {self.status_code} on {self.method} {self.url}: {self.detail}"
        if 300 <= self.status_code < 400 and self.location:
            return (
                f"{base} | redirect location={self.location} "
                "(check DOCUMENSO_API_URL, scheme http/https, and endpoint trailing slash)"
            )
        if self.response_body:
            return f"{base} | response={self.response_body}"
        return base


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
        """Performs a POST request to the API and returns the JSON response."""
        url = f"{self.base_url}{path}"
        try:
            with httpx.Client(timeout=30, follow_redirects=False) as client:
                response = client.post(url, json=payload, headers=self._headers())
        except httpx.RequestError as exc:
            raise DocumensoAPIError(0, str(exc), "POST", url) from exc

        if response.status_code not in (200, 201):
            response_text = (response.text or "").strip()
            response_excerpt = response_text[:300]
            try:
                detail = response.json().get("detail", response_excerpt)
            except Exception:
                detail = response_excerpt
            raise DocumensoAPIError(
                response.status_code,
                detail,
                "POST",
                url,
                response.headers.get("location"),
                response_excerpt,
            )

        return response.json()

    def create_user(self, email: str, name: str, password: str) -> dict:
        """Creates a user in Documenso via documenso-django."""
        data = self._post(
            "/api/documenso/users/",
            {"email": email, "name": name, "password": password},
        )
        logger.info("User created in Documenso: %s", email)
        return data

    def lookup_user_by_email(self, email: str) -> dict | None:
        """Looks up a user in Documenso by email. Returns None if not found."""
        try:
            return self._post("/api/documenso/users/lookup", {"email": email})
        except DocumensoAPIError as exc:
            if exc.status_code == 404:
                return None
            raise

    def provision_workspace(self, org_name: str, owner_email: str) -> dict:
        """Creates (or retrieves) the shared workspace for the group."""
        data = self._post("/api/documenso/workspaces/", {"org_name": org_name, "owner_email": owner_email})
        logger.info("Workspace provisionado en Documenso: %s", org_name)
        return data

    def add_user_to_workspace(self, user_id: int, org_name: str) -> dict:
        """Adds a user to the shared workspace."""
        data = self._post(
            "/api/documenso/workspaces/members",
            {"user_id": user_id, "org_name": org_name},
        )
        logger.info(
            "User %s added to workspace '%s' in Documenso", user_id, org_name
        )
        return data

