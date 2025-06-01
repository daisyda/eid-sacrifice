import csv
from main_app.models import Udhiyah

with open('sacrifices.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            # Create object only with known model fields
            Udhiyah.objects.create(
                reference_number=row.get('reference_number', ''),
                order_number=row.get('order_number', ''),
                name=row.get('name', ''),
                phone_number=row.get('phone_number', '') or row.get('phone', ''),  # fallback
                product=row.get('product', ''),
                status=row.get('status', ''),
                serial_number=row.get('serial_number', '')
            )
        except Exception as e:
            print(f"❌ Skipped row due to error: {e} — {row}")
