import logging
import random
import string

from celery import shared_task
from django.contrib.auth import get_user_model

from documents.mail import build_system_themed_email
from documents.mail import send_email
from paperless_documenso.client import DocumensoAPIError
from paperless_documenso.client import DocumensoClient

logger = logging.getLogger("paperless.documenso.tasks")

User = get_user_model()


def _generate_password(first_name: str, last_name: str) -> str:
    """
    Genera una contraseña temporal con el formato:
      nombre + 4 dígitos aleatorios + apellido
    Ej: David4821Acosta
    """
    digits = "".join(random.choices(string.digits, k=4))
    first = (first_name or "user").strip()
    last = (last_name or "").strip()
    return f"{first}{digits}{last}"


def _send_credentials_email(email: str, name: str, password: str, documenso_url: str = "") -> None:
    """Envía las credenciales de Documenso al usuario con el diseño estándar de Paperless."""
    subject = "Tus credenciales en Documenso"

    login_line = f"\n🔗 Accede aquí: {documenso_url}" if documenso_url else ""

    body = (
        f"Hola {name},\n\n"
        f"Tu cuenta en Documenso ha sido creada exitosamente.\n\n"
        f"📧 Usuario: {email}\n"
        f"🔑 Contraseña temporal: {password}"
        f"{login_line}\n\n"
        f"Por seguridad, te recomendamos cambiar tu contraseña al iniciar sesión por primera vez."
    )

    html_message, inline_images = build_system_themed_email(
        subject=subject,
        body=body,
        doc_url=documenso_url,
    )

    send_email(
        subject=subject,
        body=body,
        to=[email],
        attachments=[],
        html_message=html_message,
        inline_images=inline_images,
    )


@shared_task
def sync_documenso_user(user_id: int, group_link_id: int) -> str:
    """
    Crea un usuario en Documenso para el par (user, group_link) si aún no fue sincronizado,
    provisiona el workspace del grupo si no existe, y añade al usuario al workspace.
    Envía las credenciales al correo del usuario.
    """
    from paperless_documenso.models import DocumensoGroupLink
    from paperless_documenso.models import DocumensoUserSync

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logger.warning("sync_documenso_user: usuario %s no encontrado", user_id)
        return f"User {user_id} not found"

    try:
        group_link = DocumensoGroupLink.objects.get(pk=group_link_id)
    except DocumensoGroupLink.DoesNotExist:
        logger.warning(
            "sync_documenso_user: group_link %s no encontrado", group_link_id
        )
        return f"GroupLink {group_link_id} not found"

    if not group_link.is_configured:
        return f"GroupLink {group_link_id} no tiene org name configurado"

    if not user.email:
        logger.info(
            "sync_documenso_user: usuario %s no tiene email, omitiendo", user_id
        )
        return f"User {user_id} has no email"

    # Constraint: no llamar a Documenso si ya fue sincronizado
    sync_record, _ = DocumensoUserSync.objects.get_or_create(
        user=user,
        group_link=group_link,
    )
    if sync_record.synced:
        logger.info(
            "sync_documenso_user: usuario %s ya sincronizado para group_link %s, omitiendo",
            user_id,
            group_link_id,
        )
        return f"User {user_id} already synced for group_link {group_link_id}"

    org_name = group_link.documenso_org_name
    name = f"{user.first_name} {user.last_name}".strip() or user.username
    client = DocumensoClient()

    # 1. Buscar usuario por email; si no existe, crearlo
    created_password: str | None = None
    user_data = client.lookup_user_by_email(user.email)
    if user_data:
        logger.info(
            "sync_documenso_user: usuario %s ya existe en Documenso, se reutiliza",
            user.email,
        )
    else:
        password = _generate_password(user.first_name, user.last_name)
        try:
            user_data = client.create_user(email=user.email, name=name, password=password)
            created_password = password
        except DocumensoAPIError as exc:
            # Si hubo carrera y otro worker lo creó justo antes, recuperamos por email.
            if exc.status_code == 409:
                user_data = client.lookup_user_by_email(user.email)
                if not user_data:
                    logger.error(
                        "sync_documenso_user: conflicto al crear %s, pero lookup posterior no encontró usuario",
                        user.email,
                    )
                    return f"Conflict creating user {user.email}, and lookup did not find the user"
            else:
                logger.error(
                    "sync_documenso_user: error al crear usuario %s en Documenso: %s",
                    user.email,
                    exc,
                )
                return f"Error creating user {user.email} in Documenso: {exc}"

    documenso_user_id = user_data.get("id") if isinstance(user_data, dict) else None

    # 2. Provisionar workspace (idempotente) y capturar token si se genera uno nuevo
    try:
        workspace_data = client.provision_workspace(org_name=org_name)
        team_token = workspace_data.get("team_token") if isinstance(workspace_data, dict) else None
        if team_token:
            group_link.documenso_team_token = team_token
            group_link.save(update_fields=["documenso_team_token"])
            logger.info(
                "sync_documenso_user: team_token guardado para group_link %s",
                group_link_id,
            )
    except DocumensoAPIError as exc:
        logger.error(
            "sync_documenso_user: error al provisionar workspace '%s': %s",
            org_name,
            exc,
        )
        return f"Error provisioning workspace '{org_name}': {exc}"

    # 3. Añadir usuario al workspace
    if documenso_user_id:
        try:
            client.add_user_to_workspace(user_id=documenso_user_id, org_name=org_name)
        except DocumensoAPIError as exc:
            logger.error(
                "sync_documenso_user: error al añadir usuario %s al workspace '%s': %s",
                user.email,
                org_name,
                exc,
            )
            # No bloqueamos la sincronización por este error

    # 4. Enviar credenciales por correo
    from django.conf import settings as django_settings
    documenso_url = getattr(django_settings, "DOCUMENSO_URL", "")
    if created_password is not None:
        try:
            _send_credentials_email(
                email=user.email,
                name=name,
                password=created_password,
                documenso_url=documenso_url,
            )
        except Exception as exc:
            logger.error(
                "sync_documenso_user: error al enviar correo a %s: %s",
                user.email,
                exc,
            )
            # Aunque el correo falle, el usuario ya fue creado — marcamos como sincronizado
            # para no crear duplicados en Documenso.

    sync_record.mark_synced()
    logger.info(
        "sync_documenso_user: usuario %s sincronizado exitosamente en group_link %s",
        user.email,
        group_link_id,
    )
    return f"User {user.email} synced to Documenso for group_link {group_link_id}"


