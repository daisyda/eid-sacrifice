from django.core.management.base import BaseCommand
from main_app.models import Udhiyah

STATUS_MAP = {
    'تم الدفع': 'paid',
    'تم حجز الأضحية': 'booked',
    'تم الذبح': 'slaughtered',
    'تم التقطيع': 'cutting',
    'نصف الأضحية جاهز للاستلام': 'half_ready',
    'جاري التوزيع': 'distributing',
    'تم التوزيع': 'done',
}

class Command(BaseCommand):
    help = 'Normalize status field for Udhiyah records'

    def handle(self, *args, **kwargs):
        updated = 0
        skipped = 0

        for obj in Udhiyah.objects.all():
            status_value = obj.status.strip()
            if status_value in STATUS_MAP:
                obj.status = STATUS_MAP[status_value]
                obj.save()
                self.stdout.write(self.style.SUCCESS(f"✅ Updated ID {obj.id} to: {obj.status}"))
                updated += 1
            elif status_value in STATUS_MAP.values():
                skipped += 1
                self.stdout.write(f"ℹ️ Already correct ID {obj.id}: {status_value}")
            else:
                self.stdout.write(self.style.WARNING(f"⚠️ Skipped ID {obj.id}: Unknown status '{status_value}'"))

        self.stdout.write(f"\n🎉 Done. Updated: {updated}, Already correct: {skipped}")
