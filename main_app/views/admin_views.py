from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.core.management import call_command
from django.conf import settings
from ..models import Udhiyah
import json
import os

# ✅ فقط للمستخدمين المشرفين
def staff_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='admin_login')(view_func)

# ✅ تسجيل دخول المشرف
def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('choose_status')
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة، أو الحساب ليس مشرفاً.')

    return render(request, 'admin/admin_login.html')

# ✅ عرض كل الأضاحي
@staff_required
def udhiya_list(request):
    udhiyas = Udhiyah.objects.all()
    return render(request, 'admin/udhiyah_list.html', {'udhiyas': udhiyas})

# ✅ تحديث حالة الأضاحي
@csrf_exempt
@staff_required
def update_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        numbers = data.get('numbers', [])
        status_value = data.get('status', '')

        if not status_value:
            return JsonResponse({"error": "❌ لم يتم تحديد الحالة."}, status=400)

        Udhiyah.objects.filter(serial_number__in=numbers).update(status=status_value)
        return JsonResponse({"success": True, "message": "✅ تم تحديث الحالة بنجاح."})

    return JsonResponse({"error": "❌ الطلب غير صالح."}, status=400)

# ✅ اختيار رقم أو حالة
@staff_required
def choose_number(request):
    return render(request, 'admin/choose_number.html')

@staff_required
def choose_status(request):
    return render(request, 'admin/choose_status.html')

# ✅ عرض الأرقام المؤهلة فقط حسب الحالة السابقة
@staff_required
def get_sacrifice_numbers(request):
    status = request.GET.get("status", "")

    # التسلسل المنطقي للحالات
    status_flow = {
        "slaughtered": "booked",
        "cut": "slaughtered",
        "distributing_now": "cut",
        "distributed": "distributing_now",
    }

    previous_status = status_flow.get(status)
    if not previous_status:
        return JsonResponse({"numbers": [], "selected_numbers": []})

    valid_numbers = list(
        Udhiyah.objects.filter(status=previous_status).values_list("serial_number", flat=True)
    )

    selected_numbers = list(
        Udhiyah.objects.filter(status=status).values_list("serial_number", flat=True)
    )

    return JsonResponse({
        "numbers": valid_numbers,
        "selected_numbers": selected_numbers
    })

# ✅ صفحات الحالات (كل صفحة تعرض فقط الأضاحي بالحالة المطلوبة)
@staff_required
def page_slaughtered(request):  # حالة "booked"
    udhiyas = Udhiyah.objects.filter(status="booked")
    return render(request, 'admin/slaughtered.html', {
        "status": "slaughtered",
        "udhiyas": udhiyas
    })

@staff_required
def page_Cut(request):  # حالة "slaughtered"
    udhiyas = Udhiyah.objects.filter(status="slaughtered")
    return render(request, 'admin/cut.html', {
        "status": "cut",
        "udhiyas": udhiyas
    })

@staff_required
def page_Distributing_Now(request):  # حالة "cut"
    udhiyas = Udhiyah.objects.filter(status="cut")
    return render(request, 'admin/distributing_now.html', {
        "status": "distributing_now",
        "udhiyas": udhiyas
    })

@staff_required
def page_Distributing_Done(request):  # حالة "distributing_now"
    udhiyas = Udhiyah.objects.filter(status="distributing_now")
    return render(request, 'admin/distribution_done.html', {
        "status": "distributed",
        "udhiyas": udhiyas
    })

# ✅ تحميل الأضاحي من CSV
@staff_required
def run_load_sacrifices(request):
    try:
        filepath = os.path.join(settings.BASE_DIR, 'sacrifices.csv')
        if not os.path.exists(filepath):
            return HttpResponse("❌ لم يتم العثور على الملف: sacrifices.csv")

        call_command('load_sacrifices', filepath)
        return HttpResponse("✅ تم تحميل الأضاحي بنجاح.")
    except Exception as e:
        return HttpResponse(f"❌ خطأ: {str(e)}")
