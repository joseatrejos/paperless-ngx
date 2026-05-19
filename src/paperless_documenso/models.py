from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import models
from django.utils import timezone


class DocumensoGroupLink(models.Model):
    """
    Vincula un Group de Paperless con una organización (Team) en Documenso.
    La API key almacenada es la del equipo en Documenso.
    """

    group = models.OneToOneField(
        Group,
        on_delete=models.CASCADE,
        related_name="documenso_link",
        verbose_name="grupo",
    )
    documenso_org_name = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Nombre de organización Documenso",
        help_text="Nombre del workspace compartido en Documenso (se usará como slug).",
    )
    documenso_team_token = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Token de equipo Documenso",
        help_text="API token del equipo en Documenso. Se asigna automáticamente al provisionar.",
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
    Registra si un usuario ya fue creado en Documenso para un grupo concreto.
    Constraint: evita llamar a la API dos veces para el mismo par (user, link).
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
        help_text="True si el usuario ya fue creado exitosamente en Documenso.",
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
