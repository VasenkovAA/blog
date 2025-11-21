from django.contrib.sites.models import Site
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Setup default site"

    def handle(self, *args, **options):
        site, created = Site.objects.get_or_create(
            id=1, defaults={"domain": "127.0.0.1:8080", "name": "localhost"}
        )
        if not created:
            site.domain = "127.0.0.1:8080"
            site.name = "localhost"
            site.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully {'created' if created else 'updated'} site: {site.name}"
            )
        )
