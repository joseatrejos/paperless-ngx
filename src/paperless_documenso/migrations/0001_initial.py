import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DocumensoGroupLink",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "documenso_api_key",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="API Key del equipo/organización en Documenso.",
                        max_length=512,
                        verbose_name="Documenso API Key",
                    ),
                ),
                (
                    "group",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documenso_link",
                        to="auth.group",
                        verbose_name="grupo",
                    ),
                ),
            ],
            options={
                "verbose_name": "Documenso Group Link",
                "verbose_name_plural": "Documenso Group Links",
            },
        ),
        migrations.CreateModel(
            name="DocumensoUserSync",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "synced",
                    models.BooleanField(
                        default=False,
                        help_text="True si el usuario ya fue creado exitosamente en Documenso.",
                    ),
                ),
                (
                    "synced_at",
                    models.DateTimeField(blank=True, null=True),
                ),
                (
                    "group_link",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_syncs",
                        to="paperless_documenso.documensogrouplink",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documenso_syncs",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Documenso User Sync",
                "verbose_name_plural": "Documenso User Syncs",
                "unique_together": {("user", "group_link")},
            },
        ),
    ]
