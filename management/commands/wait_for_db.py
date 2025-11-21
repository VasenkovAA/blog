# management/commands/wait_for_db.py
import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        max_retries = 30
        for i in range(max_retries):
            try:
                connections["default"].ensure_connection()
                self.stdout.write(self.style.SUCCESS("Database available!"))
                return
            except OperationalError:
                if i == max_retries - 1:
                    self.stdout.write(self.style.ERROR("Database unavailable"))
                    raise
                time.sleep(2)