@shared_task
def sync_all_group_users(group_link_id: int) -> str:
    """
    Itera todos los usuarios del grupo y lanza sync_documenso_user para cada uno.
    Se ejecuta cuando se asigna o actualiza el org name de un DocumensoGroupLink.
    """
    from paperless_documenso.models import DocumensoGroupLink

    try:
        group_link = DocumensoGroupLink.objects.select_related("group").get(
            pk=group_link_id
        )
    except DocumensoGroupLink.DoesNotExist:
        logger.warning(
            "sync_all_group_users: group_link %s no encontrado", group_link_id
        )
        return f"GroupLink {group_link_id} not found"

    if not group_link.is_configured:
        return f"GroupLink {group_link_id} no tiene org name configurado"

    # Provisionar el workspace inmediatamente, aunque el grupo esté vacío.
    # Esto garantiza que la Organización y el Team existan en Documenso
    # antes de que se agreguen usuarios.
    client = DocumensoClient()
    try:
        workspace_data = client.provision_workspace(org_name=group_link.documenso_org_name)
        logger.info(
            "sync_all_group_users: workspace '%s' provisionado para group_link %s",
            group_link.documenso_org_name,
            group_link_id,
        )
        # Guardar el token del equipo si se recibió y aún no está almacenado
        team_token = workspace_data.get("team_token") if isinstance(workspace_data, dict) else None
        if team_token:
            group_link.documenso_team_token = team_token
            group_link.save(update_fields=["documenso_team_token"])
            logger.info(
                "sync_all_group_users: team_token guardado para group_link %s",
                group_link_id,
            )
    except DocumensoAPIError as exc:
        logger.error(
            "sync_all_group_users: error al provisionar workspace '%s': %s",
            group_link.documenso_org_name,
            exc,
        )
        return f"Error provisioning workspace '{group_link.documenso_org_name}': {exc}"

    users = group_link.group.user_set.all()
    count = 0
    for user in users:
        sync_documenso_user.delay(user.pk, group_link_id)
        count += 1

    logger.info(
        "sync_all_group_users: encoladas %s tareas de sincronización para group_link %s",
        count,
        group_link_id,
    )
    return f"Queued {count} sync tasks for group_link {group_link_id}"

