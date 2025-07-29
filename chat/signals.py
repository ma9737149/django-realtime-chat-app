from django_cleanup.signals import cleanup_pre_delete
from django.dispatch import receiver

@receiver(cleanup_pre_delete)
def prevent_deleting_defaults(sender, file, **kwargs):
    if file.name.startswith("defaults/"):
        kwargs['file']._committed = False  
