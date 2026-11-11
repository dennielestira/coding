from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .seed_data import seed_database


@receiver(post_migrate)
def populate_learning_content(sender, **kwargs):
    seed_database()
