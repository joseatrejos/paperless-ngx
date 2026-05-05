from urllib.parse import urlencode, urlparse

import httpx
from django.conf import settings
from django.urls import reverse

from .consts import (
    DISCORD_API_TIMEOUT,
    DISCORD_GUILD_MEMBER_PATH,
    DISCORD_REDIRECT_ROUTE_NAME,
    DISCORD_TOKEN_PATH,
    DISCORD_USER_PATH,
    LOCAL_DEV_HOSTS,
)


def has_discord_configuration():
    return all([
        settings.DISCORD_CLIENT_ID,
        settings.DISCORD_CLIENT_SECRET,
        settings.DISCORD_SCOPES,
    ])


def get_redirect_uri(request):
    callback_uri = request.build_absolute_uri(reverse(DISCORD_REDIRECT_ROUTE_NAME))
    protocol = getattr(settings, "ACCOUNT_DEFAULT_HTTP_PROTOCOL", "http")
    parsed = urlparse(callback_uri)
    callback_uri = parsed._replace(scheme=protocol).geturl()

    if not settings.DISCORD_REDIRECT_URI:
        return callback_uri

    configured_uri = urlparse(settings.DISCORD_REDIRECT_URI)
    request_uri = urlparse(callback_uri)

    if configured_uri.hostname in LOCAL_DEV_HOSTS and configured_uri.netloc != request_uri.netloc:
        return callback_uri

    return settings.DISCORD_REDIRECT_URI


def build_authorization_url(request, state):
    params = {
        "client_id": settings.DISCORD_CLIENT_ID,
        "redirect_uri": get_redirect_uri(request),
        "response_type": settings.DISCORD_RESPONSE_TYPE,
        "scope": " ".join(settings.DISCORD_SCOPES),
        "state": state,
    }
    return f"{settings.DISCORD_AUTH_URL}?{urlencode(params)}"


def exchange_code_for_token(request, code):
    if not code:
        return None

    data = {
        "client_id": settings.DISCORD_CLIENT_ID,
        "client_secret": settings.DISCORD_CLIENT_SECRET,
        "grant_type": settings.DISCORD_GRANT_TYPE,
        "code": code,
        "redirect_uri": get_redirect_uri(request),
        "scope": " ".join(settings.DISCORD_SCOPES),
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = httpx.post(
            f"{settings.DISCORD_API_URL}{DISCORD_TOKEN_PATH}",
            data=data, headers=headers, timeout=DISCORD_API_TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
    except (httpx.HTTPError, ValueError):
        return None

    return payload.get("access_token")


def get_discord_guild_member(access_token):
    if not access_token or not settings.DISCORD_GUILD_ID:
        return None

    try:
        response = httpx.get(
            f"{settings.DISCORD_API_URL}{DISCORD_GUILD_MEMBER_PATH.format(guild_id=settings.DISCORD_GUILD_ID)}",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=DISCORD_API_TIMEOUT,
        )
        if response.status_code in {401, 403, 404}:
            return None
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPError, ValueError):
        return None


def get_discord_user(access_token):
    if not access_token:
        return None

    try:
        response = httpx.get(
            f"{settings.DISCORD_API_URL}{DISCORD_USER_PATH}",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=DISCORD_API_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()
    except (httpx.HTTPError, ValueError):
        return None
