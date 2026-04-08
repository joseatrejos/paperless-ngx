from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager

from .consts import DISCORD_FALLBACK_EMAIL_DOMAIN


class DiscordUserManager(UserManager):
    def create_or_update_discord_user(self, discord_user: dict):
        User = get_user_model()

        discord_id = str(discord_user["id"])
        username = f"discord_{discord_id}"
        email = discord_user.get("email") or f"{discord_id}@{DISCORD_FALLBACK_EMAIL_DOMAIN}"
        display_name = (
            discord_user.get("nick")
            or discord_user.get("global_name")
            or discord_user.get("username")
            or username
        )
        parts = display_name.split(" ", 1)
        first_name = parts[0][:150]
        last_name = parts[1][:150] if len(parts) > 1 else ""

        discord_tag = (
            f"{discord_user.get('username')}#{discord_user.get('discriminator')}"
            if discord_user.get("discriminator") and discord_user.get("discriminator") != "0"
            else discord_user.get("username", "")
        )

        user, _ = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "first_name": first_name, "last_name": last_name},
        )

        changed = []
        if user.email != email:
            user.email = email
            changed.append("email")
        if user.first_name != first_name:
            user.first_name = first_name
            changed.append("first_name")
        if user.last_name != last_name:
            user.last_name = last_name
            changed.append("last_name")
        if changed:
            user.save(update_fields=changed)

        from paperless_discord.models import DiscordProfile
        profile, _ = DiscordProfile.objects.get_or_create(user=user, defaults={"discord_id": discord_id})
        if profile.discord_id != discord_id or profile.discord_tag != discord_tag:
            profile.discord_id = discord_id
            profile.discord_tag = discord_tag
            profile.save(update_fields=["discord_id", "discord_tag"])

        return user
