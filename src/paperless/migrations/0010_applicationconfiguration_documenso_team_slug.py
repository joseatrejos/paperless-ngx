from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("paperless", "0009_alter_applicationconfiguration_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="applicationconfiguration",
            name="documenso_team_slug",
            field=models.CharField(
                blank=True,
                max_length=128,
                null=True,
                verbose_name="Documenso team slug for direct document URL",
            ),
        ),
    ]
