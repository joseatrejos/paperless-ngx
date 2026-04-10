from __future__ import annotations

from dataclasses import dataclass
from email import message_from_bytes
from email.mime.image import MIMEImage
import mimetypes
from pathlib import Path

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from filelock import FileLock

from paperless.config import GeneralConfig
from paperless.models import ApplicationConfiguration


@dataclass(frozen=True)
class EmailAttachment:
    path: Path
    mime_type: str
    friendly_name: str


@dataclass(frozen=True)
class EmailInlineImage:
    content_id: str
    data: bytes
    subtype: str  # e.g. "png", "jpeg", "svg+xml"


def build_system_themed_email(
    *,
    subject: str,
    body: str,
    doc_url: str = "",
) -> tuple[str, list[EmailInlineImage] | None]:
    """Render the standard branded HTML email using system-wide configuration."""
    paperless_default_color = "#17541f"
    email_logo_cid = "email_logo"
    legacy_theme_keys = ("app_theme_color", "general-settings:theme:color")

    def _get_legacy_theme_color() -> str | None:
        try:
            # Import lazily to avoid circular imports during Django app loading.
            from documents.models import UiSettings

            for user_settings in UiSettings.objects.exclude(settings=None):
                settings_json = user_settings.settings
                if not isinstance(settings_json, dict):
                    continue

                for key in legacy_theme_keys:
                    value = settings_json.get(key)
                    if isinstance(value, str) and value.strip():
                        return value.strip()
        except Exception:
            return None

        return None

    try:
        general_config = GeneralConfig()
        theme_color = (
            general_config.app_theme_color
            or _get_legacy_theme_color()
            or paperless_default_color
        )
        app_title = general_config.app_title or settings.APP_TITLE or "Paperless-ngx"
    except Exception:
        theme_color = _get_legacy_theme_color() or paperless_default_color
        app_title = settings.APP_TITLE or "Paperless-ngx"

    inline_images: list[EmailInlineImage] = []
    logo_src: str | None = None

    try:
        app_cfg = ApplicationConfiguration.objects.first()
        if app_cfg and app_cfg.app_logo:
            mime_type, _ = mimetypes.guess_type(app_cfg.app_logo.name)
            mime_type = mime_type or "image/png"
            subtype = mime_type.split("/", 1)[1]
            logo_bytes = app_cfg.app_logo.read()
            inline_images = [
                EmailInlineImage(
                    content_id=email_logo_cid,
                    data=logo_bytes,
                    subtype=subtype,
                )
            ]
            logo_src = f"cid:{email_logo_cid}"
    except Exception:
        pass

    if not logo_src:
        logo_src = settings.APP_LOGO

    html_message = render_to_string(
        "account/email/workflow_notification.html",
        {
            "subject": subject,
            "body": body,
            "doc_url": doc_url,
            "app_title": app_title,
            "logo_url": logo_src,
            "primary_color": theme_color,
        },
    )

    return html_message, (inline_images or None)


def send_email(
    subject: str,
    body: str,
    to: list[str],
    attachments: list[EmailAttachment],
    html_message: str | None = None,
    inline_images: list[EmailInlineImage] | None = None,
) -> int:
    """
    Send an email with optional HTML alternative, inline images (CID), and attachments.

    Args:
        subject: Email subject
        body: Plain-text email body (used as fallback when html_message is provided)
        to: List of recipient email addresses
        attachments: List of attachments
        html_message: Optional HTML body; when provided the email is sent as multipart/alternative
        inline_images: Optional list of images to embed inline via Content-ID (cid:)

    Returns:
        Number of emails sent

    TODO: re-evaluate this pending https://code.djangoproject.com/ticket/35581 / https://github.com/django/django/pull/18966
    """
    if html_message:
        email: EmailMessage = EmailMultiAlternatives(
            subject=subject,
            body=body,
            to=to,
        )
        email.attach_alternative(html_message, "text/html")
        if inline_images:
            # multipart/related allows HTML to reference inline images via cid:
            email.mixed_subtype = "related"
            for img in inline_images:
                mime_img = MIMEImage(img.data, _subtype=img.subtype)
                mime_img.add_header("Content-ID", f"<{img.content_id}>")
                mime_img.add_header(
                    "Content-Disposition", "inline", filename=f"{img.content_id}.{img.subtype}"
                )
                email.attach(mime_img)
    else:
        email = EmailMessage(
            subject=subject,
            body=body,
            to=to,
        )

    used_filenames: set[str] = set()

    # Something could be renaming the file concurrently so it can't be attached
    with FileLock(settings.MEDIA_LOCK):
        for attachment in attachments:
            filename = _get_unique_filename(
                attachment.friendly_name,
                used_filenames,
            )
            used_filenames.add(filename)

            with attachment.path.open("rb") as f:
                content = f.read()
                if attachment.mime_type == "message/rfc822":
                    # See https://forum.djangoproject.com/t/using-emailmessage-with-an-attached-email-file-crashes-due-to-non-ascii/37981
                    content = message_from_bytes(content)

                email.attach(
                    filename=filename,
                    content=content,
                    mimetype=attachment.mime_type,
                )

    return email.send()


def _get_unique_filename(friendly_name: str, used_names: set[str]) -> str:
    """
    Constructs a unique friendly filename for the given document, append a counter if needed.
    """
    if friendly_name not in used_names:
        return friendly_name

    stem = Path(friendly_name).stem
    suffix = "".join(Path(friendly_name).suffixes)

    counter = 1
    while True:
        filename = f"{stem}_{counter:02}{suffix}"
        if filename not in used_names:
            return filename
        counter += 1
