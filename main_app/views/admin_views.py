import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from ..models import Udhiyah
from django.contrib.auth.decorators import login_required


def udhiya_list(request):
    udhiyas = Udhiyah.objects.all()
    return render(request, 'admin/udhiyah_list.html', {'udhiyas': udhiyas})


@csrf_exempt
def update_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        numbers = data.get('numbers', [])
        status_value = data.get('status', '')

        if not status_value:
            return JsonResponse({"error": "لا توجد حالة محددة"}, status=400)

        Udhiyah.objects.filter(serial_number__in=numbers).update(status=status_value)
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)


def choose_number(request):
    return render(request, 'admin/choose_number.html')


def choose_status(request):
    return render(request, 'admin/choose_status.html')


def get_sacrifice_numbers(request):
    status = request.GET.get("status", "")
    
    # ✅ Fixed mapping: using internal English status values
    required_previous = {
        "slaughtered": "booked",
        "cutting": "slaughtered",
        "distributing": "cutting",
        "done": "distributing",
    }

    previous_status = required_previous.get(status)
    if not previous_status:
        return JsonResponse({"numbers": [], "selected_numbers": []})

    valid_numbers = list(Udhiyah.objects.filter(status=previous_status).values_list("serial_number", flat=True))
    selected_numbers = list(Udhiyah.objects.filter(status=status).values_list("serial_number", flat=True))
    all_displayed = list(set(valid_numbers + selected_numbers))

    return JsonResponse({
        "numbers": all_displayed,
        "selected_numbers": selected_numbers
    })


# -------------------------------
# Status Pages (Admin Panel)
# -------------------------------

@login_required
def page_slaughtered(request):
    udhiyas = Udhiyah.objects.filter(status="booked")  # for تم الذبح
    return render(request, 'admin/slaughtered.html', {
        "status": "تم الذبح",
        "udhiyas": udhiyas
    })

@login_required
def page_Cut(request):
    udhiyas = Udhiyah.objects.filter(status="slaughtered")  # for تم التقطيع
    return render(request, 'admin/cut.html', {
        "status": "تم التقطيع",
        "udhiyas": udhiyas
    })

@login_required
def page_Distributing_Now(request):
    udhiyas = Udhiyah.objects.filter(status="cutting")  # for جاري التوزيع
    return render(request, 'admin/distributing_now.html', {
        "status": "جاري التوزيع",
        "udhiyas": udhiyas
    })

@login_required
def page_Distributing_Done(request):
    udhiyas = Udhiyah.objects.filter(status="distributing")  # for تم التوزيع
    return render(request, 'admin/distribution_done.html', {
        "status": "تم التوزيع",
        "udhiyas": udhiyas
    })



from django.core.management import call_command
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
import os

@staff_member_required
def run_load_sacrifices(request):
    try:
        filepath = os.path.join(settings.BASE_DIR, 'sacrifices.csv')
        if not os.path.exists(filepath):
            return HttpResponse("❌ File not found: sacrifices.csv")

        call_command('load_sacrifices', filepath)
        return HttpResponse("✅ Sacrifices loaded successfully.")
    except Exception as e:
        return HttpResponse(f"❌ Error: {str(e)}")
