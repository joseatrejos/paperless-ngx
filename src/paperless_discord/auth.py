from django.conf import settings
from django.contrib.auth.backends import BaseBackend

from .consts import (
    DISCORD_LOGIN_ERROR_ATTR,
    ERROR_DISCORD_ALLOWED_ROLES_MISSING,
    ERROR_DISCORD_INVALID_IDENTIFIER,
    ERROR_DISCORD_ROLE_REQUIRED,
)
from .managers import DiscordUserManager
from .utils import get_user_by_id, normalize_roles


class DiscordAuthenticationBackend(BaseBackend):
    def authenticate(self, request, user=None, **kwargs):
        if request and hasattr(request, DISCORD_LOGIN_ERROR_ATTR):
            delattr(request, DISCORD_LOGIN_ERROR_ATTR)

        if request is None or not user:
            return None

        user_id = str(user.get("id") or "").strip()
        if not user_id:
            setattr(request, DISCORD_LOGIN_ERROR_ATTR, ERROR_DISCORD_INVALID_IDENTIFIER)
            return None

        allowed_roles = normalize_roles(settings.DISCORD_ALLOWED_ROLES)
        if allowed_roles:
            roles = normalize_roles(user.get("roles", []))
            if not roles.intersection(allowed_roles):
                setattr(request, DISCORD_LOGIN_ERROR_ATTR, ERROR_DISCORD_ROLE_REQUIRED)
                return None

        discord_user = DiscordUserManager().create_or_update_discord_user(user)
        if not discord_user.is_active:
            setattr(request, DISCORD_LOGIN_ERROR_ATTR, ERROR_DISCORD_ALLOWED_ROLES_MISSING)
            return None

        return discord_user

    def get_user(self, user_id):
        return get_user_by_id(user_id)

