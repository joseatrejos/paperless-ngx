# ---------------------------------------------------------------------------
# Email / theming constants
# ---------------------------------------------------------------------------

EMAIL_TEMPLATE_WORKFLOW_NOTIFICATION = "account/email/workflow_notification.html"

EMAIL_LOGO_CID = "email_logo"
EMAIL_MIXED_SUBTYPE_RELATED = "related"

PAPERLESS_DEFAULT_THEME_COLOR = "#17541f"

# Template context key names
EMAIL_CTX_SUBJECT = "subject"
EMAIL_CTX_BODY = "body"
EMAIL_CTX_DOC_URL = "doc_url"
EMAIL_CTX_APP_TITLE = "app_title"
EMAIL_CTX_LOGO_URL = "logo_url"
EMAIL_CTX_PRIMARY_COLOR = "primary_color"

# Global UI settings keys
UI_SETTING_APP_THEME_COLOR = "app_theme_color"

# Shared API keys
API_KEY_MESSAGE = "message"

DOCUMENSO_CREATE_ENVELOPE_PATH = "/api/v2/envelope/create"
DOCUMENSO_DOCUMENTS_PATH = "/documents"
DOCUMENSO_DOCUMENT_EDIT_PATH = "/t/{team_slug}/documents/{document_id}/edit"

DOCUMENSO_AUTH_HEADER = "Authorization"
DOCUMENSO_DOCUMENT_IDS_KEY = "document_ids"
DOCUMENSO_FILES_FIELD = "files"
DOCUMENSO_PAYLOAD_FIELD = "payload"
DOCUMENSO_RESPONSE_URL_KEY = "url"
DOCUMENSO_RESPONSE_ID_KEY = "id"
DOCUMENSO_RESPONSE_DOCUMENT_ID_KEY = "documentId"
DOCUMENSO_TYPE_KEY = "type"
DOCUMENSO_TITLE_KEY = "title"
DOCUMENSO_PAYLOAD_TYPE = "DOCUMENT"
DOCUMENSO_DOCUMENTS_LABEL = "documents"

DOCUMENSO_VIEW_DOCUMENT_PERMISSION = "view_document"
DOCUMENSO_INSUFFICIENT_PERMISSIONS = "Insufficient permissions"

DOCUMENSO_JSON_CONTENT_TYPE = "application/json"
DOCUMENSO_PDF_CONTENT_TYPE = "application/pdf"

DOCUMENSO_NOT_CONFIGURED = "Documenso integration is not configured"
DOCUMENSO_USER_NO_GROUP = "User does not belong to a Documenso-configured group"
DOCUMENSO_DOCUMENT_IDS_REQUIRED = "document_ids must be a non-empty list"
DOCUMENSO_DOCUMENTS_NOT_FOUND = "One or more documents not found"
DOCUMENSO_NO_DOCUMENT_ID = "Documenso returned no document id"
DOCUMENSO_SEND_ERROR = "Error sending to Documenso: {error}"
DOCUMENSO_API_ERROR = "Documenso error: {response_text}"
DOCUMENSO_API_ERROR_LOG = "Documenso API error %s: %s"
DOCUMENSO_RESPONSE_MISSING_DOCUMENT_ID_LOG = (
	"Documenso response missing document id: %s"
)
DOCUMENSO_SEND_EXCEPTION_LOG = "Error sending documents to Documenso: %s"
