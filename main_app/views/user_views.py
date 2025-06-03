from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from ..models import Udhiyah, STATUS_CHOICES
import re

# -------------------------------
# Donor Views
# -------------------------------

def donor_search(request):
    return render(request, 'user/donor_search.html')

# Helper: Normalize phone input from user
def normalize_phone(phone_raw):
    if not phone_raw:
        return None

    # Convert Arabic numerals to English
    arabic_to_english = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
    phone = phone_raw.translate(arabic_to_english)

    # Remove non-digit characters (e.g. +, spaces)
    phone = re.sub(r'\D', '', phone)

    # Remove country code or leading zero
    if phone.startswith("00966"):
        phone = phone[5:]
    elif phone.startswith("966"):
        phone = phone[3:]
    elif phone.startswith("0"):
        phone = phone[1:]

    return phone

def donor_status(request):
    udhiyah_id = request.GET.get('udhiyah_id')
    raw_phone = request.GET.get('phone')
    phone = normalize_phone(raw_phone)

    print("🔍 Searching for order:", udhiyah_id, "| normalized phone:", phone)

    record = Udhiyah.objects.filter(serial_number=udhiyah_id, phone_number=phone).first()
    if not record:
        return render(request, 'user/donor_status.html', {'status': 'not_found'})

    donor_name = record.name
    current_status = record.status
    donation_type = getattr(record, 'donation_type', None)

    # نبدأ نعرف المتغير الأساسي أول
    status_sequence = ['paid', 'booked', 'slaughtered', 'cutting']

    # نضيف الباقي حسب نوع التبرع
    if donation_type == 'half':
        status_sequence += ['half_ready', 'distributing', 'done']
    else:
    # إذا نوع التبرع فاضي أو "full"
        status_sequence += ['distributing', 'done']


    current_index = status_sequence.index(current_status) if current_status in status_sequence else -1
    timeline_steps = []

    for i, step in enumerate(status_sequence):
        status = 'done' if i < current_index else 'active' if i == current_index else 'upcoming'
        timeline_steps.append({
            'code': step,
            'label': dict(Udhiyah._meta.get_field('status').choices).get(step, step),
            'status': status
        })

    return render(request, 'user/donor_status.html', {
        'udhiyah_id': record.serial_number,
        'phone': record.phone_number,
        'donor_name': donor_name,
        'status': current_status,
        'timeline_steps': timeline_steps,
    })
    
    # أضيفي هذا في views.py (مثلاً فوق)
from django.http import HttpResponse
from main_app.fix_status import fix_status_values  # تأكدي من المسار

def run_fix_status(request):
    try:
        fix_status_values()
        return HttpResponse("✅ Status updated successfully.")
    except Exception as e:
        import traceback
        return HttpResponse(
            f"❌ Error occurred:<br><pre>{traceback.format_exc()}</pre>",
            content_type="text/html",
            status=500
        )


