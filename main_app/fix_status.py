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
    skipped = 0

    for obj in Udhiyah.objects.all():
        status_value = obj.status.strip()

        # Case 1: Arabic to English mapping needed
        if status_value in STATUS_MAP:
            obj.status = STATUS_MAP[status_value]
            obj.save()
            updated += 1
            print(f"✅ Updated ID {obj.id} to: {obj.status}")

        # Case 2: Already correct English status
        elif status_value in STATUS_MAP.values():
            skipped += 1
            print(f"ℹ️ Already correct ID {obj.id}: {status_value}")

        # Case 3: Unknown value
        else:
            print(f"⚠️ Skipped ID {obj.id}: Unknown status '{status_value}'")

    print(f"\n🎉 Done. Updated: {updated}, Already correct: {skipped}")
