from django.utils import timezone
from django.core.management.base import BaseCommand

from authentication.models import Session


class Command(BaseCommand):
    def handle(self, *args, **options):
        deleted_count, _ = Session.objects.filter(
            expires_at__lte=timezone.now()
        ).delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"Deleted expired sessions: {deleted_count}"
            )
        )
