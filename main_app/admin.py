from django.contrib import admin
from .models import Udhiyah

@admin.register(Udhiyah)
class UdhiyahAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'name', 'status', 'updated_at')
    search_fields = ('serial_number', 'order_number', 'name', 'phone_number')
    list_filter = ('status',)
