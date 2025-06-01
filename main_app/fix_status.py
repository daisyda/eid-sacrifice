from main_app.models import Udhiyah

# Arabic-to-English status code mapping
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
        arabic_status = obj.status.strip()
        if arabic_status in STATUS_MAP:
            obj.status = STATUS_MAP[arabic_status]
            obj.save()
            updated += 1
            print(f"✅ Updated ID {obj.id} to: {obj.status}")
        else:
            print(f"⚠️ Skipped ID {obj.id}: Unknown status '{arabic_status}'")
    print(f"\n🎉 Done. Total updated: {updated}")

if __name__ == "__main__":
    fix_status_values()
