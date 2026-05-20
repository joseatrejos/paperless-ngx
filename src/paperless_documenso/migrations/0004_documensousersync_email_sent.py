from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("paperless_documenso", "0003_documensogrouplink_documenso_team_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="documensousersync",
            name="email_sent",
            field=models.BooleanField(
                default=False,
                help_text="True if the credentials email was successfully delivered to the user.",
            ),
        ),
    ]
