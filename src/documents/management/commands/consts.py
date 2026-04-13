"""
Shared constants for management commands (seeds, etc.).
"""

# List of all seed commands run by seed_all.
# Add new seeds here to include them automatically.
SEED_COMMANDS: list[str] = [
    "seed_users",
    "seed_workflows",
]

# Default workflow name prefix used to identify system-created workflows.

# Dict keys used in workflow spec dicts (avoids magic strings).
NAME = "name"
ORDER = "order"
TRIGGER = "trigger"
ACTION = "action"
EMAIL = "email"
TYPE = "type"
MATCHING_ALGORITHM = "matching_algorithm"
SUBJECT = "subject"
BODY = "body"
INCLUDE_DOCUMENT = "include_document"
ENABLED = "enabled"

# Jinja2 placeholders used in email templates.
TPL_TITLE = "{{ doc_title }}"
TPL_ADDED = "{{ added }}"
TPL_OWNER = "{{ owner_username }}"
TPL_ORIGINAL_FILE = "{{ original_filename }}"
TPL_URL = "{% if doc_url %}URL: {{ doc_url }}{% endif %}"

# Email body field labels.
LBL_TITLE = "Title"
LBL_ADDED = "Added"
LBL_OWNER = "Owner"
LBL_ORIGINAL_FILE = "Original file"
