from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from django.utils import timezone


class DocumensoGroupLink(models.Model):
    """
    Links a Paperless Group to an organisation (Team) in Documenso.
    The stored API key belongs to the team in Documenso.
    """

    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        related_name="documenso_link",
        verbose_name="group",
    )
    documenso_org_name = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Documenso organisation name",
        help_text="Name of the shared workspace in Documenso (used as a slug).",
    )
    documenso_team_token = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Documenso team token",
        help_text="API token for the team in Documenso. Assigned automatically when provisioning.",
    )

    class Meta:
        verbose_name = "Documenso Group Link"
        verbose_name_plural = "Documenso Group Links"

    def __str__(self):
        return f"{self.group.name} → Documenso"

    @property
    def is_configured(self) -> bool:
        return bool(self.documenso_org_name)


class DocumensoUserSync(models.Model):
    """
    Records whether a user has already been created in Documenso for a specific group.
    Constraint: prevents calling the API twice for the same (user, group_link) pair.
    """

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="documenso_syncs",
    )
    group_link = models.ForeignKey(
        DocumensoGroupLink,
        on_delete=models.CASCADE,
        related_name="user_syncs",
    )
    synced = models.BooleanField(
        default=False,
        help_text="True if the user has already been successfully created in Documenso.",
    )
    synced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Documenso User Sync"
        verbose_name_plural = "Documenso User Syncs"
        unique_together = ("user", "group_link")

    def __str__(self):
        status = "✓" if self.synced else "✗"
        return f"{status} {self.user} @ {self.group_link}"

    def mark_synced(self):
        self.synced = True
        self.synced_at = timezone.now()
        self.save(update_fields=["synced", "synced_at"])
