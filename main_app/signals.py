from django.db.models.signals import pre_save
from django.dispatch import receiver
from main_app.models import Udhiyah
from main_app.utils.zapier import send_status_update_to_zapier

@receiver(pre_save, sender=Udhiyah)
def notify_status_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # it's a new object, skip

    try:
        old_instance = Udhiyah.objects.get(pk=instance.pk)
    except Udhiyah.DoesNotExist:
        return

    if old_instance.status != instance.status:
        send_status_update_to_zapier(instance)
