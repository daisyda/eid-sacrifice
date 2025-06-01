from django.db import models

# Define the available status options
STATUS_CHOICES = [
    ('paid', 'تم الدفع'),
    ('booked', 'تم حجز الأضحية'),
    ('slaughtered', 'تم الذبح'),
    ('cutting', 'تم التقطيع'),
    ('half_ready', 'نصف الأضحية جاهز للاستلام'),
    ('distributing', 'جاري التوزيع'),
    ('done', 'تم التوزيع'),
]

class Udhiyah(models.Model):
    serial_number = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    product = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    order_number = models.CharField(max_length=100, blank=True, null=True)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    
    # ✅ Add this line
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.serial_number} - {self.status}"
