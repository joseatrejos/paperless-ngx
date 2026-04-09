"""
seed_workflows — creates default workflows that come pre-installed.

Each workflow is created only if no workflow with that name already exists,
so running this command multiple times is safe (idempotent).

Users can disable or delete any of these workflows from the UI at any time.
"""

from django.core.management.base import BaseCommand

from documents.management.commands.consts import (
    ACTION, BODY, EMAIL, ENABLED, ORDER, SEED_WORKFLOW_PREFIX, SUBJECT, TRIGGER, TYPE, NAME, MATCHING_ALGORITHM, INCLUDE_DOCUMENT,
    TPL_TITLE, TPL_ADDED, TPL_OWNER, TPL_ORIGINAL_FILE, TPL_URL,
    LBL_TITLE, LBL_ADDED, LBL_OWNER, LBL_ORIGINAL_FILE,
)

from documents.models import Workflow
from documents.models import WorkflowAction
from documents.models import WorkflowActionEmail
from documents.models import WorkflowTrigger


def _propagate(name: str, order: int, trigger_type: WorkflowTrigger.WorkflowTriggerType) -> dict:
    return {
        NAME: f"{SEED_WORKFLOW_PREFIX} {name}",
        ORDER: order,
        TRIGGER: {TYPE: trigger_type, MATCHING_ALGORITHM: WorkflowTrigger.WorkflowTriggerMatching.NONE},
        ACTION: {TYPE: WorkflowAction.WorkflowActionType.PROPAGATE_TAG_PERMISSIONS},
    }


def _email(name: str, order: int, trigger_type: WorkflowTrigger.WorkflowTriggerType, subject: str, body: str) -> dict:
    return {
        NAME: f"{SEED_WORKFLOW_PREFIX} {name}",
        ORDER: order,
        TRIGGER: {TYPE: trigger_type, MATCHING_ALGORITHM: WorkflowTrigger.WorkflowTriggerMatching.NONE},
        EMAIL: {SUBJECT: subject, BODY: body, INCLUDE_DOCUMENT: False},
    }


PROPAGATE_WORKFLOWS = [
    _propagate("Propagate tag permissions on document updated", 0, WorkflowTrigger.WorkflowTriggerType.DOCUMENT_UPDATED),
    _propagate("Propagate tag permissions on document added",   1, WorkflowTrigger.WorkflowTriggerType.DOCUMENT_ADDED),
    _propagate("Propagate tag permissions on consumption",      2, WorkflowTrigger.WorkflowTriggerType.CONSUMPTION),
]

EMAIL_WORKFLOWS = [
    _email(
        "Email notification on document added", 3, WorkflowTrigger.WorkflowTriggerType.DOCUMENT_ADDED,
        subject=f"Paperless: Document added — {TPL_TITLE}",
        body=(
            f"A new document has been added to Paperless-ngx.\n\n"
            f"{LBL_TITLE}: {TPL_TITLE}\n"
            f"{LBL_ADDED}: {TPL_ADDED}\n"
            f"{LBL_OWNER}: {TPL_OWNER}\n"
            f"{TPL_URL}"
        ),
    ),
    _email(
        "Email notification on document deleted", 4, WorkflowTrigger.WorkflowTriggerType.DOCUMENT_DELETED,
        subject=f"Paperless: Document deleted — {TPL_TITLE}",
        body=(
            f"A document has been deleted from Paperless-ngx.\n\n"
            f"{LBL_TITLE}: {TPL_TITLE}\n"
            f"{LBL_ORIGINAL_FILE}: {TPL_ORIGINAL_FILE}\n"
            f"{LBL_OWNER}: {TPL_OWNER}"
        ),
    ),
]


class Command(BaseCommand):
    help = "Creates default workflows if they do not already exist."

    def handle(self, *args, **options):
        all_specs = PROPAGATE_WORKFLOWS + EMAIL_WORKFLOWS

        for spec in all_specs:
            workflow, _ = Workflow.objects.get_or_create(
                name=spec[NAME],
                defaults={ORDER: spec[ORDER], ENABLED: True},
            )

            if not workflow.triggers.exists():
                workflow.triggers.add(WorkflowTrigger.objects.create(**spec[TRIGGER]))

            if not workflow.actions.exists():
                if EMAIL in spec:
                    email_obj = WorkflowActionEmail.objects.create(**spec[EMAIL], to="")
                    action = WorkflowAction.objects.create(
                        type=WorkflowAction.WorkflowActionType.EMAIL,
                        email=email_obj,
                    )
                else:
                    action = WorkflowAction.objects.create(**spec[ACTION])
                workflow.actions.add(action)


