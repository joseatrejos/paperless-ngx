import logging

logger = logging.getLogger("paperless.documenso.signals")


def on_group_link_saved(sender, instance, created, **kwargs):
    """
    Se dispara después de guardar un DocumensoGroupLink.
    Si tiene API key configurada, lanza la sincronización masiva de todos
    los usuarios del grupo de forma asíncrona.
    """
    from paperless_documenso.tasks import sync_all_group_users

    update_fields = kwargs.get("update_fields")
    if update_fields and set(update_fields).issubset({"documenso_team_token"}):
        # Evita bucles: cuando la tarea guarda el team token, no relanzamos sync masivo.
        return

    if not instance.is_configured:
        return

    logger.info(
        "DocumensoGroupLink %s guardado con API key. "
        "Iniciando sincronización masiva del grupo '%s'.",
        instance.pk,
        instance.group.name,
    )
    sync_all_group_users.delay(instance.pk)


def on_user_groups_changed(sender, instance, action, pk_set, **kwargs):
    """
    Se dispara cuando cambia la relación User.groups (m2m_changed).
    Cuando se agrega un usuario a un grupo que tiene DocumensoGroupLink configurado,
    lanza la tarea de sincronización individual.
    """
    if action != "post_add" or not pk_set:
        return

    from django.contrib.auth.models import Group

    from paperless_documenso.models import DocumensoGroupLink
    from paperless_documenso.tasks import sync_documenso_user

    # pk_set contiene los PKs de los grupos recién añadidos al usuario
    linked_groups = DocumensoGroupLink.objects.filter(
        group_id__in=pk_set,
        documenso_org_name__gt="",
    )

    for group_link in linked_groups:
        logger.info(
            "Usuario %s añadido al grupo '%s'. Iniciando sincronización Documenso.",
            instance.pk,
            group_link.group.name,
        )
        sync_documenso_user.delay(instance.pk, group_link.pk)
