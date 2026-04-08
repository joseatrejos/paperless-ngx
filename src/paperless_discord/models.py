from django.contrib.auth import get_user_model
from django.db import models


class DiscordProfile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="discord_profile",
    )
    discord_id = models.CharField(max_length=255, unique=True)
    discord_tag = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        verbose_name = "Discord Profile"
        verbose_name_plural = "Discord Profiles"

    def __str__(self):
        return f"{self.user} ({self.discord_id})"
