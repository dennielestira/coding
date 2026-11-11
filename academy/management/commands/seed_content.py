from django.core.management.base import BaseCommand

from academy.seed_data import seed_database


class Command(BaseCommand):
    help = "Populate the learning platform with lesson data and starter content"

    def handle(self, *args, **options):
        seed_database()
        self.stdout.write(self.style.SUCCESS("Starter content loaded successfully."))
