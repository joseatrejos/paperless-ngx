from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("paperless", "0010_applicationconfiguration_documenso_team_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="applicationconfiguration",
            name="app_theme_color",
            field=models.CharField(
                verbose_name="Application theme color",
                null=True,
                blank=True,
                max_length=16,
            ),
        ),
    ]
