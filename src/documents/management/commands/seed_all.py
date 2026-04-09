"""
seed_all — central entry point that runs all individual seed commands.

Add new seed commands to consts.SEED_COMMANDS to include them.
"""

from django.core.management import call_command
from django.core.management.base import BaseCommand

from documents.management.commands.consts import SEED_COMMANDS


class Command(BaseCommand):
    help = "Runs all seed commands to populate default data."

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("Running all seeds...\n"))
        for cmd in SEED_COMMANDS:
            self.stdout.write(self.style.MIGRATE_LABEL(f"=> {cmd}"))
            call_command(cmd, stdout=self.stdout, stderr=self.stderr)
        self.stdout.write(self.style.SUCCESS("\nAll seeds completed."))
