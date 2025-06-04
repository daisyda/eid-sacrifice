from django.core.management.base import BaseCommand
from main_app.models import Udhiyah
import csv

class Command(BaseCommand):
    help = 'Load sacrifice data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        filepath = options['filepath']
        created = 0
        skipped = 0

        # ✅ Step 1: Delete all existing records
        Udhiyah.objects.all().delete()
        self.stdout.write(self.style.WARNING("🧹 Existing Udhiyah records deleted."))

        try:
            with open(filepath, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        Udhiyah.objects.create(
                            reference_number=row.get('reference_number', ''),
                            order_number=row.get('order_number', ''),
                            name=row.get('name', ''),
                            phone_number=row.get('phone_number', '') or row.get('phone', ''),
                            product=row.get('product', ''),
                            status=row.get('status', ''),
                            serial_number=row.get('serial_number', '')
                        )
                        created += 1
                    except Exception as e:
                        skipped += 1
                        self.stdout.write(self.style.WARNING(f"❌ Skipped: {e} — {row}"))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"❌ File not found: {filepath}"))
            return

        self.stdout.write(self.style.SUCCESS(f"✅ Done. Created: {created}, Skipped: {skipped}"))
