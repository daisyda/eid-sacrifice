# fix_status.py
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

def fix_status_values():
    updated = 0

    for obj in Udhiyah.objects.all():
        status_value = obj.status.strip()

        # فقط الحالات العربية
        if status_value in STATUS_MAP:
            obj.status = STATUS_MAP[status_value]
            obj.save()
            updated += 1

    if updated:
        print(f"✅ Auto-fixed {updated} status values.")
