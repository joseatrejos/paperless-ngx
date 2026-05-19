import logging

logger = logging.getLogger("paperless.documenso.signals")


def on_group_link_saved(sender, instance, created, **kwargs):
    """
    Fires after a DocumensoGroupLink is saved.
    If an org name is configured, triggers a bulk synchronisation of all
    users in the group asynchronously.
    """
    from paperless_documenso.tasks import sync_all_group_users

    update_fields = kwargs.get("update_fields")
    if update_fields and set(update_fields).issubset({"documenso_team_token"}):
        # Avoid loops: when the task saves the team token, do not re-trigger bulk sync.
        return

    if not instance.is_configured:
        return

    logger.info(
        "DocumensoGroupLink %s saved with org name configured. "
        "Starting bulk synchronisation for group '%s'.",
        instance.pk,
        instance.group.name,
    )
    sync_all_group_users.delay(instance.pk)


def on_user_groups_changed(sender, instance, action, pk_set, **kwargs):
    """
    Fires when the User.groups relationship changes (m2m_changed).
    When a user is added to a group that has a configured DocumensoGroupLink,
    triggers the individual synchronisation task.
    """
    if action != "post_add" or not pk_set:
        return

    from django.contrib.auth.models import Group

    from paperless_documenso.models import DocumensoGroupLink
    from paperless_documenso.tasks import sync_documenso_user

    # pk_set contains the PKs of the groups just added to the user
    linked_groups = DocumensoGroupLink.objects.filter(
        group_id__in=pk_set,
        documenso_org_name__gt="",
    )

    for group_link in linked_groups:
        logger.info(
            "User %s added to group '%s'. Starting Documenso synchronisation.",
            instance.pk,
            group_link.group.name,
        )
        sync_documenso_user.delay(instance.pk, group_link.pk)
