import logging

from django.conf import settings
from django.db.utils import InterfaceError
from django.db.utils import OperationalError
from django.http import JsonResponse

from paperless import version

logger = logging.getLogger("paperless.db_checks")


class ApiVersionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            versions = settings.REST_FRAMEWORK["ALLOWED_VERSIONS"]
            response["X-Api-Version"] = versions[len(versions) - 1]
            response["X-Version"] = version.__full_version_str__

        return response


class DatabaseConnectionMiddleware:
    """
    Si la conexión a la base de datos se pierde mientras el proyecto ya
    está corriendo (login, index, /api/status/, cualquier vista), esto
    responde con un 503 controlado en vez de dejar que la petición
    truene con un 500 sin contexto (o la página de debug si DEBUG está
    habilitado).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, (OperationalError, InterfaceError)):
            logger.error(
                f"Error de conexión a la base de datos durante la petición "
                f"{request.path}: {exception}",
            )
            return JsonResponse(
                {
                    "error": "database_unavailable",
                    "detail": "El servicio no está disponible en este momento. Intenta de nuevo más tarde.",
                },
                status=503,
            )
        return None
