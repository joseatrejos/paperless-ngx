from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("paperless_documenso", "0002_rename_documenso_api_key_documensogrouplink_documenso_org_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="documensogrouplink",
            name="documenso_team_token",
            field=models.CharField(
                blank=True,
                default="",
                help_text="API token del equipo en Documenso. Se asigna automáticamente al provisionar.",
                max_length=255,
                verbose_name="Token de equipo Documenso",
            ),
        ),
    ]
