from django.apps import AppConfig


class PaperlessDocumensoConfig(AppConfig):
    name = "paperless_documenso"
    verbose_name = "Paperless Documenso"

    def ready(self):
        from django.contrib.auth import get_user_model
        from django.db.models.signals import m2m_changed
        from django.db.models.signals import post_save

        from paperless_documenso.models import DocumensoGroupLink
        from paperless_documenso.signals import on_group_link_saved
        from paperless_documenso.signals import on_user_groups_changed

        User = get_user_model()

        post_save.connect(
            on_group_link_saved,
            sender=DocumensoGroupLink,
            dispatch_uid="documenso_group_link_saved",
        )
        m2m_changed.connect(
            on_user_groups_changed,
            sender=User.groups.through,
            dispatch_uid="documenso_user_groups_changed",
        )
