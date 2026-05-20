from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("paperless_documenso", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="documensogrouplink",
            old_name="documenso_api_key",
            new_name="documenso_org_name",
        ),
    ]
